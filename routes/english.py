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

router = APIRouter()
router = APIRouter(prefix="/english", tags=["english"])
templates = Jinja2Templates(directory="templates")


messages = [
    ("You", "I am your personal document assistant"),
]

filenames = []


@router.get("/input/textarea", response_class=HTMLResponse)
async def render_textarea_template(request: Request):
    return templates.TemplateResponse(
        "en-form-textarea.html",
        {"request": request, "result": None},
    )


@router.get("/input/file", response_class=HTMLResponse)
async def render_file_template(request: Request):
    return templates.TemplateResponse(
        "en-form-file.html",
        {"request": request, "result": None, "messages": messages},
    )


@router.post("/summary/textarea", response_class=HTMLResponse)
async def summary_en_textarea(request: Request):
    form_data = await request.form()
    input_text = form_data["input_text"]
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=5000, chunk_overlap=500
    )

    llm = get_llm(openai_api_key=openai_api_key)

    docs = text_splitter.create_documents([input_text])

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        verbose=False,  # Set verbose=True if you want to see the prompts being used
    )

    result = summary_chain.run(docs)

    return templates.TemplateResponse(
        "en-form-textarea.html",
        {"request": request, "result": result},
    )


@router.post("/summary/file", response_class=HTMLResponse)
async def summary_en_file(request: Request, file: UploadFile = File(...)):
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

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "\t"], chunk_size=1000, chunk_overlap=0
    )

    docs = text_splitter.create_documents([input_text])

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # vectors = embeddings.embed_documents([x.page_content for x in docs])

    db = FAISS.from_documents(docs, embeddings)

    db.save_local("faiss_index")

    llm = get_llm(openai_api_key=openai_api_key)

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        verbose=False,  # Set verbose=True if you want to see the prompts being used
    )

    result = summary_chain.run(docs)

    folder_path = "results"
    result_file_path = f"results/{file.filename}.txt"

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    filenames.append(result_file_path)

    with open(result_file_path, "w") as f:
        f.write(result)

    return templates.TemplateResponse(
        "en-form-file.html",
        {"request": request, "result": result, "messages": messages},
    )


@router.post("/chat/file", response_class=HTMLResponse)
async def chat_en_file(request: Request):
    form_data = await request.form()

    query = form_data["message"]

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    new_db = FAISS.load_local("faiss_index", embeddings)

    docs = new_db.similarity_search(query)

    llm = get_llm(openai_api_key=openai_api_key)

    chain = load_qa_chain(llm, chain_type="stuff")

    response = chain.run(input_documents=docs, question=query)

    with open(filenames[-1], "r") as f:
        result = f.read()

    messages.append(("You", f"{query}"))
    messages.append(("Bot", f"{response}"))

    return templates.TemplateResponse(
        "en-form-file.html",
        {"request": request, "result": result, "messages": messages},
    )
