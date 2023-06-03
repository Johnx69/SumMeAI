from fastapi import APIRouter, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PyPDF2 import PdfReader


from utils.utils import get_file_extension, generate_summary, get_model
from utils.constants import ALLOWED_EXTENSIONS

# Create an instance of the APIRouter
router = APIRouter(prefix="/vietnamese", tags=["vietnamese"])
templates = Jinja2Templates(directory="templates")

# Mount the static files directory
router.mount("/static", StaticFiles(directory="static"), name="static")


# Route to render the template for the text area input form
@router.get("/input/textarea", response_class=HTMLResponse)
async def render_textarea_template(request: Request):
    return templates.TemplateResponse(
        "vi-form-textarea.html",
        {"request": request, "result": None},
    )


# Route to render the template for the file input form
@router.get("/input/file", response_class=HTMLResponse)
async def render_file_template(request: Request):
    return templates.TemplateResponse(
        "vi-form-file.html", {"request": request, "result": None}
    )


# Route to generate a summary for the input text from the textarea
@router.post("/summary/textarea", response_class=HTMLResponse)
async def summary_vi_textarea(request: Request):
    form_data = await request.form()
    input_text = form_data["input_text"]
    model_name = form_data["option"]

    # Generate the summary using the provided input text and model name
    result = generate_summary(input_text, model_name)

    return templates.TemplateResponse(
        "vi-form-textarea.html",
        {"request": request, "result": result, "model_name": model_name},
    )


# Route to generate a summary for the uploaded file
@router.post("/summary/file")
async def summary_vi_file(request: Request, file: UploadFile = File(...)):
    form_data = await request.form()
    model_name = form_data["option"]

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

    # Generate the summary using the provided input text and model names
    result = generate_summary(input_text, model_name)

    return templates.TemplateResponse(
        "vi-form-file.html", {"request": request, "result": result}
    )
