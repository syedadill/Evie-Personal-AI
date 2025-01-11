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

    
import openai
import pdfplumber
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from pathlib import Path
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

# Load environment variables
load_dotenv(dotenv_path="D:/AI/.env")

# Set your API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Path to the PDF file
PDF_PATH = Path(__file__).resolve().parent / "data" / "sample.pdf"

# Function to extract text from PDF
def extract_pdf_data(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting data: {str(e)}"

# Function to query OpenAI with context
def query_openai_with_context(pdf_text, user_query):
    try:
        # Crafting the prompt to provide context and clear instructions
        prompt = (
            f"The following information is available for reference:\n\n{pdf_text[:3000]}...\n\n"
            "Use this information and your general knowledge to provide a helpful, detailed answer to the user's question. "
            "Do not mention the source or refer to where the information came from. "
            f"User query: {user_query}"
        )
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides direct and insightful responses without referencing the source of the information."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return None  # Return None if OpenAI cannot provide an answer

import requests

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_news(query):
    try:
        # Simplify query for better matching
        simplified_query = " ".join(query.split()[-2:]) if len(query.split()) > 2 else query

        params = {
            "q": simplified_query,  # Use simplified query
            "apiKey": NEWS_API_KEY,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": 5  # Limit the number of articles
        }
        response = requests.get(NEWS_API_URL, params=params)
        response_data = response.json()

        if response.status_code == 200 and response_data.get("articles"):
            news_items = response_data["articles"]
            news_context = [
                f"{item['title']} ({item['source']['name']}): {item['url']}"
                for item in news_items
            ]
            return "\n".join(news_context)
        else:
            return "No recent news found for this query."
    except Exception as e:
        return f"Error fetching news: {str(e)}"

# API Endpoint for Assistant
class AssistantAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Ensure PDF file exists
        if not PDF_PATH.exists():
            return Response({"error": "PDF file not found"}, status=status.HTTP_404_NOT_FOUND)

        # Extract text from the PDF
        pdf_text = extract_pdf_data(PDF_PATH)
        if "Error extracting data" in pdf_text:
            return Response({"error": pdf_text}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get the user query from request body
        query = request.data.get("query", "").strip()
        if not query:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Query OpenAI with PDF content and user question
        answer = query_openai_with_context(pdf_text, query)

        # Check if OpenAI returned a useful answer
        if answer and "I'm sorry" not in answer:
            # If OpenAI provides a valid response, return it
            return Response({"answer": answer}, status=status.HTTP_200_OK)
        else:
            # If OpenAI fails, fetch news updates
            answer = fetch_news(query)
            return Response(
                {
                    "answer": "I couldn't find a direct answer. Here are some related news updates:",
                    "news_context": answer,
                },
                status=status.HTTP_200_OK,
            )