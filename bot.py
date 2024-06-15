import streamlit as st
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Set the environment variable for OpenAI API key
os.environ["OPENAI_API_KEY"] = ""

# Constants
CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context , the context is a mix of both English and roman Urdu:

{context}

---

Answer the question based on the above context: {question}
"""
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
        color: black;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .st-title {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize the embeddings and vector store
embedding_function = OpenAIEmbeddings()
db = Chroma(persist_directory='chroma/final', embedding_function=embedding_function)
retriever = db.as_retriever()

# Initialize the language model
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.1)

# Streamlit app layout
st.title(':grey[r/lums AI version 🗿]')

st.write("The bot has been fed data from r/lums sub reddit currenlty and would answer based on contextual information ;))")

query_text = st.text_input("pocho sawaal!")

if query_text:
    # Retrieve context from the database
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Format the prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Get response from the language model
    response_text = llm.invoke(prompt)

    # Display the results
    st.write("According to reddit:")
    st.write(response_text.content)



