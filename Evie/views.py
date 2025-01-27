from django.shortcuts import render
# Create your views here.
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny , IsAuthenticated
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import *


class RegisterView(generics.CreateAPIView):
    queryset= User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# import openai
# import pdfplumber
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from pathlib import Path
# import os
# from dotenv import load_dotenv
# import requests
# from googleapiclient.discovery import build

# # Load environment variables
# load_dotenv(dotenv_path="D:/AI/.env")

# # Set your API keys
# openai.api_key = os.getenv("OPENAI_API_KEY")
# NEWS_API_KEY = os.getenv("NEWS_API_KEY")
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

# # Path to the PDF file
# PDF_PATH = Path(__file__).resolve().parent / "data" / "sample.pdf"

# # Function to extract text from PDF
# def extract_pdf_data(file_path):
#     try:
#         with pdfplumber.open(file_path) as pdf:
#             text = ""
#             for page in pdf.pages:
#                 text += page.extract_text()
#         return text
#     except Exception as e:
#         return f"Error extracting data: {str(e)}"

# # Function to query OpenAI with context
# def query_openai_with_context(pdf_text, user_query):
#     try:
#         # Crafting the prompt to provide context and clear instructions
#         prompt = (
#             f"The following information is available for reference:\n\n{pdf_text[:3000]}...\n\n"
#             "Use this information and your general knowledge to provide a helpful, detailed answer to the user's question. "
#             "Do not mention the source or refer to where the information came from. "
#             f"User query: {user_query}"
#         )
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant that provides direct and insightful responses without referencing the source of the information."},
#                 {"role": "user", "content": prompt},
#             ],
#             max_tokens=500,
#         )
#         return response['choices'][0]['message']['content'].strip()
#     except Exception as e:
#         return None  # Return None if OpenAI cannot provide an answer

# # Function to fetch news from NewsAPI
# def fetch_news(query):
#     try:
#         simplified_query = " ".join(query.split()[-2:]) if len(query.split()) > 2 else query

#         params = {
#             "q": simplified_query,
#             "apiKey": NEWS_API_KEY,
#             "sortBy": "publishedAt",
#             "language": "en",
#             "pageSize": 5
#         }
#         response = requests.get("https://newsapi.org/v2/everything", params=params)
#         response_data = response.json()

#         if response.status_code == 200 and response_data.get("articles"):
#             news_items = response_data["articles"]
#             news_context = [
#                 f"{item['title']} ({item['source']['name']}): {item['url']}"
#                 for item in news_items
#             ]
#             return "\n".join(news_context)
#         else:
#             return "No recent news found for this query."
#     except Exception as e:
#         return f"Error fetching news: {str(e)}"

# # Function to perform Google Custom Search
# def fetch_google_search_results(query):
#     try:
#         service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
#         res = service.cse().list(q=query, cx=GOOGLE_SEARCH_ENGINE_ID).execute()

#         if 'items' in res:
#             search_results = []
#             for item in res['items']:
#                 search_results.append(f"{item['title']}: {item['link']}")
#             return "\n".join(search_results)
#         else:
#             return "No relevant search results found on Google."
#     except Exception as e:
#         return f"Error fetching Google search results: {str(e)}"

# # API Endpoint for Assistant
# class AssistantAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         # Ensure PDF file exists
#         if not PDF_PATH.exists():
#             return Response({"error": "PDF file not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Extract text from the PDF
#         pdf_text = extract_pdf_data(PDF_PATH)
#         if "Error extracting data" in pdf_text:
#             return Response({"error": pdf_text}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Get the user query from request body
#         query = request.data.get("query", "").strip()
#         if not query:
#             return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Query OpenAI with PDF content and user question
#         answer = query_openai_with_context(pdf_text, query)

#         # Check if OpenAI returned a useful answer
#         if answer and "I'm sorry" not in answer:
#             return Response({"answer": answer}, status=status.HTTP_200_OK)
#         else:
#             # If OpenAI fails, fetch Google search results
#             google_results = fetch_google_search_results(query)
#             return Response(
#                 {
#                     "answer": "I couldn't find a direct answer. Here are some related Google search results:",
#                     "google_results": google_results,
#                 },
#                 status=status.HTTP_200_OK,
#             )


import openai
#import pdfplumber
import PyPDF2
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from pathlib import Path
import os
from dotenv import load_dotenv
import requests
from googleapiclient.discovery import build

# Load environment variables
load_dotenv(dotenv_path="D:/AI/.env")

# Ensure environment variables are loaded
openai.api_key = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

# Session memory file path
SESSION_MEMORY_FILE = "session_memory.json" # Adjust path as needed for your django project

# Initialize session_memory as a global variable
session_memory = []

def load_session_memory():
    if os.path.exists(SESSION_MEMORY_FILE):
        try:
            with open(SESSION_MEMORY_FILE, "r") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                else:
                    print(f"Session memory is not a list, resetting memory.")
                    return []
        except Exception as e:
            print(f"Error loading session memory: {e}")
            return []
    return []

def save_session_memory(session_memory):
    try:
        with open(SESSION_MEMORY_FILE, "w") as file:
            json.dump(session_memory, file, indent=4)
    except Exception as e:
        print(f"Error saving session memory: {e}")

# Load session memory at startup
session_memory = load_session_memory()

def extract_pdf_data(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            content = "".join(page.extract_text() for page in reader.pages)
            return content.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

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

def generate_response(query, pdf_data, search_results, session_memory):
    memory_context = "\n".join(
        [f"User Query: {entry['query']}\nAssistant Response: {entry['response']}" for entry in session_memory[-4:]]
    ) if len(session_memory) >= 4 else ""

    prompt = f"""
You are a highly intelligent,Personal assistant who use user data to help them decision making using his data and realtime google search data,  **Concise, actionable, and contextually relevant** responses. Your primary focus is on maintaining conversational continuity and ensuring clarity in every interaction.


###Context:

    ### Session Memory (Recent Conversations):
    {session_memory}
    ### Current Query:
    "{query}"

    ### PDF Data (Personal Context):
    {pdf_data[:3000]}

    ### Search Results (Real-Time Context):
    {search_results}
- **Session Memory**: The user's recent queries and your responses. Always get the context from here if you user doesn't specify the query.
- **Search Results**: Real-time, up-to-date data to supplement context.
- **PDF Data**: Personalized information relevant to the user's queries.
    

### Core Principles:
1. **Strict Context Reliance**: Every response must consider the user's previous query and your last response. Assume follow-up queries are related to the last conversation unless explicitly stated otherwise.
2. **Focused and Relevant Responses**: If the query is ambiguous, prioritize the context of the last response. Provide specific answers that directly address the user's intent without drifting into unrelated suggestions.
3. **Clarification When Necessary**: If the query cannot be linked to prior context or lacks clarity, politely ask targeted questions to refine your understanding before generating a response.
4. Always provide the response only related to the last query if user does not specify any other thing

### Behavior for Follow-Up Queries:
1. Dont show the options or suggestions just provide the best option according with their relevant details.
1. To specify the context or topic dont ask the user always get it from the last query or response in **Session Memory**.
2. Always reference the most recent query and response in session memory.
3. If the user does not specify a context, assume it is a continuation of the previous topic.
4. Respond specifically to the topic of the previous conversation unless explicitly instructed otherwise.



### Structure of Response:
1. **Start with Contextual Acknowledgment**: Briefly connect the new response to the last query or response, ensuring continuity.
2. **Provide Focused Information**: Answer only what the user is asking, staying on topic.
3. **Avoid Generic Suggestions**: Do not introduce unrelated information unless the query explicitly asks for it.
4. **Ask When Necessary**: If the query remains unclear after context analysis, request clarification politely and briefly.

### Task Instructions:
To specify the context or topic dont ask the user always get it from the last query or response in **Session Memory**.
- Before generating a response, always review:
  - The user's last query and your response in session memory.
  - Any relevant data (PDF or search results) if applicable.
- Use the last response as the **primary context** unless a clear shift in topic is indicated.
- Generate a response that is concise, relevant, and actionable.
- Provide relevant information (e.g., names, details, pricing, contact info).


### Task:
1. Analyze the user's current query in the context of their last query and response.
2. Generate a concise and contextually relevant response that directly addresses the user's query.
3. If the query is ambiguous, infer intent from the last conversation or ask a brief follow-up question for clarification.
4. Provide actionable, specific recommendations or information that aligns with the user's intent.
5. Provide relevant information (e.g., names, details, pricing, contact info).
6. To specify the context or topic dont ask the user always get it from the last query or response in **Session Memory**.

Now, generate the response:
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a highly intellignet personal assistant , who have user spcecific data and realtime search data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"
from django.conf import settings
class AssistantAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        global session_memory  # Add this global declaration at the top of the method
        
        user_input = request.data.get("query")

        if not user_input:
            return Response(
                {"error": "Please provide a query."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
                
        # Use Django's settings to get the correct file path
        pdf_path = os.path.join(settings.BASE_DIR, 'Evie', 'data', 'sample.pdf')
        
        # Fallback mechanism
        if not os.path.exists(pdf_path):
            # Check if PDF is stored in media or static files
            alternative_paths = [
                os.path.join(settings.MEDIA_ROOT, 'sample.pdf'),
                os.path.join(settings.STATIC_ROOT, 'sample.pdf')
            ]
            
            for alt_path in alternative_paths:
                if os.path.exists(alt_path):
                    pdf_path = alt_path
                    break
            else:
                return Response({
                    "error": "PDF file not found",
                    "paths_checked": [pdf_path] + alternative_paths
                }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            pdf_data = extract_pdf_data(pdf_path)

            if "Error" in pdf_data:
                return Response({
                    "error": pdf_data,
                    "file_path": pdf_path
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            search_results = search_google(user_input)

        

            if "Error" in search_results[0]:
                return Response({"error": search_results[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            summarized_response = generate_response(user_input, pdf_data, search_results, session_memory)
            
            session_memory.append({"query": user_input, "response": summarized_response})
            save_session_memory(session_memory)

            return Response({"response": summarized_response}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "error": str(e),
                "file_path": pdf_path
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
