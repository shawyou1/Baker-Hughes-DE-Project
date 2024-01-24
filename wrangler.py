from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
import pandas as pd


#Connection of object for sql multiple connection(redundant)
class newConnection:
    def __init__(self, serverName, database, username, password, schema):
        self.serverName = serverName
        self.database = database
        self.username = username
        self.password = password
        self.engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{serverName}/{database}', connect_args={'options': f'-csearch_path={schema}'})
       

    def connect(self):
            self.Session = sessionmaker(bind=self.engine)
            return self.Session()
        


def readTrafomLoad(locationDfname,DataDFname,sheet,server):
    #slice datafrom to get location and type of location row
    sheet11=sheet.iloc[4:6,1:]
    #backfill null values in location
    list1= sheet11.iloc[0].values
    list11 = [list1[i-1] if pd.isna(list1[i]) else list1[i] for i in range(0,len(list1))][:-3]
    #list of location type
    list2= list(sheet11.iloc[1].values)[:-3]
    #location table
    locations={"Location":list11,"Type":list2}
    loactionsUS=pd.DataFrame(locations)
    #save location data in stagingtable in SQL DB
    loactionsUS.to_sql("locationStage",con=server.engine, chunksize=5000,if_exists="replace")
    sheet12=sheet.set_index(sheet.columns[0])
    #subsetting table to ignore first 5 rows and last 3 "Total" columns
    sheet12=sheet12.iloc[6:,:-3]

    #updating columns with location table index
    sheet12.columns=list(loactionsUS.index)
    sheet12.reset_index(inplace=True)
    sheet12.rename(columns={sheet12.columns[0]:"date"}, inplace = True)
    sheet12=pd.melt(sheet12,id_vars="date",var_name="Location",value_name="Value")
    #Save data to staging table
    sheet12.to_sql("DataDFStage",con=server.engine, chunksize=5000,if_exists="replace",index=False)

    #merge sfrom stage table to actual table 
    merge_query1 = f"""
    MERGE INTO "{locationDfname}" AS target
    USING "locationStage" AS sor
    ON target."index" = sor."index"
    WHEN MATCHED THEN
        UPDATE SET 
            "index" = sor.index,
            "Location" = sor."Location",
            "Type" = sor."Type"
    WHEN NOT MATCHED THEN
        INSERT ("index", "Location", "Type")
        VALUES (sor."index", sor."Location", sor."Type");
    """
    session = server.connect()
    # Use session.execute to execute the SQL query
    session.execute(text(merge_query1))

    # Commit the changes
    session.commit()


    #merge sfrom stage table to actual table 
    merge_query2 = f"""
    MERGE INTO "{DataDFname}" AS target
    USING "DataDFStage" AS sor
    ON target."date" = sor."date" and target."location" = sor."Location" and target."value" = sor."Value"
    WHEN MATCHED THEN
        UPDATE SET 
            "date" = sor.date,
            "location" = sor."Location",
            "value" = sor."Value"
    WHEN NOT MATCHED THEN
        INSERT ("date", "location", "value")
        VALUES (sor."date", sor."Location", sor."Value");
    """
    session = server.connect()
    # Use session.execute to execute the SQL query
    session.execute(text(merge_query2))

    # Commit the changes
    session.commit()
    # Close the session
    session.close()


if __name__ == "__main__":
    import pandas as pd
    import os

    #connection to sql DB
    from credential import *
    server = newConnection(serverName, database, username, password,schema)

    #reading exxcel sheets in pandas
    sheet1=pd.read_excel(os.getcwd()+r"\wetransfer_ea-assessment-shubham-shaw-senior-data-engineer-kolkata_2024-01-10_1145\BH data.xlsx",sheet_name="US L & OS Split by State")
    sheet2=pd.read_excel(os.getcwd()+r"\wetransfer_ea-assessment-shubham-shaw-senior-data-engineer-kolkata_2024-01-10_1145\BH data.xlsx",sheet_name="Canada L & OS Split by Province")

    readTrafomLoad("locationUS","DataUS",sheet1,server)
    readTrafomLoad("locationCA","DataCA",sheet2,server)