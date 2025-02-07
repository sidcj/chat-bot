from flask import Flask, request, jsonify
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv

# Set user agent for web requests
os.environ["USER_AGENT"] = "BrainloxQA/1.0 (contact@yourdomain.com)"

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

def initialize_components():
    def prepare_website_data(url):
        loader = WebBaseLoader(url)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

        embeddings = OllamaEmbeddings(model="gemma")
        vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
        return vectorstore.as_retriever()

    retriever = prepare_website_data("https://brainlox.com/courses/category/technical")
    llm = Ollama(model="gemma")

    template = """Answer using only this context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    return (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    ), retriever

chain, retriever = initialize_components()

@app.route('/')
def home():
    return "Brainlox Course QA API - Ask questions via URL: /ask/your_question_here"

@app.route('/ask', methods=['GET'])
def handle_empty_question():
    return jsonify({"error": "No question provided. Use /ask/your_question_here"}), 400

@app.route('/ask/<path:question>', methods=['GET'])
def ask_question(question):
    try:
        if not question.strip():
            return jsonify({"error": "Empty question provided"}), 400

        answer = chain.invoke(question)
        docs = retriever.invoke(question)
        sources = list(set([doc.metadata['source'] for doc in docs[:3]]))

        return jsonify({
            "question": question,
            "answer": answer,
            "sources": sources
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)