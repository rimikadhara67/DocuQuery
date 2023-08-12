from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"


app = Flask(__name__)

# Configure the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'user_files')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Store the docsearch and chain as global variables
docsearch = None
chain = None

from flask import render_template  # add this to your imports

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    global docsearch, chain
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Read the file
        reader = PdfReader(file)
        raw_text = ''
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                raw_text += text

        # Split the text
        text_spliter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_spliter.split_text(raw_text)

        # Generate embeddings
        embeddings = OpenAIEmbeddings()
        docsearch = FAISS.from_texts(texts, embeddings)

        # Load the question-answering chain
        chain = load_qa_chain(OpenAI(), chain_type="stuff")

        return jsonify({'message': 'File successfully uploaded'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/ask_question', methods=['POST'])
def ask_question():
    global docsearch, chain
    if docsearch is None or chain is None:
        return jsonify({'error': 'No document loaded'}), 400
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Query the document
    docs = docsearch.similarity_search(question)

    # Get the answer
    try:
        answer = chain.run(input_documents=docs, question=question)
    except Exception as e:
        print(f"Exception while running chain: {e}")
        return jsonify({'error': 'Error while finding answer'}), 500

    return jsonify({'answer': answer}), 200

if __name__ == '__main__':
    app.run(debug=True, port='8081')
