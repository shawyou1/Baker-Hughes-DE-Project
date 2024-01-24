from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from wrangler import readTrafomLoad
from CreateTableScript import createTables
import pandas as pd
import os


class newConnection:
    def __init__(self, serverName, database, username, password,schema ="public"):
        self.serverName = serverName
        self.database = database
        self.username = username
        self.password = password
        self.engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{serverName}/{database}', connect_args={'options': f'-csearch_path={schema}'})

    def connect(self):
            self.Session = sessionmaker(bind=self.engine)
            return self.Session()


if __name__ == "__main__":
    from credential import *

    #Create empty tables
    createTables(serverName,database ,username ,password ,schema )

    #connect to sql for etl 
    server = newConnection(serverName, database, username, password,schema)

    #read excel file
    sheet1=pd.read_excel(os.getcwd()+r"\wetransfer_ea-assessment-shubham-shaw-senior-data-engineer-kolkata_2024-01-10_1145\BH data.xlsx",sheet_name="US L & OS Split by State")
    sheet2=pd.read_excel(os.getcwd()+r"\wetransfer_ea-assessment-shubham-shaw-senior-data-engineer-kolkata_2024-01-10_1145\BH data.xlsx",sheet_name="Canada L & OS Split by Province")

    #transform excel file and load in sql DB
    #locationUS is the name of the table of location from sheet "US L & OS Split by State"
    #DataUS is the anme of the table of values from sheet "US L & OS Split by State" 
    readTrafomLoad("locationUS","DataUS",sheet1,server)

    #locationCA is the name of the table of location from sheet "Canada L & OS Split by Province"
    #DataCA is the anme of the table of values from sheet "Canada L & OS Split by Province" 
    readTrafomLoad("locationCA","DataCA",sheet2,server)
    print("\nProcess Completed!")