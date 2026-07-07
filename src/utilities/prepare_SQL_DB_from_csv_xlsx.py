import os
import pandas as pd

from load_config import LoadConfig

#Sqlalchemy is used to make conversation between python and database
from sqlalchemy import create_engine
#create_engine creates connections to the database
from sqlalchemy import inspect
#inspect is used to find any tables or columns in database

class Prepare_SQL_from_Tabular_Data:
    """"
    A class that prepares a SQL database from CSV or XLSX files within a specified directory.
    This class reads each file, converts the data to a DataFrame, and then
    stores it as a table in a SQLite database, which is specified by the application configuration.
    """
    #Step1:Establish a connection with csv_xlsx files
    def __init__(self, file_dir) -> None:
        """Initialize an instance of Prepare_SQL_From_Tabular_Data.
        Args: files_dir (str): The directory containing the CSV or XLSX files to be converted to SQL tables."""
        get_app_configuration=LoadConfig()
        self.file_directory=file_dir                                            #suppose file_dir=data/csv_xlsx
        self.file_list=os.listdir(self.file_directory)                          #[Cancer_Data.csv, diabetes.csv]
        db_path=get_app_configuration.stored_csv_xlsx_sqldb_directory           #ostad/AI Agent Development/Database interaction/data/csv_xlsx_sqldb.db
        db_path=f'sqlite:///{db_path}'                                          #sqlite:///ostad/AI Agent Development/Database interaction/data/csv_xlsx_sqldb.db
        self.engine=create_engine(db_path)                                      #connection established
        print("Making Connection with the Database has beed Completed")

    #Step2: Convert csv or xlsx file to SQL file
    def create_SQL_DB(self):
        """Private method to convert CSV/XLSX files from the specified directory into SQL tables.
        Each file's name (excluding the extension) is used as the table name.
        The data is saved into the SQLite database referenced by the engine attribute."""
        for file in self.file_list:
            full_file_path=os.path.join(self.file_directory, file)             #data/csv_xlsx/Cancer_Data.csv or #data/csv_xlsx/diabetes.csv
            if file.endswith(".csv"):
                df=pd.read_csv(full_file_path)                                 #from csv to converted into dataframe
            if file.endswith(".xlsx"):
                df=pd.read_excel(full_file_path)
            else:
                print("File type not supported.")
            file_name=os.path.splitext(file)[0]                                #Cancer or diabetes
            file_extension=os.path.splitext(file)[1]                           #.csv
            df.to_sql(file_name,if_exists='replace', index=False)              #dataframe converted to SQL
            print("SQL File creation Successfully Done")

    #Step 3: Validate the New Created SQL DB , if the tables are present there or not
    def validate_SQL_DB(self):
        inspect_DB=inspect(self.engine)
        table_names=inspect_DB.get_table_names()
        print("========================================================")
        print(f"The Available table names are: {table_names}")
        print("========================================================")


    #Step 4: Run the function
    def run_pipeline(self):
        self.create_SQL_DB()
        self.validate_SQL_DB()


