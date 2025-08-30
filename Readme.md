DevOps RAG Chatbot
A Streamlit-powered conversational chatbot providing expert answers about DevOps, Kubernetes, Helm, Ansible, and related practices. Powered by Retrieval-Augmented Generation (RAG) and Google Gemini, it can answer both general and document-based queries with a friendly UI.

Table of Contents
Features

Project Structure

Setup & Installation

Configuration

Usage

Troubleshooting

License

Features
Beautiful Streamlit UI with dark/light mode toggle

Instant DevOps Q&A with RAG document retrieval

Conversational memory (Chat history)

Expert support for Kubernetes, Helm, Ansible, and more

Avatar icons, animated chat bubbles, markdown/code rendering

Cloud-friendly (Streamlit Cloud)

Project Structure
text
devops-rag-chatbot/
├── app.py                ← Main Streamlit application
├── requirements.txt      ← Python dependencies
├── src/
│   ├── loader.py         ← Document loaders (PDF, etc.)
│   ├── splitter.py       ← Document chunking
│   ├── vectorstore.py    ← Vector store construction
│   ├── rag_chain.py      ← RAG logic and chains
│   └── followup.py       ← History-aware chains
├── data/
│   └── devops.pdf        ← Source documents (optional)


Setup & Installation

Clone the repository:

git clone https://github.com/your-username/devops-rag-chatbot.git
cd devops-rag-chatbot
Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate   # On Windows: .\venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt


Configuration
API Keys:
Store your Google Gemini API key securely. On Streamlit Cloud, set secrets in your dashboard:
GOOGLE_API_KEY = "your_api_key"


Locally, use a .env file:
GOOGLE_API_KEY=your_api_key
Documents:

Place source PDFs (e.g., devops.pdf) under the data/ folder.

Make sure file paths in app.py match your repo structure.

Usage
Run locally:
streamlit run app.py
On Streamlit Cloud:

Push to GitHub

Deploy from your repo using Streamlit Cloud

Troubleshooting
Missing dependencies:
Ensure all required packages are in requirements.txt.

Quota errors:
Check your API plan or wait for daily quota reset.

PDF file not found:
Confirm data/devops.pdf is present and referenced with the correct path.

Chroma/SQLite errors:
Remove persist_directory or switch to in-memory/hosted vector storage for cloud deployments.

License
This project is licensed under the MIT License.
Feel free to use, modify, and share as needed.

Credits
Made by Rudra Tyagi.
Powered by Google Gemini, LangChain, and Streamlit.

