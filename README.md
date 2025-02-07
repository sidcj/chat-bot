#🚀 Brainlox Course QA Chatbot

This repository contains a Flask-based chatbot that uses LangChain to extract course information from Brainlox. It processes the data using embeddings, stores it in a vector database (FAISS), and provides a RESTful API for answering questions.

#📌 Features

Scrapes course data from Brainlox using LangChain's WebBaseLoader.

Splits data into smaller chunks for efficient retrieval.

Generates embeddings using the Ollama model (gemma).

Stores embeddings in a FAISS vector database for quick access.

Provides a Flask REST API to handle user queries.

#🛠 Installation & Setup

🔹 Prerequisites

Make sure you have:

Python 3.8+ installed

pip installed

A working internet connection

🔹 Clone the Repository

git clone https://github.com/yourusername/brainlox-chatbot.git
cd brainlox-chatbot

🔹 Install Dependencies

pip install -r requirements.txt

#🚀 Running the Chatbot

Step 1: Set Up Environment Variables

Create a .env file in the project root and add the following:

FLASK_APP=app.py
FLASK_ENV=development

Step 2: Start the API Server

python app.py

The server will start at http://localhost:5000.

📡 API Endpoints

#1️⃣ Welcome Page

GET / → Returns a simple welcome message.

curl http://localhost:5000/

Response:

"Brainlox Course QA API - Ask questions via URL: /ask/your_question_here"

#2️⃣ Ask a Question

GET /ask/{question} → Queries the chatbot with a question.

curl http://localhost:5000/ask/What%20courses%20are%20available?

Response:

{
  "question": "What courses are available?",
  "answer": "Brainlox offers multiple technical courses including Python, AI, and Web Development.",
  "sources": ["https://brainlox.com/courses/category/technical"]
}

POST /ask → Accepts a question in JSON format.

curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d '{"question": "Tell me about Python courses"}'


