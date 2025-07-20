# Text Summarizer Application

This project is a text summarizer application built using Streamlit and the OpenAI GPT-4o-mini model. It allows users to input text directly or upload documents (Word or PDF) for summarization.

## Features

- Input text directly or upload files (Word, PDF).
- Summarizes the complete text using the GPT-4o-mini model.
- User-friendly interface built with Streamlit.

## Project Structure

```
text-summarizer-app
├── src
│   ├── app.py            # Main entry point for the Streamlit application
│   ├── summarizer.py     # Logic for summarizing text using OpenAI
│   └── utils
│       └── file_handler.py # Utility functions for handling file uploads
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd text-summarizer-app
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key:**
   - Create a `.env` file in the root directory and add your API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run src/app.py
   ```

2. Open your web browser and go to `http://localhost:8501`.

3. You can either:
   - Enter text directly into the input box.
   - Upload a Word or PDF file containing the text you want to summarize.

4. Click the "Summarize" button to generate the summary.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.