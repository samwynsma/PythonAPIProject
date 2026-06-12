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

    return

if __name__ == "__main__":
    main()
