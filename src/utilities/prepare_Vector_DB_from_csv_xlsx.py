import os
import pandas as pd
from anyio import sleep_forever

from utlities.load_config import LoadConfig

class Prepare_Vector_DB_from_csv_xlsx:
    #Step-1: Load the predefined blueprint
    def __init__(self, file_dir:str):
        """ Initialize the instance with the file_dir and load the app_configuration
            Args: fir_dir:str: The directory path to be processed"""
        self.app_configuration=LoadConfig()
        self.file_directory=file_dir

    #Step-2: Convert the csv or xlsx file to vectordb
    def create_Vector_DB(self):


