#performe the following commands in assignment directory

#create virtual environment(optional)
python -m venv env
env\Scripts\activate

#install requirment liberary
pip install -r requirment.txt


#start start docker instance of PostgreSQL ( if PostgreSQL not already installed, optional)
#in assignment directory execute following commands
docker-compose up -d

#edit credentials of PostgreSQL server in credential.py file

#please take note sheet name,excel file name, and location of file with respect to main file is hardcoded in code.
#it is taken in consideration that first 5 row and last 3 colums is ignored in etl process.
#*********************************************************

#run main.py to execute whole process

#*********************************************************

#run CreateTableScript.py to create empty CreateTableScript(optional)
#run wrangler.py to run only ETL process(optional)
