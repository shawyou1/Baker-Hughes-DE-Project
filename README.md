###One of the research teams have requested to scrape data from Baker Hughes (BH) in order to understand changes in the weekly rig report.  Your task will be to create a schema that will house the data and an ETL to extract the data from the excel file provided and also to design some SQL tables that will house the data. 

###Task 1 - PostgreSQL Schema/Table Creation: 
Write a SQL query to create a schema that will house the data from both tabs in the provided excel file.
-	Design PostgreSQL tables to appropriately store the data retrieved from the provided Excel file. Consider the data types, relationships, and any necessary constraints. 
-	 Output required: (You may choose to do 1 or both of these outputs)
-	A raw SQL script that creates a schema called “web_scrapes” and also tables to store the data
-	Using python/SQLAlchemy create a schema called “web_scrapes” and also tables to store the data
  
###Task 2 -  Python ETL Development:
Create an ETL that will read the “Baker Hughes” excel file, transform/clean data as required and then load the data into the tables you have created. You are expected to extract data from both tabs of the excel file.  
You have been provided a template.zip file that gives you a template to structure your code.
-	Using Python, develop an ETL process that extracts the data from the provided Excel file.
-	Transform the extracted data as needed, such as cleaning, filtering, or aggregating, to ensure its compatibility with the SQL tables.
-	Load the transformed data into the SQL tables designed in the previous task.

###Task 2: Output required: 
-	Python file(s) that contain your code to Extract, Transform and Load the “Baker Hughes” excel file into the PostgreSQL tables you create
