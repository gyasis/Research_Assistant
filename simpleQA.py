from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import os
import dis
# Import the API-Key from the config file
# from ..config import API_KEY

from config import API_KEY

os.environ["OPENAI_API_KEY"] = API_KEY

parent_directory = os.path.join(os.getcwd())
data_folder = os.path.join(parent_directory, 'data')
file_folder = os.path.join(parent_directory, 'uploads')
embeddings = OpenAIEmbeddings()
persist_directory = os.path.join(data_folder, 'residency')
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
retriever = vectordb.as_retriever()
import textwrap
from langchain.chains import ConversationalRetrievalChain

from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), retriever, chain_type='map-rerank', memory=memory)

while True:
    # Get the Question
    user_question = input("Enter a question: ")
    
    if user_question == "exit":
        break
    answer=qa.run(user_question)

    
    import textwrap
    wrapper = textwrap.TextWrapper(width=50)  
    # Set the maximum width for a line
  
    
    wrapped_page_content = wrapper.fill(text=answer)
    print(wrapped_page_content)
    
    