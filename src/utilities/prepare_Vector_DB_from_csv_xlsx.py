import os
import pandas as pd

from utilities.load_config import LoadConfig

class Prepare_Vector_DB_from_Tabular_Data:
    #Step-1: Load the predefined blueprint and defined file name
    def __init__(self, file_dir:str):
        """ Initialize the instance with the file_dir and load the app_configuration
            Args: fir_dir:str: The directory path to be processed"""
        self.app_configuration=LoadConfig()
        self.file_directory=file_dir
        print(f"File directory: {self.file_directory}")

    #Step-2: Convert the csv or xlsx file to dataframe
    def create_dataframe(self, file_dir:str):
        """Load Dataframe from Specified CSV/EXEL file
        Args: file_dir (str): The directory path of the file to be loaded.
        Returns:DataFrame, str: The loaded DataFrame and the file's base name without the extension.
        Raises:ValueError: If the file extension is neither CSV nor Excel."""
        file_name_with_extension=os.path.basename(file_dir)                    #if file_dir="data/diabetes.csv" the file_name_with_extension=diabetes.csv
        file_name=os.path.splitext(file_name_with_extension)[0]                   #file_name=diabetes
        file_extension=os.path.splitext(file_name_with_extension)[1]           #file_extension=.csv
        if file_extension == '.csv':
            df=pd.read_csv(file_dir)
        elif file_extension == '.xlsx':
            df=pd.read_excel(file_dir)
        else:
            raise ValueError('The file extension must be .csv or .xlsx')
        print("DataFrame Creation Successful")

        return df, file_name

    #Step-3: Convert the dataframe text into vector
    def convert_text_into_vector(self,df:pd.DataFrame, file_name:str):
        """Convert every row into text, then convert it into vector using embedding model.
        Args:df (pd.DataFrame): The DataFrame containing the data to be processed.
             file_name (str): The base name of the file for use in metadata.
        Returns: list, list, list, list: Lists containing documents, metadatas, ids, and embeddings respectively."""
        docs=[]
        embeddings=[]
        metadatas=[]
        ids=[]
        for index, rows in df.iterrows():
            output_str=" "                                #here output_str=empty
            for cols in df.columns:
                output_str +=f"{cols}:{rows[cols]},\n"    #output_str="value of that column" suppose column name:id and value:842517 then output_str=842517
            response= self.app_configuration.openai_client.embeddings.create(
                input=output_str,
                model=self.app_configuration.embedding_model_name)          #response={data:[{"embedding":[0.32,0.21,-0.43,0.23]}],model:model_name}
            embedding_output= response.data[0].embedding  #embedding_output=[0.32,0.21,-0.43,0.23]
            embeddings.append(embedding_output)           #embeddings=[[0.32,0.21,-0.43,0.23],[--------]
            docs.append(output_str)                       #docs=[id:85321,diagnosis:M,radius:17.99
            metadatas.append({"source":file_name})       #metadatas=[{"source":diabetes
            ids.append(f"id{index}")                     #ids=[ids0,ids1,....]
        print("Text are successfully converted into vector")
        return docs,embeddings, metadatas, ids

    #put this vectorDB in ChromaDB so that chromadb gives relevant responses
    def inject_vector_data_to_chromaDB(self):
        """Inject the prepared data into ChromaDB.
        Raises an error if the collection_name already exists in ChromaDB.
        The method prints a confirmation message upon successful data injection."""
        chroma_file_dir=self.app_configuration.chroma_client              #chroma_file_dir=data\chroma
        rag_file_dir=self.app_configuration.collection_name               #rag_file_dir="titanic.csv"
        connection=chroma_file_dir.get_or_create_collection(name=rag_file_dir)   #connection=data\chroma\titanic_small.csv
        connection.add(
            documents=self.docs,
            embeddings=self.embeddings,
            metadatas=self.metadatas,
            ids=self.ids
        )
        print("==============================================")
        print("Vector Data Injection in ChromaDB is Successful")

    def validate_DB(self):
        """Validate the contents of the database to ensure that the data injection has been successful.
            Prints the number of vectors in the ChromaDB collection for confirmation."""
        vectordb=self.app_configuration.chroma_client.get_collection(name=self.app_configuration.collection_name)
        print("------------------------------------------------------")
        print("Number of vectors in the ChromaDB collection is: ",vectordb.count())
        print("--------------------------------------------------------------------------")

    def run_pipeline(self):
        """Execute the entire pipeline for preparing the database from the CSV.
           This includes loading the data, preparing the data for injection, injecting the data into ChromaDB, and validating the existence of the injected data."""
        self.df, self.file_name =self.create_dataframe(file_dir=self.file_directory)
        self.docs,self.embeddings,self.metadatas, self.ids=self.convert_text_into_vector(df=self.df,file_name=self.file_name)
        self.inject_vector_data_to_chromaDB()
        self.validate_DB()


