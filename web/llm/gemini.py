
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('AIzaSyCwNdYKPAkCyojmefc8UIGX2ysSRrLq2DU'))

def get_response(text: str) -> str:
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f'एक अनुभवी भारतीय किसान की तरह सरल हिंदी में जवाब दो:\n\n{text}'
    response = model.generate_content(prompt)
    return response.text
