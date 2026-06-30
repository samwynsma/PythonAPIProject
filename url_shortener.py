import datetime
import os

from tkinter import messagebox
import tkinter as tk

# Optional dependency: pyodbc (install with `pip install pyodbc`)
try:
    import pyodbc
except Exception:
    pyodbc = None

class URLShortenManager:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), "APIDatabase.accdb")
        self.pyodbc = pyodbc

    def show_url_popup(self, parent):
        return