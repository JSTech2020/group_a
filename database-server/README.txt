- These are docker file for the database server
- We are going to use the MongoDB with shell version v4.2.3
- If you want other version/type of server on your local system you can see https://hub.docker.com/_/mongo
- In case docker does not work for you, you can also install the server on your local system :)

-Basic instructions 
1. Install docker into system. Check the version using [ docker --version ] command.

2. Go into the directory where the DockerFile is located. For our project it is <git-repository-path>/database-server/docker

3. build the image (go into directory with)
	[ docker build -t <repository-name> . ]
   - you can check the creation of repository using [ docker images ] command

4. run the image(preferably on port 27017 as the codes are based on that)
	[  docker run --name <container-name> -d -v <git-repository-path>/database-server/data/db:/data/db -p 27017:27017 <repository-name> ]

    we are explicitly defining volume path for docker, so that the data of the database is not lost every time we restart the server

5. start server container
   [ docker container start <container-name> ]
   - you can check the status of the container using [ docker ps ] command

6. check MongoBD version
   after the container is activated, use [ mongo --version ] command to check the version of database.

