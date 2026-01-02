# AI Search Agent

This is a simple command-line AI agent that answers your queries by searching the internet, summarizing the content, and providing the sources.

## Setup

1.  **Install Dependencies:**

    Make sure you have Python 3.6+ installed. Then, install the required libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up your Google API Key:**

    This project uses the Google Gemini API to generate summaries. You will need to get an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

    Once you have your key, you need to add it to the `.env` file.

    1.  Make a copy of the `.env.example` file and rename it to `.env`.
    2.  Open the `.env` file and replace `YOUR_API_KEY_HERE` with your actual API key.

    ```
    GOOGLE_API_KEY='YOUR_API_KEY_HERE'
    ```

## How to Run

Once you have completed the setup, you can run the agent with the following command:

```bash
python main.py
```

The application will start in an interactive mode, and you can start asking questions. To exit the application, type `exit` or `quit`.
