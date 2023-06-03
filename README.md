# SumMeAI - Text Summarization and Document Analysis

<img src = "static/images/logo/summeai.png"/>

## I. Introduction 🌟
SumMeAI is a powerful application designed to simplify the process of text summarization and document analysis. With support for both Vietnamese and English texts, this application allows users to extract key information from a given text or uploaded files in various formats such as TXT and PDF.

## II. Features 🔧

### 1. Text Summarization 📝 ✂️
- SumMeAI utilizes advanced natural language processing techniques to generate concise summaries of lengthy texts. By extracting the most important sentences and preserving the context, users can quickly grasp the main ideas and key points of any document.
 
### 2. Multilingual Support 🌍 🔤
- SumMeAI supports both Vietnamese and English texts, enabling users to summarize documents written in either language. This makes the application versatile and accessible to a wider user base.

### 3. File Upload 📂 ⬆️
- Users can easily upload TXT or PDF files directly into SumMeAI for summarization and analysis. Whether it's a research paper, an article, or a report, the application efficiently processes the content and provides valuable insights in a matter of seconds.

### 4. Virtual Assistant 💬 💡
- SumMeAI goes beyond text summarization by offering a virtual assistant that can answer questions related to the uploaded documents. Users can interact with the assistant and gain further understanding of the content, enabling a more comprehensive analysis.

## III. Technical Overview 🔬
<p align="center">
  <a href="https://en.wikipedia.org/wiki/HTML" target="_blank" rel="noreferrer">
    <img src="https://www.vectorlogo.zone/logos/w3_html5/w3_html5-icon.svg" alt="HTML" width="100" height="100"/>
  </a>
  <a href="https://en.wikipedia.org/wiki/CSS" target="_blank" rel="noreferrer">
    <img src="https://www.vectorlogo.zone/logos/w3_css/w3_css-icon.svg" alt="CSS" width="100" height="100"/>
  </a>
  <a href="https://getbootstrap.com/" target="_blank" rel="noreferrer">
    <img src="https://www.vectorlogo.zone/logos/getbootstrap/getbootstrap-ar21.svg" alt="Bootstrap" width="150" height="100"/>
  </a>
  <a href="https://pytorch.org/" target="_blank" rel="noreferrer">
    <img src="https://www.vectorlogo.zone/logos/pytorch/pytorch-icon.svg" alt="pytorch" width="100" height="100"/>
  </a>
  <a href="https://fastapi.tiangolo.com/" target="_blank" rel="noreferrer">
    <img src="https://cdn.worldvectorlogo.com/logos/fastapi.svg" alt="fastapi" width="100" height="100"/>
  </a>
  <a href="https://huggingface.co/" target="_blank" rel="noreferrer">
    <img src="static/images/readme/Huggingface.png" alt="huggingface" width="150" height="100"/>
  </a>
  <a href="https://python.langchain.com/en/latest/index.html" target="_blank" rel="noreferrer">
    <img src="static/images/readme/Langchain.png" alt="langchain" width="150" height="150"/>
  </a>
  <a href="https://openai.com/" target="_blank" rel="noreferrer">
    <img src="static/images/readme/Openai.png" alt="openai" width="100" height="100"/>
  </a>
</p>

### 1. Vietnamese Summarization 🇻🇳 📝

#### Language Models 🔤 🤖

For Vietnamese text summarization, SumMeAI supports two models:

- 1. **Vietai Pretrained T5-vit Large Model** (Hugging Hub): This model has been pretrained and fine-tuned specifically for Vietnamese text summarization tasks. It leverages the power of the **T5-vit** architecture to generate high-quality summaries.

- 2. **MT5-small Model** (Custom Trained): This model is trained on a Vietnamese news dataset for 7 hours using **Google Colab** and the **Hugging Face** library. It provides an alternative option for users who prefer a custom-trained model.

#### File Upload and Processing 📂 💻

- SumMeAI allows users to upload TXT or PDF files for summarization. The application handles the file upload process, extracting the text content from the uploaded files. It utilizes appropriate libraries to parse and extract the required text, ensuring compatibility with both Vietnamese and English documents.


### 2. English Summarization 🇬🇧 📝

#### Language Models 🔤 🤖

For English text summarization, SumMeAI utilizes the **OpenAI API** and **Langchain** library, which is renowned for its ability to generate accurate and coherent summaries. Users can enter English text directly into the application or upload TXT/PDF files for summarization and chat with a virtual assistant to know more about their document. 

#### English Virtual Assistant 💬 🤖

- The English feature also includes a virtual assistant powered by the **Langchain library** and **Faiss vector database**. This enables users to ask questions about their uploaded English documents, enhancing their understanding of the content. The virtual assistant utilizes natural language processing techniques to provide conversational responses based on the document's context.

#### File Upload and Processing 📂 💻

- SumMeAI allows users to upload TXT or PDF files for summarization. The application handles the file upload process, extracting the text content from the uploaded files. It utilizes appropriate libraries to parse and extract the required text, ensuring compatibility with both Vietnamese and English documents.


### 3. User Interface and Interaction 💻 🤝

- SumMeAI provides a user-friendly web-based interface for users to interact with the application. The interface is built using **Jinja2 templates**, **FastAPI**, and **Bootstrap**, providing a responsive and intuitive design. Users can enter text directly into the textarea or upload files for summarization. The summarization results are displayed in an easily readable format.

## IV. How to Install 📥

1. Open Terminal and clone this repository:

```bash
git clone https://github.com/Johnx69/SumMeAI.git
```

2. In the `.env` file, add your personal OpenAI key in this website `https://platform.openai.com/account/api-keys`

```.env
OPENAI_KEY=
```

3. Change the current directory to SumMeAI

```bash
cd SumMeAI
```

4. Open Docker and run the following command line

```
docker build -t summeai .
```

5. Run the application with this command line

```bash
docker run -p 8000:8000 -d summeai
```

6. Access the application in your web browser at `http://localhost:8000`.

## V. Usage 📝

1. Open the SumMeAI application in your web browser.

2. Enter text directly into the textarea for summarization, or click on the file upload button to upload a TXT or PDF file.

3. For Vietnamese text summarization, select the desired model from the options available. For English text summarization, the application will automatically use the OpenAI API.

4. Click on the "Submit" button to generate a summary of the text or uploaded document.

5. The summarization results will be displayed on the screen. You can scroll through the summary to quickly grasp the key points of the document.

6. If you have uploaded an English document, you can also interact with the virtual assistant by asking questions about the content. The virtual assistant will provide conversational responses based on the context of the document.

## VI. Contributing 🤝

Contributions to SumMeAI are welcome! If you find any issues or have suggestions for improvements, please feel free to submit a pull request or open an issue on the GitHub repository.

## VII. License ⚖️

SumMeAI is licensed under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute this software as per the terms of this license.

