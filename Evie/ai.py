import requests
import openai
import os
import PyPDF2
import json

# OpenAI GPT API Key
openai.api_key = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

# Session memory file path
SESSION_MEMORY_FILE = "session_memory.json"

# Function to load session memory from a file
def load_session_memory():
    if os.path.exists(SESSION_MEMORY_FILE):
        try:
            with open(SESSION_MEMORY_FILE, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading session memory: {e}")
    return {}

# Function to save session memory to a file
def save_session_memory(session_memory):
    try:
        with open(SESSION_MEMORY_FILE, "w") as file:
            json.dump(session_memory, file, indent=4)
    except Exception as e:
        print(f"Error saving session memory: {e}")

# Load session memory at startup
session_memory = load_session_memory()

# Function to read and extract text from a PDF file
def extract_pdf_data(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            content = "".join(page.extract_text() for page in reader.pages)
            return content.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Function to perform a web search using Google Custom Search API
def search_google(query):
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": GOOGLE_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "num": 5,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        search_results = response.json().get("items", [])
        return [result["snippet"] for result in search_results if "snippet" in result]
    except Exception as e:
        return [f"Error: {str(e)}"]

def summarize_results(results, query, pdf_data, session_memory):
    # Get the last query-response pair for context
    last_query, last_response = session_memory.popitem() if session_memory else ("", "")

    # Combine session memory context
    memory_context = "\n".join(
        [f"User Query: {q}\nAssistant Response: {r}" for q, r in list(session_memory.items())[-4:]]
    )
    memory_context += f"\nUser Query: {last_query}\nAssistant Response: {last_response}" if last_response else ""

    # Build a detailed prompt
    prompt = f"""
You are an intelligent personal assistant. Your goal is to provide precise, relevant, and actionable responses.

### Current Query:
"{query}"

### PDF Data (Personal Info):
{pdf_data[:2000]}

### Search Results:
{results}

### Session Memory Context (Recent History):
{memory_context}

### Task:
- Respond to the user's current query by using all available context.
- Refer to the previous query and response when relevant.
- Provide meaningful and actionable suggestions.
- For ambiguous queries like "Why?" or "What next?", use context to clarify or ask for more information.

Now, provide the best response:
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful and intelligent assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"
    
def main():
    pdf_path = "D:\\AI\\Evie\\data\\sample.pdf"
    pdf_data = extract_pdf_data(pdf_path)

    if "Error" in pdf_data:
        print(pdf_data)
        return

    print("PDF data loaded successfully. Hi, How can I assist you?")
    last_query = ""
    last_response = ""
    
    while True:
        user_input = input("\nEnter your query (or type 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            save_session_memory(session_memory)  # Save memory before exiting
            break

        if not user_input:
            print("Please enter a valid query.")
            continue

        # Combine last context
        combined_context = f"Last query: {last_query}\nLast response: {last_response}" if last_query else ""

        print("\nSearching for relevant information...")
        search_results = search_google(user_input)

        if "Error" in search_results[0]:
            print(search_results[0])
            continue

        summarized_response = summarize_results(search_results, user_input, pdf_data, session_memory)
        
        # Save the current query and response in memory
        session_memory[user_input] = summarized_response
        save_session_memory(session_memory)  # Save memory after every query

        # Update last query and response
        last_query = user_input
        last_response = summarized_response

        print("\nSmart Assistant Response:")
        print(summarized_response)

# Run the bot
if __name__ == "__main__":
    main()
