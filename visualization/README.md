go into the directory @group_a/visualization
1. Create virtual environment for python 3.7, using virtualenv or conda
   
2. Source to the python environment. Install spacy model for German Language using the following command
    > de_core_news_md

3. install required packages in python environment:
    > pip install -r requirements.txt

4. Run flask server:
    > python app.py
    
5. go into client then install required packages
    > cd client
    npm install
    
    Note: Might have to do [ sudo npm install -g @vue/cli@3.7.0 ] if npm install doesn't work immidiately
    
6. Serve frontend in dev mode:
    > npm run serve
    

