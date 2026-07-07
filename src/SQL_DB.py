from utilities.prepare_SQL_DB_from_csv_xlsx import Prepare_SQL_from_Tabular_Data
from utilities.load_config import LoadConfig

app_configuration=LoadConfig()

if __name__=="__main__":
    prepare_sql_instance = app_configuration.stored_csv_xlsx_directory    #it returns data/csv_xlsx
    instance=Prepare_SQL_from_Tabular_Data(prepare_sql_instance)          #It has the blueprint
    prepare_sql = instance.run_pipeline()                                 #It runs the function

