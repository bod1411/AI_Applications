# chatBPK Project

## Overview
chatBPK is a Streamlit application that allows users to interact with the OpenAI model "gpt-4o-mini". Users can input prompts and receive responses in real-time, making it a fun and engaging way to explore the capabilities of AI.

## Project Structure
```
chatBPK
├── src
│   ├── app.py          # Main entry point for the Streamlit application
│   ├── response.py     # Logic for interacting with the OpenAI API
│   └── utils
│       └── __init__.py # Utility functions and classes (currently empty)
├── requirements.txt     # Project dependencies
├── .env                 # Environment variables (e.g., OpenAI API key)
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd chatBPK
   ```

2. **Create a Virtual Environment**
   It is recommended to create a virtual environment to manage dependencies.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   Install the required packages using pip.
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage
To run the Streamlit application, execute the following command:
```bash
streamlit run src/app.py
```
This will start the application, and you can access it in your web browser.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.