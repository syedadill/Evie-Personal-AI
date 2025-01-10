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

    


# Set your OpenAI API key

import openai
import pdfplumber
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path="D:\AI\.env")

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

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

# Function to query OpenAI with enhanced prompt engineering
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
            model="gpt-4",  # Update to your desired model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides direct and insightful responses without referencing the source of the information."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error with OpenAI: {str(e)}"

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

        # Structure the response
        return Response({"answer": answer}, status=status.HTTP_200_OK)
