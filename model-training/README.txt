Switch to python virtual env or Conda environment using Source.
In case of docker, The commands are written in Docker files .
We are using python version 3.7, wo we setup environment accordingly.
Our path to work for python scripts os <git-repository-path>/model-training

1. Install packages using requirements.txt
 - in case of Conda, we need to install pip if not already installed using [ conda install pip ] command
 - We use [ pip install -r requirements.txt ] command
 

2. Install the SpaCy CNN core model for de
 - run [ python -m spacy download de_core_news_sm ]
 - source - https://spacy.io/models/de

3. Download BERT pretrained model
 -The pretrained model must be downloaded in the <git-repository-path>/model-training/models folder.
 -We are currently using "multi_cased_L-12_H-768_A-12" model
 -It can be downloaded from "https://storage.googleapis.com/bert_models/2018_11_23/multi_cased_L-12_H-768_A-12.zip"
 [source- https://github.com/google-research/bert/blob/master/README.md].


4. Run the python scripts/notebooks
 - I have also created jupyter notebooks in <git-repository-path>/model-training/samples folder. So we do not need to explicitly run the scripts.
 - The scripts exists only for cases we might require to run them through node server apis.
 - The notebooks need to be run in specific order:
   "notebook_import_from_file.ipynb" -> "notebook_preprocessing.ipynb" -> "notebook_similarity.ipynb".

 - In case you want to run the scripts manually you can do as follows:
     -We need to run the scripts in specific order as they are dependent on each other.
     -The scripts are inside <git-repository-path>/model-training/source folder
     -We can run the scripts simply by suing [ python <script-file(e.g. import_to_db.py)> ] command
     a. Run import_to_db.py script:
      -This script inserts the data from csv file to database table(stories).
      -If the data is already in db, and no new data is added in csv file, we do not need to run this file
     b. Run preprocessing.py script:
      -This script runs pre-processing of text from the db table(stories), and saves them in another db table(autotags).
      -This script runs preprocessing in each document in the stories collection, so it might take some time to process.
      -In case no new changes are made in stories collection, we do not need to run the script
     c. Run similarity.py script:
      -This script uses the BERT pretrained model to create vector embedding of our preprocessed tokens, and finds the similarities between the stories using cosine similarity.
      -The dependency for bert-server is already installed when installing packages from requirements.txt file(ref: 1)
      -We need to run the bert-server to access the pretrained model.
      -Go into directory <git-repository-path>/model-training/models.
      -To serve bert model we use [bert-serving-start -model_dir ./multi_cased_L-12_H-768_A-12/ -num_worker=1 -show_tokens_to_client] command
      -After the bert server is running we can run similarities.py