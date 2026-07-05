import os

import yaml
#It is used to store configuration(full configuration has been already stored in app_config.yml)

import shutil
#it is used for manipulate files like copy delete extract and all

import dotenv

from dotenv import load_dotenv

#used to create path directory and find the exact location of file
try:
    from pyprojroot import here
    #pyprojroot acts like GPS of the file. It easily finds the main folder of any file using here() function
except Exception:
    #this is backup code..it is used when the system fail to work with pyprojroot
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

class Load_Config:
    def __init__(self) -> None:
        with open(here("config/app_config.yml")) as configure:
            app_configuration= yaml.load(configure, Loader=yaml.FullLoader)

x=Load_Config()
print(x)
