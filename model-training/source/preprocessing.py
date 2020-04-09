import sys
import re
import pandas as pd
import spacy
from pymongo import MongoClient

uri = 'mongodb://localhost:27017/'
database = 'zs_database'
collection_fetch = 'stories'
collection_push = 'autotags'

df = pd.DataFrame()
db = object

# exception handling for database operation
try:
    print("Connecting to database")
    # init mongodb client
    client = MongoClient(uri)
    db = client[database]

    # retrieving only story id and details for now
    df = pd.DataFrame(list(db[collection_fetch].find({}, {"_id":0, "id": 1, "plain_text": 1})))

    # check if push collection(autotags) already exists, if so, remove(drop) the collection for now

except:  # TODO: maybe be specific about the exceptions that can occur
    print('Unexpected error:', sys.exc_info()[0])
    print('Exiting system ...')
    exit()


# Clean given text
def clean_text(content):
    """
    Removing Unwanted Characters
    """
    # removing html tags
    content = re.sub('<[^<]+?>', '', content)

    # removing entity names
    content = re.sub('&[^<]+?;', '', content)

    # removing whitespace from escape characters
    content = re.sub(r'[\n\r\t\a\f\b\v]', '', content)

    # remove unwanted characters (eg ",',.,?,!). We might want to kee these later though.
    content = re.sub(r'[\'\-".?!,0-9“„–()]', '', content)

    """
    Encoding the proper format
    """
    # python 3 handles sting in UTF-8 by default
    # We need to write ode if we want to process data in other formats
    # for now default UTF-8 is ok

    return content


# Generate tokens for given text
def generate_tokens(content):
    # load plain text into spacy processor
    doc = nlp(content)

    # init list
    token_list = []
    lemma_list = []
    pos_list = []

    # Iterate through each token identified in doc
    for token in doc:
        # remove stop words for German Language like like 'eine', 'könnte'... from spacy lib.
        if (not token.is_stop) and (token.text != " ") and (token.text != ""):
            # additional trimming needed for some cases
            word = token.text.strip()
            lemma = token.lemma_.strip()
            pos = token.pos_.strip()

            # addictionl check to see if the trimmed or converted text is not empty
            if word != '':
                token_list.append(word)  # token list without stop word
            if lemma != '':
                lemma_list.append(lemma)
            if pos != '':
                pos_list.append(pos)

    # Entity listing through spaCy lib. requires text without stop words for wfficiency
    entity_list = [[i.text, i.label_] for i in doc.ents]
    noun_list = [chunk.text for chunk in doc.noun_chunks]

    return token_list, lemma_list, pos_list, entity_list, noun_list


"""
preprocess text and insert into collection
"""
# load spaCy core for German language
nlp = spacy.load('de_core_news_sm')

# check if push collection(autotags) already exists, if so, remove(drop) the collection for now
# TODO: handle exception
if collection_push in db.list_collection_names():
    collection = db[collection_push]
    if collection.estimated_document_count() != 0:
        print('Dropping the old collection (' + collection_push + ') ...')
        collection.drop()
collection = db[collection_push]

print("Pre-processing all text. This might take some time...")
print("Story id(s) processed: ", end=" ")
for x in df.iterrows():
    # fetching id and content for each item in data-frame
    index, item = x
    story_id = item.id
    content = item.plain_text

    # clean text for each document
    content = clean_text(content)

    """
    Creating Tokens without stop words
    crete lemma list and pat of speech list in case we need it later
    """
    # word tokanization and other preprocessing for each document
    token_list, lemma_list, pos_list, entity_list, noun_list = generate_tokens(content)


    # TODO
    # if we are going to use un-cased data sets, we need to change the tokens to lower case
    # use spaCy sentencizer component if sentence tokenizing is needed

    # insert into db
    # TODO: write try catch statement, possibly ignore this if singular document is not inserted and continue with other
    collection.insert_one(
        {
            "story_id": story_id,
            "tokens": token_list,
            "lemmas": lemma_list,
            "pos": pos_list,
            "nouns": noun_list,
            "entities": entity_list
        }
    )
    print(str(story_id), end=" ")

print('Done !!!')
print('Pre-processed data entered into (' + collection_push + ') collection')


