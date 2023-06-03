from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langchain import OpenAI
from transformers import MT5ForConditionalGeneration, MT5Tokenizer


def get_file_extension(filename: str) -> str:
    """Get the file extension from the filename."""
    return filename.split(".")[-1]


def get_model(model_name):
    """
    Get the tokenizer and model based on the model name.

    Supported model names:
    - "vietai": vit5-large-vietnews-summarization
    - "anhdao": mt5_small_summarization
    """

    if model_name == "vietai":
        tokenizer = AutoTokenizer.from_pretrained(
            "VietAI/vit5-large-vietnews-summarization"
        )
        model = AutoModelForSeq2SeqLM.from_pretrained(
            "VietAI/vit5-large-vietnews-summarization"
        )

    if model_name == "anhdao":
        model = MT5ForConditionalGeneration.from_pretrained(
            "Johnx69/mt5_small_summarization"
        )
        tokenizer = MT5Tokenizer.from_pretrained("Johnx69/mt5_small_summarization")

    return tokenizer, model


def generate_summary(input_text, model_name):
    """
    Generate a summary for the input text using the specified model.

    Args:
    - input_text: The input text to summarize.
    - model_name: The name of the model to use for summarization.

    Returns:
    - The generated summary.
    """

    tokenizer, model = get_model(model_name)

    input_text = "vietnews: " + input_text + " </s>"
    encoding = tokenizer(input_text, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"].to("cpu"), encoding[
        "attention_mask"
    ].to("cpu")
    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_masks,
        max_length=256,
        early_stopping=True,
    )
    for output in outputs:
        line = tokenizer.decode(
            output, skip_special_tokens=True, clean_up_tokenization_spaces=True
        )

    return line


def get_llm(openai_api_key, temperature=0):
    """
    Get the Language Model from OpenAI.

    Args:
    - openai_api_key: The OpenAI API key.
    - temperature: The temperature parameter for text generation (default: 0).

    Returns:
    - The Language Model.
    """
    llm = OpenAI(temperature=temperature, openai_api_key=openai_api_key)
    return llm
