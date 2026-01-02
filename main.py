from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def search_web(query, num_results=5):
    """
    Searches the web for a given query using DuckDuckGo and returns a list of URLs.
    """
    try:
        print(f"Searching the web for: {query}...")
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=num_results))
            urls = [r['href'] for r in results]
            print(f"Found {len(urls)} results.")
            return urls
    except Exception as e:
        print(f"An error occurred during web search: {e}")
        return []

def fetch_and_parse(url):
    """
    Fetches the content of a URL and parses it to extract the text.
    """
    try:
        print(f"Fetching content from: {url}...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        text = soup.get_text()

        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        print(f"Successfully fetched and parsed content from: {url}")
        return text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL {url}: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while parsing the content from {url}: {e}")
        return None

def summarize_text(text, query):
    """
    Summarizes the given text using the Gemini API.
    """
    try:
        # IMPORTANT: You need to set the GOOGLE_API_KEY environment variable
        # for this to work.
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("\nWARNING: The GOOGLE_API_KEY is not set. The summarization will fail.")
            print("Please set the environment variable.\n")
            return "Could not generate a summary due to a missing API key."

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel('gemini-pro')

        prompt = f"Based on the following text, please provide a concise summary that directly answers the question: '{query}'\n\nText:\n{text}"

        print("Generating summary...")
        response = model.generate_content(prompt)
        print("Summary generated successfully.")
        return response.text
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return "Could not generate a summary."

def main():
    """
    The main function that runs the interactive AI agent.
    """
    print("Welcome to the AI Search Agent!")
    print("Type 'exit' or 'quit' to end the session.")

    while True:
        try:
            query = input("\nPlease enter your query: ").strip()
        except EOFError:
            break

        if query.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        if not query:
            print("Query cannot be empty. Please try again.")
            continue

        urls = search_web(query, num_results=3) # Limit to 3 results for faster processing

        if not urls:
            print("Could not find any relevant websites for your query.")
            continue

        all_text = ""
        for url in urls:
            content = fetch_and_parse(url)
            if content:
                all_text += content + "\n\n"

        if not all_text:
            print("Could not extract content from the found websites.")
            continue

        summary = summarize_text(all_text, query)

        print("\n" + "="*50)
        print("AI Generated Summary:")
        print(summary)
        print("\nSources:")
        for url in urls:
            print(f"- {url}")
        print("="*50 + "\n")


if __name__ == "__main__":
    main()
