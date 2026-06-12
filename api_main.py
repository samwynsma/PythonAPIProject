import requests
import tkinter as tk
from tkinter import messagebox

BASE_URL = "https://jsonplaceholder.typicode.com"

class ApiGuiManager:
    def __init__(self):
        self.method = "GET"
        self.user_id = 1
        self.id = 1
        self.title = ""
        self.body = ""
    
    def create_gui(self):
        root = tk.Tk()
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
        tk.Label(request_frame, text="API Request Type", anchor="w").grid(row=0, column=0, sticky="w", pady=6)
        tk.Radiobutton(request_frame, text="GET", variable=self.request_type_var, value="GET").grid(row=0, column=1, sticky="w")
        tk.Radiobutton(request_frame, text="POST", variable=self.request_type_var, value="POST").grid(row=0, column=2, sticky="w")
        tk.Radiobutton(request_frame, text="PUT", variable=self.request_type_var, value="PUT").grid(row=0, column=3, sticky="w")
        tk.Radiobutton(request_frame, text="PATCH", variable=self.request_type_var, value="PATCH").grid(row=0, column=4, sticky="w")
        tk.Radiobutton(request_frame, text="DELETE", variable=self.request_type_var, value="DELETE").grid(row=0, column=5, sticky="w")

        info_frame = tk.Frame(root)
        info_frame.pack(padx=20, fill="x")

        tk.Label(info_frame, text="Resource:", anchor="w").grid(row=0, column=0, sticky="w", pady=6)
        self.resource_entry = tk.Entry(info_frame, width=28)
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
        tk.Button(button_frame, text="Quit", width=16, command=root.destroy).grid(row=0, column=1, padx=6)

        root.mainloop()

    def run_api_command(self):
        self.method = self.request_type_var.get()
        self.user_id = self.user_entry.get()
        self.id = self.ID_entry.get()
        self.title = self.title_entry.get()
        self.body = self.body_entry.get()
        url = f"{BASE_URL}/"
        url += self.resource_entry.get()
        params = {}
        if(len(self.user_id) > 0):
            params["userId"] = self.user_id

        if(len(self.id) > 0):
            if(self.method == "POST" or self.method == "PUT" or self.method == "PATCH"):
                params["id"] = self.id
            url += "/"
            url += self.id
        
        if(len(self.title) > 0):
            params["title"] = self.title

        if(len(self.body) > 0):
            params["body"] = self.body

        # For write methods send the data as JSON body, otherwise send as query params
        if self.method in ("POST", "PUT", "PATCH"):
            new_request = self.safe_request_api(self.method, url, json=params)
        else:
            new_request = self.safe_request_api(self.method, url, params=params)

        # Ensure the label receives a string
        self.result_label.config(text=str(new_request))
    

    def safe_request_api(self, method, url, **kwargs):
        try:
            self.result_label.config(fg="green")
            response = requests.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            try:
                return response.json()
            except ValueError:
                self.result_label.config(fg="red")
                return response.text
        except requests.exceptions.RequestException as e:
            self.result_label.config(fg="red")
            return {"error": str(e)}
        




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
    print("GET /posts")
    posts = safe_request("GET", f"{BASE_URL}/posts")
    print(posts[:2])

    print("\nGET /posts?userId=1")
    posts = safe_request("GET", f"{BASE_URL}/posts", params={"userId" : 1})
    print(posts)

    print("\nPOST /posts")
    new_post = safe_request("POST", f"{BASE_URL}/posts", json={"title": "A Test Post for Testing", "body" : "This is a drill.", "userId" : 1})
    print(new_post)

    print("\nPUT /posts/1")
    updated_post = safe_request("PUT", f"{BASE_URL}/posts/1", json={"id": 1, "title": "Updated Test Title", "body": "New content for a new test!", "userId" : 1})
    print(updated_post)

    print("\nPATCH /posts/1")
    patched_post = safe_request("PATCH", f"{BASE_URL}/posts/1", json={"id" : 1, "title" : "Only a little bit."})
    print(patched_post)

    print("\nDELETE /posts/1")
    deleted_post = safe_request("DELETE", f"{BASE_URL}/posts/1")
    print(deleted_post)

    gui = ApiGuiManager()
    gui.create_gui()

    return

if __name__ == "__main__":
    main()
