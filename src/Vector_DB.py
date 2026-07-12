from utilities.prepare_Vector_DB_from_csv_xlsx import Prepare_Vector_DB_from_Tabular_Data
from utilities.load_config import LoadConfig
from pyprojroot import here

app_configuration=LoadConfig()

if __name__=='__main__':
    from pyprojroot import here

    titanic_dir = here("data/for_upload/titanic_small.csv")
    # Create an instance of the PrepareVectorDBFromTabularData class with the file directory
    data_prep_instance = Prepare_Vector_DB_from_Tabular_Data(file_dir=titanic_dir)
    # Run the pipeline to prepare and inject the data into the vector database
    data_prep_instance.run_pipeline()



