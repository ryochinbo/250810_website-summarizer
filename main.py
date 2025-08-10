import os
import io
import pandas as pd
import requests
from urllib.parse import urlplarse
from bs4 import BeautifulSoup
from dotenv import load_dotenv

import streamlit as st
from google import genai



client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)