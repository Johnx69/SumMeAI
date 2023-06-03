from fastapi import APIRouter, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

from utils.utils import get_file_extension, get_llm
from utils.constants import ALLOWED_EXTENSIONS

import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv


load_dotenv()

openai_api_key = os.getenv("OPENAI_KEY")

# Create an instance of the APIRouter
router = APIRouter(prefix="/english", tags=["english"])
templates = Jinja2Templates(directory="templates")

# Define initial messages for the chat interface
messages = [
    (
        "Bot",
        "👋 Hello there! As your personal document assistant, I'm here to assist you with any document-related needs you may have. How can I help you today?",
    ),
]

# List to store filenames of generated result files
filenames = []


# Route to render the template for the text area input form
@router.get("/input/textarea", response_class=HTMLResponse)
async def render_textarea_template(request: Request):
    """
    Render the template for the text area input form.
    """
    return templates.TemplateResponse(
        "en-form-textarea.html",
        {"request": request, "result": None},
    )


# Route to render the template for the file input form
@router.get("/input/file", response_class=HTMLResponse)
async def render_file_template(request: Request):
    """
    Render the template for the file input form.
    """
    return templates.TemplateResponse(
        "en-form-file.html",
        {"request": request, "result": None, "messages": messages},
    )


# Route to generate a summary for the input text from the textarea
@router.post("/summary/textarea", response_class=HTMLResponse)
async def summary_en_textarea(request: Request):
    """
    Generate a summary for the input text from the textarea.
    """
    form_data = await request.form()
    input_text = form_data["input_text"]

    # Split the input text into chunks for processing
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=5000, chunk_overlap=500
    )

    # Get the language model for summarization
    llm = get_llm(openai_api_key=openai_api_key)

    # Create document objects from the input text
    docs = text_splitter.create_documents([input_text])

    # Load the summarization chain
    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        verbose=False,  # Set verbose=True if you want to see the prompts being used
    )

    # Generate the summary
    result = summary_chain.run(docs)

    return templates.TemplateResponse(
        "en-form-textarea.html",
        {"request": request, "result": result},
    )


# Route to generate a summary for the uploaded file
@router.post("/summary/file", response_class=HTMLResponse)
async def summary_en_file(request: Request, file: UploadFile = File(...)):
    """
    Generate a summary for the uploaded file.
    """
    file_extension = get_file_extension(file.filename)

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=404,
            detail="Invalid file type. Only TXT and PDF files are allowed.",
        )

    if file_extension == "pdf":
        # Read the PDF file and decode the content as UTF-8
        pdf_reader = PdfReader(file.file)
        input_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            input_text += page.extract_text()

        # Close the file
        file.file.close()

    if file_extension == "txt":
        contents = await file.read()
        input_text = contents.decode("utf-8")

    # Split the input text into chunks for processing
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "\t"], chunk_size=1000, chunk_overlap=0
    )

    # Create document objects from the input text
    docs = text_splitter.create_documents([input_text])

    # Get the embeddings for the documents
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # vectors = embeddings.embed_documents([x.page_content for x in docs])

    # Create a vector store for similarity search
    db = FAISS.from_documents(docs, embeddings)

    # Save the vector store locally
    db.save_local("faiss_index")

    # Get the language model for summarization
    llm = get_llm(openai_api_key=openai_api_key)

    # Load the summarization chain
    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        verbose=False,  # Set verbose=True if you want to see the prompts being used
    )

    # Generate the summary
    result = summary_chain.run(docs)

    # Create a folder to store the result files if it doesn't exist
    folder_path = "results"
    result_file_path = f"results/{file.filename}.txt"

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    # Store the result file path in the filenames list
    filenames.append(result_file_path)

    # Write the result to a file
    with open(result_file_path, "w") as f:
        f.write(result)

    return templates.TemplateResponse(
        "en-form-file.html",
        {"request": request, "result": result, "messages": messages},
    )


# Route to perform chat-based question answering on the uploaded file
@router.post("/chat/file", response_class=HTMLResponse)
async def chat_en_file(request: Request):
    """
    Perform a chat-based question answering on the uploaded file.
    """
    form_data = await request.form()

    query = form_data["message"]

    # Get the embeddings for similarity search
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Load the vector store for similarity search
    new_db = FAISS.load_local("faiss_index", embeddings)

    # Perform similarity search on the query
    docs = new_db.similarity_search(query)

    # Get the language model for question answering
    llm = get_llm(openai_api_key=openai_api_key)

    # Load the question answering chain
    chain = load_qa_chain(llm, chain_type="stuff")

    # Perform question answering on the input documents
    response = chain.run(input_documents=docs, question=query)

    # Read the content of the latest result file
    with open(filenames[-1], "r") as f:
        result = f.read()

    # Add the user query and bot response to the messages list
    messages.append(("You", f"{query}"))
    messages.append(("Bot", f"{response}"))

    return templates.TemplateResponse(
        "en-form-file.html",
        {"request": request, "result": result, "messages": messages},
    )
