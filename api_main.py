import requests
import tkinter as tk
from tkinter import messagebox
import os
import json
import datetime

# Optional dependency: pyodbc (install with `pip install pyodbc`)
try:
    import pyodbc
except Exception:
    pyodbc = None

BASE_URL = "https://jsonplaceholder.typicode.com"

class ApiGuiManager:
    def __init__(self):
        self.method = "GET"
        self.resource = "posts"
        self.user_id = "1"
        self.id = "1"
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
        tk.Button(button_frame, text="Quit", width=16, command=root.destroy).grid(row=0, column=2, padx=6)

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
        db_path = os.path.join(os.path.dirname(__file__), "APIDatabase.accdb")
        try:
            history = self.read_history_from_access(db_path)
        except Exception as exc:
            messagebox.showerror("History Error", f"Unable to load request history:\n{exc}")
            return

        if not history:
            messagebox.showinfo("History", "No previous API calls were found.")
            return

        popup = tk.Toplevel()
        popup.title("API Request History")
        popup.geometry("760x460")
        popup.minsize(520, 320)
        popup.resizable(True, True)

        header = tk.Label(popup, text="Previous API Calls", font=("Segoe UI", 12, "bold"))
        header.pack(pady=(12, 4))

        frame = tk.Frame(popup)
        frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        history_text = tk.Text(frame, wrap="word", state="disabled", font=("Segoe UI", 10), padx=8, pady=6)
        history_scroll = tk.Scrollbar(frame, command=history_text.yview)
        history_text.configure(yscrollcommand=history_scroll.set)
        history_scroll.pack(side="right", fill="y")
        history_text.pack(side="left", fill="both", expand=True)

        history_text.configure(state="normal")
        for record in history:
            history_text.insert("end", f"ID: {record.get('ID', '')}\n")
            history_text.insert("end", f"Timestamp: {record.get('Timestamp', '')}\n")
            history_text.insert("end", f"Method: {record.get('Command', '')}\n")
            history_text.insert("end", f"Resource: {record.get('Resource', '')}\n")
            history_text.insert("end", f"User ID: {record.get('UserID', '')}\n")
            history_text.insert("end", f"Resource ID: {record.get('ResourceID', '')}\n")
            history_text.insert("end", f"Title: {record.get('Title', '')}\n")
            history_text.insert("end", f"Body: {record.get('Body', '')}\n")
            history_text.insert("end", f"Successful: {record.get('Successful', '')}\n")
            history_text.insert("end", "-" * 86 + "\n")
        history_text.configure(state="disabled")

        tk.Button(popup, text="Close", width=12, command=popup.destroy).pack(pady=(0, 10))

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
                db_path = os.path.join(os.path.dirname(__file__), "APIDatabase.accdb")
                self.write_results_to_access(db_path, True)
            except Exception:
                pass

            return result
        except requests.exceptions.RequestException as e:
            self.result_label.config(fg="red")
            err = {"error": str(e)}
            try:
                db_path = os.path.join(os.path.dirname(__file__), "APIDatabase.accdb")
                self.write_results_to_access(db_path, False)
            except Exception:
                pass
            return err
        
    def write_results_to_access(self, db_path, isSuccessful, table_name="APIReq"):
        """Write the current request metadata into an Access .accdb file.

        - Requires `pyodbc` and the Microsoft Access ODBC driver installed on Windows.
        - Creates the history table if it doesn't exist.
        """
        if pyodbc is None:
            raise RuntimeError("pyodbc is required to write to Access. Install with `pip install pyodbc`.")

        conn_str = f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};"
        conn = pyodbc.connect(conn_str)
        cur = conn.cursor()

        self.ensure_history_table(cur, table_name)

        cur.execute(
            f"INSERT INTO {table_name} (Timestamp, Command, Resource, UserID, ResourceID, Title, Body, Successful) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.datetime.now(), self.method, self.resource, self.user_id, self.id, self.title, self.body, isSuccessful),
        )
        conn.commit()
        cur.close()
        conn.close()

    def ensure_history_table(self, cur, table_name="APIReq"):
        try:
            cur.execute(f"SELECT TOP 1 * FROM {table_name}")
            columns = [column[0].lower() for column in cur.description]
            required_columns = {"timestamp", "command", "resource", "userid", "resourceid", "title", "body", "successful"}
            missing = required_columns.difference(set(columns))
            if missing:
                for column_name in missing:
                    if column_name == "body":
                        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN Body MEMO")
                    elif column_name == "successful":
                        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN Successful YESNO")
                    else:
                        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} TEXT")
                cur.connection.commit()
        except Exception:
            cur.execute(
                f"CREATE TABLE {table_name} ("
                "ID COUNTER PRIMARY KEY, "
                "Timestamp DATETIME, "
                "Command TEXT, "
                "Resource TEXT, "
                "UserID TEXT, "
                "ResourceID TEXT, "
                "Title TEXT, "
                "Body MEMO, "
                "Successful YESNO)"
            )
            cur.connection.commit()

    def read_history_from_access(self, db_path, table_name="APIReq"):
        if pyodbc is None:
            raise RuntimeError("pyodbc is required to read history from Access. Install with `pip install pyodbc`.")

        conn_str = f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};"
        conn = pyodbc.connect(conn_str)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        columns = [column[0] for column in cur.description]
        results = [dict(zip(columns, row)) for row in rows]
        cur.close()
        conn.close()

        results.sort(
            key=lambda record: record.get("Timestamp") or datetime.datetime.min,
            reverse=True,
        )
        return results
        




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
