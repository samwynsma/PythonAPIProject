import requests
import tkinter as tk
import os
import json

from history_manager import ApiHistoryManager
from url_shortener import URLShortenManager

BASE_URL = "https://jsonplaceholder.typicode.com"


class ApiGuiManager:
    def __init__(self):
        self.method = "GET"
        self.resource = "posts"
        self.user_id = "1"
        self.id = "1"
        self.title = ""
        self.body = ""
        self.root = None
        self.history_manager = ApiHistoryManager()
        self.url_shorten_manager = URLShortenManager()
    
    def create_gui(self):
        root = tk.Tk()
        self.root = root
        root.title("API Selection")
        root.geometry("450x500")
        root.resizable(False, False)

        header = tk.Label(
            root,
            text="Welcome to Sam's API Selection app",
            font=("Segoe UI", 14, "bold"),
            wraplength=380,
            justify="center",
            pady=12,
        )
        header.pack()

        instructions = tk.Label(
            root,
            text="Select a type of API command, the information that you want to use, and then click \"Enter\"",
            font=("Segoe UI", 10),
            wraplength=380,
            justify="center",
        )
        instructions.pack(pady=(0, 14))

        request_frame = tk.Frame(root)
        request_frame.pack(padx=20, fill="x")

        self.request_type_var = tk.StringVar(value="GET")
        tk.Label(request_frame, text="API Request Type", anchor="w").grid(row=0, column=0, sticky="w", pady=6, columnspan=3)
        tk.Radiobutton(request_frame, text="GET", variable=self.request_type_var, value="GET").grid(row=0, column=1, sticky="w")
        tk.Radiobutton(request_frame, text="POST", variable=self.request_type_var, value="POST").grid(row=0, column=2, sticky="w")
        tk.Radiobutton(request_frame, text="PUT", variable=self.request_type_var, value="PUT").grid(row=0, column=3, sticky="w")
        tk.Radiobutton(request_frame, text="PATCH", variable=self.request_type_var, value="PATCH").grid(row=0, column=4, sticky="w")
        tk.Radiobutton(request_frame, text="DELETE", variable=self.request_type_var, value="DELETE").grid(row=0, column=5, sticky="w")
        tk.Radiobutton(request_frame, text="OPTIONS", variable=self.request_type_var, value="OPTIONS").grid(row=0, column=6, sticky="w")

        info_frame = tk.Frame(root)
        info_frame.pack(padx=20, fill="x")

        tk.Label(info_frame, text="Resource:", anchor="w").grid(row=0, column=0, sticky="w", pady=6)
        self.resource_entry = tk.Entry(info_frame, text="posts", width=28)
        self.resource_entry.insert(0, "posts")
        self.resource_entry.grid(row=0, column=1, pady=6)

        tk.Label(info_frame, text="User ID:", anchor="w").grid(row=1, column=0, sticky="w", pady=6)
        self.user_entry = tk.Entry(info_frame, width=28)
        self.user_entry.grid(row=1, column=1, pady=6)

        tk.Label(info_frame, text="id:", anchor="w").grid(row=2, column=0, sticky="w", pady=6)
        self.ID_entry = tk.Entry(info_frame, width=28)
        self.ID_entry.grid(row=2, column=1, pady=6)

        tk.Label(info_frame, text="Title:", anchor="w").grid(row=3, column=0, sticky="w", pady=6)
        self.title_entry = tk.Entry(info_frame, width=28)
        self.title_entry.grid(row=3, column=1, pady=6)

        tk.Label(info_frame, text="Body:", anchor="w").grid(row=4, column=0, sticky="w", pady=6)
        self.body_entry = tk.Entry(info_frame, width=28)
        self.body_entry.grid(row=4, column=1, pady=6)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=16)

        self.result_label = tk.Label(root, text="", font=("Segoe UI", 10), fg="green", wraplength=420, justify="center")
        self.result_label.pack(pady=(8, 0))

        tk.Button(button_frame, text="Run API Request", width=16, command=self.run_api_command).grid(row=0, column=0, padx=6)
        tk.Button(button_frame, text="History", width=16, command=self.get_history).grid(row=0, column=1, padx=6)
        tk.Button(button_frame, text="URL Shortener", width=16, command=self.run_url_shortener).grid(row=0, column=2, padx=6)
        tk.Button(button_frame, text="Quit", width=16, command=root.destroy).grid(row=0, column=3, padx=6)

        root.mainloop()

    def run_api_command(self):
        self.method = self.request_type_var.get()
        self.resource = self.resource_entry.get().strip()
        self.user_id = self.user_entry.get()
        self.id = self.ID_entry.get()
        self.title = self.title_entry.get()
        self.body = self.body_entry.get()

        url, kwargs = self.build_request_data(
            self.method,
            self.resource,
            self.user_id,
            self.id,
            self.title,
            self.body,
        )

        new_request = self.safe_request_api(self.method, url, **kwargs)

        # Ensure the label receives a string
        self.result_label.config(text=str(new_request))

    def get_history(self):
        parent = self.root if self.root is not None else None
        self.history_manager.show_history_popup(parent)

    def run_url_shortener(self):
        parent = self.root if self.root is not None else None
        self.url_shorten_manager.show_url_popup(parent)

    @staticmethod
    def build_request_data(method, resource="", user_id="", id_="", title="", body=""):
        resource = resource.strip()
        url = f"{BASE_URL}/{resource}" if resource else BASE_URL

        params = {}
        if user_id:
            params["userId"] = user_id

        if id_:
            if method in ("POST", "PUT", "PATCH"):
                params["id"] = id_
            url = f"{url}/{id_}"

        if title:
            params["title"] = title

        if body:
            params["body"] = body

        if method in ("POST", "PUT", "PATCH"):
            return url, {"json": params}
        return url, {"params": params}


    def safe_request_api(self, method, url, **kwargs):
        try:
            self.result_label.config(fg="green")
            response = requests.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            try:
                result = response.json()
            except ValueError:
                text = response.text.strip()
                self.result_label.config(fg="green")
                if text:
                    result = {"status_code": response.status_code, "text": text}
                else:
                    result = {
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "message": "No response body returned.",
                    }

            # Attempt to write result to Access DB; failures shouldn't stop the app
            try:
                self.history_manager.record_request(
                    self.method,
                    self.resource,
                    self.user_id,
                    self.id,
                    self.title,
                    self.body,
                    True,
                )
            except Exception:
                pass

            return result
        except requests.exceptions.RequestException as e:
            self.result_label.config(fg="red")
            err = {"error": str(e)}
            try:
                self.history_manager.record_request(
                    self.method,
                    self.resource,
                    self.user_id,
                    self.id,
                    self.title,
                    self.body,
                    False,
                )
            except Exception:
                pass
            return err
        

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
    
    gui = ApiGuiManager()
    gui.create_gui()

    return

if __name__ == "__main__":
    main()
