import sys
import re
import pandas as pd
import spacy


nlp = spacy.load('de_core_news_md')

def removeUnwantedCharacters(text):
    """
    Removing Unwanted Characters
    """
    # removing html tags
    text = re.sub('<[^<]+?>', '', text)

    # removing entity names
    text = re.sub('&[^<]+?;', '', text)

    # removing whitespace from escape characters
    text = re.sub(r'[\n\r\t\a\f\b\v]', '', text)
    text = re.sub(r'\xa0', '', text)

    # remove unwanted characters (eg ",',.,?,!). We might want to kee these later though.
    text = re.sub(r'[\'\-".?!,0-9“„–()]', '', text)
    text = re.sub(r'[\\\".?!,0-9():;]', '', text)
    # remove additional characters
    text = re.sub(r'[\‘\'\-\[\]»«0-9“„”…–]', '', text)

    """
    Encoding the proper format
    """
    # python 3 handles sting in UTF-8 by default
    # We need to write ode if we want to process data in other formats
    # for now default UTF-8 is ok

    return text


def tokenizeText(text):
    #load plain text into spacy processor
    doc = nlp(text)

    # filter for names
    filter_names = [i.text for i in doc.ents if i.label_.lower() in ["per"]]

    # init list
    token_list = []
    lemma_list = []
    wo_verbs_and_names = []
    pos_list = []

    # Iterate through each token identified in doc
    for token in doc:
        # remove stop words for German Language like like 'eine', 'könnte'... from spacy lib.
        if (not token.is_stop) and (token.text != " ") and (token.text.strip() != ""):
            # additional trimming needed for some cases
            word = token.text.strip()
            lemma = token.lemma_.strip()
            pos = token.pos_.strip()

            # addictional check to see if the trimmed or converted text is not empty
            if word != '':
                token_list.append(word)  # token list without stop word
            if lemma != '':
                lemma_list.append(lemma)
                if pos != "VERB" and pos != "ADV":
#                     wo_verbs_and_names.append(lemma)
                    if lemma not in filter_names:
                       wo_verbs_and_names.append(lemma)
            if pos != '':
                pos_list.append(pos)

    # Entity listing through spaCy lib. requires text without stop words for efficiency
    entity_list = [[i.text, i.label_] for i in doc.ents]
    noun_list = [chunk.text for chunk in doc.noun_chunks]

    return (token_list, lemma_list, pos_list, entity_list, noun_list, wo_verbs_and_names)


