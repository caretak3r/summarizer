# Import the necessary libraries
import openai
import pdfplumber
import os
import tiktoken

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_text_from_pdf(pdf_file, page_range) -> str:
    """
    Function to extract text from a PDF file using pdfplumber
    """
    # Parse the page range
    if page_range:
        start_page, end_page = map(int, page_range.split("-"))
    else:
        start_page, end_page = None, None

    try:
        # Open the PDF file
        with pdfplumber.open(pdf_file) as pdf:
            # Initialize an empty string for the text
            text = ""

            # Iterate over the pages within the range if specified, else all pages
            for page in (
                pdf.pages[start_page - 1 : end_page]
                if start_page and end_page
                else pdf.pages
            ):
                # for page in pdf.pages:
                # Extract the text from the page and add it to the text string
                text += page.extract_text()
    except Exception as e:
        print(f"Error occured: {e}")
        text = ""

    return text


def chunk_text(text, max_tokens=8000) -> list:
    chunk_count = 0
    chunks_log = []

    while text:
        chunk = " ".join(text.split()[:max_tokens])

        encoding = tiktoken.get_encoding("cl100k_base")
        token_count = len(encoding.encode(chunk))

        # reduce
        while token_count > max_tokens:
            chunk = " ".join(chunk.split()[:-1])
            token_count = len(encoding.encode(chunk))

        text = " ".join(text.split()[len(chunk.split()) :])
        chunk_count += 1

        chunk_data = {
            "chunk_count": chunk_count,
            "word_count": len(chunk.split()),
            "token_count": token_count,
        }
        chunks_log.append(chunk_data)
    return chunks_log


def summarize(document_prompt, user_prompt, system_prompt, model, temp=0.7) -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": document_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temp,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        output_summary = response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error occurred: {e}")
        output_summary = ""
    return output_summary
