import requests
import tkinter as tk
from tkinter import messagebox

BASE_URL = "https://jsonplaceholder.typicode.com"

def safe_request(method, url, **kwargs):
    
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return response.text
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    return

