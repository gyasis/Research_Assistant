
# %%
from flask import Flask, render_template, request, jsonify, g
from flask_socketio import SocketIO
import logging
import os
import re
from langchain import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain 
from langchain.document_loaders import UnstructuredFileLoader, DirectoryLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.memory import ConversationTokenBufferMemory
from flask_socketio import SocketIO, emit
from pathlib import Path
import os
import sqlite3
import pickle


# Set your API key
# REMEMBER TO REMOVE THIS CODE AND SET AND ENVIRONMENT VARIABLE
os.environ["OPENAI_API_KEY"] = "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"
 # %%
app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

class SocketIOStream:
    def write(self, data):
        pattern1 = r'jinja2.exceptions.TemplateNotFound: \w+.html'
        pattern2 = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        if re.search(pattern1, data) or re.search(pattern2, data):
            socketio.emit('output', data)

    def flush(self):
        pass

class DatabaseManager:
    conn = None
    cursor = None

    def __init__(self, db_name, db_dir='dump'):
        if DatabaseManager.conn is None:
            os.makedirs(db_dir, exist_ok=True)  # create directory if it doesn't exist
            db_path = os.path.join(db_dir, db_name)
            DatabaseManager.conn = sqlite3.connect(db_path)
            
            # Disable auto-vacuum
            DatabaseManager.conn.execute("PRAGMA auto_vacuum = 0")
            
            DatabaseManager.cursor = DatabaseManager.conn.cursor()
            self.create_table()

    def create_table(self):
        DatabaseManager.cursor.execute('''CREATE TABLE IF NOT EXISTS my_table
                               (name TEXT, object BLOB)''')

    def insert_data(self, name, obj):
        # Serialize the object
        obj_pickle = pickle.dumps(obj)

        DatabaseManager.cursor.execute("DELETE FROM my_table WHERE name=?", (name,))
        DatabaseManager.cursor.execute("INSERT INTO my_table VALUES (?, ?)", (name, obj_pickle))
        DatabaseManager.conn.commit()

    def get_data(self, name):
        DatabaseManager.cursor.execute("SELECT object FROM my_table WHERE name=?", (name,))
        data = DatabaseManager.cursor.fetchone()

        if data is not None:
            # Deserialize the object
            data = pickle.loads(data[0])
        return data

    def close_connection(self):
        if DatabaseManager.conn is not None:
            DatabaseManager.conn.close()
            DatabaseManager.conn = None
            DatabaseManager.cursor = None

        
logger = logging.getLogger('werkzeug')  # Use the Werkzeug logger
logger.setLevel(logging.INFO)  # Set logger level to INFO
stream_handler = logging.StreamHandler(SocketIOStream())
logger.addHandler(stream_handler)
# %%
# GLOBAL VARIABLE File Directory
llm = OpenAI()
memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=250)

# Create a DatabaseManager object
db = DatabaseManager('my_database.db')

# Store the objects in the database
db.insert_data('llm', llm)
db.insert_data('memory', memory)

# Close the database connection
db.close_connection()

template = """
        I want you to act as a research expert in your field that can understand research papers and answer questions about them. If possible also give instances where there are research gaps.  
        Here is the question: "{user_question}"
        Here is the History of the conversation: {memory}
        Use numbered list and new lines if needed to organize data, if the user asks for a list, or you have more than one concept, in a clear format. Give clear and concise answers with a good balance between formal scientific and conversational structure. If I ask you to cite sources try to do so AMA style.
        """



#This should always be the default step regardless of resuming session or starting a new one
parent_directory = os.path.join(os.getcwd(), '..')
data_folder = os.path.join(parent_directory, 'data')
file_folder = os.path.join(parent_directory, 'uploads')
embeddings = OpenAIEmbeddings()
persist_directory = os.path.join(data_folder, 'multiple')
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
retriever = vectordb.as_retriever()
# %%

@app.route('/')
def home():
    directories = ['../data/multiple']  # replace with your actual directories
    files_exist = any(os.listdir(dir) for dir in directories if os.path.isdir(dir))
    if files_exist:
        app.logger.info('Files exist in the directories.')
    else:
        app.logger.info('No files exist in the directories.')
    return render_template('index.html', files_exist=files_exist)


@app.before_request
def before_request():
    if request.path == '/chat':
        # Create the objects once when the chat route is accessed
        print("starting objects")
        # llm = OpenAI()
        # memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=250)

        


@app.route('/chat', methods=['GET'])
def chat_page():
    return render_template('chat.html')


@app.route('/chat_message', methods=['POST'])
def chat_message():
    # Create a DatabaseManager object
    db = DatabaseManager('my_database.db')

    # Retrieve the objects from the database
    llm = db.get_data('llm')
    memory = db.get_data('memory')
    print("this is the memory")
    print(memory)
    print("this is the memory variables")
    print(memory.load_memory_variables({}))
    data = request.get_json()
    user_question = data['message'] 
    prompt = PromptTemplate(input_variables= ["user_question","memory"], template=template)
   
    
    # Use the existing objects to process the message
    prompt_output = prompt.format(user_question=user_question, memory=memory.load_memory_variables({}))
   
    chain = RetrievalQAWithSourcesChain.from_chain_type(OpenAI(temperature=0), chain_type="map_reduce", retriever=retriever)
    answer = chain({"question": prompt_output},   return_only_outputs=False)
    
    
    
    answer = answer['answer']
   
    memory.save_context({"input":user_question},{"output": answer})
    print(memory)
    print(memory.load_memory_variables({}))
    # Store the updated memory object back into the database
    db.insert_data('memory', memory)

    # Close the database connection
    db.close_connection()

    return jsonify({'answer': answer})

@app.route('/download_transcript', methods=['POST'])
def download_transcript_route():
    data = request.get_json()
    video_url = data['video_url']
    save_to_db = data.get('save_to_db', False)  # Default to False if not provided

    transcript = download_transcript(video_url)

    # If save_to_db is True, store the transcript into the database:
    if save_to_db:
        db = DatabaseManager('my_database.db')
        db.insert_data('transcript', transcript)
        db.close_connection()

    return jsonify({'transcript': transcript})


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5051)
