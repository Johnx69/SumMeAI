from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from routes import vietnamese
from routes import english
import os
import fastapi_jinja

app = FastAPI()


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")


# Include routers
app.include_router(vietnamese.router)
app.include_router(english.router)


@app.get("/health")
def read_root():
    """Root endpoint"""
    return {"Hello": "World"}


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    """Main endpoint"""
    return templates.TemplateResponse("index.html", context={"request": request})


@app.exception_handler(404)
async def custom_404_handler(request, __):
    """Custom 404 handler"""
    return templates.TemplateResponse("404.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
