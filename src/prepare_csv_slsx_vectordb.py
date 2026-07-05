import os
import pandas as pd

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()

print(os.getenv("OPENAI_API_KEY"))

#folder_name where the csv files are located
folder_path="data/for_upload"
#final_file name
db_path="data/csv_xlsx_vectordb"

#create a text_store box
text_storage=[]

#the file will iterate in the folder and extract each csv file
for file in os.listdir(folder_path):
    file_path=os.path.join(folder_path,file)

    if file.endswith(".csv"):
        df= pd.read_csv(file_path)

    elif file.endswith(".xlsx"):
        df= pd.read_excel(file_path)

    else:
        continue

    table_to_text=df.to_string(index=False)    #convert the dataframe to plain text format
    text_storage.append(table_to_text)         #store the plain text in a box

combined_text="\n".join(text_storage)      #this removes the gap between each text

#a splitter machine that solit the text chunk wise
splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

#create a document from the combined text after splitting.Each document has 500 words
docs=splitter.create_documents([combined_text])
#create embedding to convert text into vector
embeddings=HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
#convert text into vector and store FAISS
vector_db=FAISS.from_documents(docs,embeddings)
#save it into local folder
vector_db.save_local(db_path)

print("Vector Database Creation has been completed")



