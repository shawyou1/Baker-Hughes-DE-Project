def createTables(serverName = 'localhost',database = 'BakerHughes',username = "BakerHughes",password = "BakerHughes",schema ="web_scrapes"):
    
    from sqlalchemy import create_engine, text, DDL
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{serverName}/{database}')
    Session = sessionmaker(bind=engine)
    session = Session()

    #Create a DDL object to represent the schema creation statement
    create_schema = DDL(f"CREATE SCHEMA IF NOT EXISTS {schema};")
    set_schema = DDL(f"SET search_path TO {schema};")
    session.execute(create_schema)
    session.execute(set_schema)

    #Create Location Table for US
    createLocationTable = f"""CREATE TABLE IF NOT EXISTS "locationUS" (
        "index" INT PRIMARY KEY,
        "Location" VARCHAR(50) NOT NULL,
        "Type" VARCHAR(50) NOT NULL
    );"""
    session.execute(text(createLocationTable))
    session.commit()

    #Create Data Table for US
    createLocationTable = f"""CREATE TABLE IF NOT EXISTS"DataUS" (
        "date" DATE NOT NULL,
        "location" INT,
        "value" INT,
        FOREIGN KEY ("location") REFERENCES "locationUS"("index")
    );"""
    session.execute(text(createLocationTable))
    session.commit()

    ##Create Location Table for CA
    createLocationTable = f"""CREATE TABLE IF NOT EXISTS"locationCA" (
        "index" INT PRIMARY KEY,
        "Location" VARCHAR(50) NOT NULL,
        "Type" VARCHAR(50) NOT NULL
    );"""
    session.execute(text(createLocationTable))
    session.commit()

    ##Create Location Table for CA
    createLocationTable = f"""CREATE TABLE IF NOT EXISTS "DataCA" (
        "date" DATE NOT NULL,
        "location" INT,
        "value" INT,
        FOREIGN KEY ("location") REFERENCES "locationCA"("index")
    );"""

    session.execute(text(createLocationTable))
    session.commit()
    engine.dispose()

if __name__ == "__main__":    
    from credential import *
    createTables(serverName,database ,username ,password ,schema)