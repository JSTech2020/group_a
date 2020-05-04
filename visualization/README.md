go into the directory @group_a/visualization

1. Setup mongo db. You can use either system database or create docker container. If you want to use docker container, do as follows:
    a. Install docker in your system. For windows go here: https://docs.docker.com/docker-for-windows/install/
    b. 

1. Create virtual environment for python 3.7, using virtualenv or conda
   
2. Source to the python environment. Install spacy model for German Language using the following command
    (env) > pip install spacy 
    (env) > python -m spacy download de_core_news_sm

3. install required packages in python environment:
    > pip install -r requirements.txt

4. Run flask server:
    > python app.py
    
5. go into client then install required packages
    > cd client
    > npm install
    
    Note: Might have to do [ sudo npm install -g @vue/cli@3.7.0 ] if npm install doesn't work immidiately
    
6. Serve frontend in dev mode:
    > npm run serve
    

