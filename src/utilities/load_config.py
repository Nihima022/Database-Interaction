import os

import yaml
#It is used to store configuration(full configuration has been already stored in app_config.yml)

import shutil
#it is used for manipulate files like copy delete extract and all

import dotenv

from dotenv import load_dotenv

load_dotenv()

#used to create path directory and find the exact location of file
try:
    from pyprojroot import here
    #pyprojroot acts like GPS of the file. It easily finds the main folder of any file using here() function
except Exception:
    #this is backup code.it is used when the system fail to work with pyprojroot
    from pathlib import Path
    def here(p=" "):
        root= Path(__file__).resolve().parents[0]
        print(root)
        if p:
            return root/p
        else:
            return root
        #here without any p="config/app_config.yml" the output will be the root directory "D:\ostad\AI Agent Development\Database interaction"

#used to generate response using gpt from Azure OpenAI Services
try:
    from openai import AzureOpenAI
    #it allows python to communicate with Azure OpenAI Service to generate answers using GPT models
except Exception:
    AzureOpenAI = None

#used to generate response using gpt with langchain from Azure OpenAI Service. langchain added tools,RAG,agents to the prompt and make the prompt AI-friendly
try:
    from langchain.chat_models import AzureChatOpenAI
except Exception:
    try:
        from langchain_openai import AzureChatOpenAI
    except Exception:
        AzureChatOpenAI = None

#used to generate response based on meaning from vector database, instead of searching from large row column based files
try:
    import chromadb
except Exception:
    chromadb = None

class LoadConfig:
    def __init__(self) -> None:
        with open(here("config/app_config.yml")) as configure:
            app_configuration= yaml.load(configure, Loader=yaml.FullLoader) #converts the yaml text to python code

            self.load_directories(app_config=app_configuration)
            self.load_llm_config(app_config=app_configuration)
            self.load_rag_config(app_config=app_configuration)
            self.load_chroma_client()                         #it doesnt require app_config cause it use data already stored in the object, such as:

    def load_directories(self,app_config):
        self.stored_csv_xlsx_directory = here(app_config["directories"]["stored_csv_xlsx_directory"])
        self.stored_csv_xlsx_sqldb_directory = str(here(app_config["directories"]["stored_csv_xlsx_sqldb_directory"]))
        self.stored_csv_xlsx_vectordb_directory = str(here(app_config["directories"]["stored_csv_xlsx_vectordb_directory"]))
        self.for_upload_directory = str(here(app_config["directories"]["for_upload_directory"]))
        self.stored_sqldb_directory=str(here(app_config["directories"]["stored_sqldb_directory"]))
        self.stored_chinook_sqlite_directory=str(here(app_config["directories"]["stored_chinook_sqlite_directory"]))
        self.persist_directory=str(here(app_config["directories"]["persist_directory"]))

    def load_llm_config(self, app_config):
        self.agent_llm_system_role=app_config["llm_config"]["agent_llm_system_role"]
        self.rag_llm_system_role=app_config["llm_config"]["rag_llm_system_role"]
        self.model_name=os.getenv("MODEL_NAME")
        self.embedding_model_name=os.getenv("EMBEDDING_MODEL")
        self.temperature=app_config["llm_config"]["temperature"]

    def load_rag_config(self, app_config):
        self.collection_name=app_config["rag_config"]["collection_name"]
        self.top_k=app_config["rag_config"]["top_k"]

    def load_chroma_client(self):
        if chromadb is None:
            print("Chromadb has not been installed")
            self.chroma_client=None
            return

        self.chroma_client=chromadb.PersistentClient(
            path=str(here(self.persist_directory))
        )

    def remove_directory(self,directory_path:str):
        """
        Removes the specified directory.

        Parameters:
            directory_path (str): The path of the directory to be removed.

        Raises:
            OSError: If an error occurs during the directory removal process.

        Returns:
            None
        """
        if os.path.exists(directory_path):
            try:
                shutil.rmtree(directory_path)
                print(f"The file {directory_path} has been removed!")
            except OSError as e:
                print(f"An Error Occurred:{e}")
        else:
            print(f"The file {directory_path} does not exist!")








