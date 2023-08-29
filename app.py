# Import necessary libraries
import streamlit as st
from utils import extract_text_from_pdf, summarize, chunk_text


def main():
    st.title("Summarizer")
    st.header("Upload a PDF and get a summary of it in seconds!")

    # allow user to put in user_prompt, system_prompt, and document_prompt
    user_prompt = st.text_input("What would you like to ask the system?")
    system_prompt = st.text_input("What would you like the system to say?")
    model = st.selectbox("Select a model", ["gpt-4"])

    # Create a file uploader widget
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        # allow user to choose a range of pages to summarize instead of all PDF pages
        page_range = st.text_input(
            "Enter the range of pages to summarize (e.g., '1-5'). Leave blank for all pages."
        )

        if st.button("Summarize"):
            # Use utility function to extract text from PDF
            pdf_text = extract_text_from_pdf(uploaded_file, page_range)

            # chunk pdf_text using utility function
            pdf_chunks = chunk_text(pdf_text)
            print(pdf_chunks)

            # Use utility function to generate summary in markdown format
            summary = ""
            for chunk in pdf_chunks:
                summary += summarize(chunk, user_prompt, system_prompt, model)

            # summary = summarize(pdf_text, user_prompt, system_prompt, model)

            # Display the summary
            st.markdown(summary)


# Run the main function to start the Streamlit app
if __name__ == "__main__":
    main()
