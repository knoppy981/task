# task

# Setup

To run this code you will need a python enviroment with the libraries specified in requirements.txt

I am running the code on 
python 3.11.5
node 20.9.0
@vue/cli 5.0.8

setup a .env file on the root folder of the directory with 
MONGO_URI="your mongodb uri"

# Seeding the database

run py parser.py to seed the database

# Run the application

to run the application open two terminals
1 terminal
go to /server
run: flask run

2 terminal
go to /my-vue-app
run: npm install
run: npm run serve

the vue app should be running on port 8080 and the flask server on port 5000