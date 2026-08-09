import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-flash-latest")

def generate_story(stats: dict, correlations: dict, filename: str):
    prompt = f"""
You are a data analyst writing a short, engaging narrative summary of a dataset.

Dataset: {filename}

Here are the calculated statistics (already computed correctly — do not recalculate, only narrate):
{stats}

Here are the correlations between numeric columns:
{correlations}

Write a short, engaging 3-4 sentence story explaining what this data shows.
Use specific numbers from the stats provided. Do not make up any numbers not given above.
Keep it conversational, like explaining insights to a curious friend.
"""

    response = model.generate_content(prompt)
    return response.text