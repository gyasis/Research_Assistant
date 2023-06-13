# %%
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain 
from langchain.document_loaders import UnstructuredFileLoader, DirectoryLoader
from langchain.text_splitter import TokenTextSplitter
from pathlib import Path
from dotenv import load_dotenv

def process_documents(subfolder: str):
    """
    Process documents and persist.

    :param subfolder: The name of the subfolder in the uploads directory
    """
    # Load .env file
    load_dotenv('api_key.env')
    # Set API key
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    # Define data_folder and file_folder
    data_folder = os.path.join(os.getcwd(), 'data')
    file_folder = os.path.join(os.getcwd(), 'uploads', subfolder)
    
    data_folder = Path(data_folder).resolve()
    file_folder = Path(file_folder).resolve()

    persist_directory = os.path.join(data_folder, subfolder)

    # This is a processing step and assumes that folders and files need to be processed and created.
    embeddings = OpenAIEmbeddings()
    loader = DirectoryLoader(str(file_folder),loader_cls=UnstructuredFileLoader)
    documents = loader.load()
    
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    
    db = Chroma.from_documents(docs, embeddings, persist_directory=str(persist_directory))
    db.persist()
    
    
process_documents("blockchain")
# %%
