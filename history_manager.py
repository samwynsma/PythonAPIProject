import datetime
import os

from tkinter import messagebox
import tkinter as tk

# Optional dependency: pyodbc (install with `pip install pyodbc`)
try:
    import pyodbc
except Exception:
    pyodbc = None


class ApiHistoryManager:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), "APIDatabase.accdb")
        self.pyodbc = pyodbc

    def record_request(self, method, resource, user_id, id_, title, body, is_successful, table_name="APIReq"):
        if self.pyodbc is None:
            raise RuntimeError("pyodbc is required to write to Access. Install with `pip install pyodbc`.")

        conn_str = f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={self.db_path};"
        conn = self.pyodbc.connect(conn_str)
        cur = conn.cursor()

        self.ensure_history_table(cur, table_name)
        cur.execute(
            f"INSERT INTO {table_name} (Timestamp, Command, Resource, UserID, ResourceID, Title, Body, Successful) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.datetime.now(), method, resource, user_id, id_, title, body, is_successful),
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

    def read_history(self, table_name="APIReq"):
        if self.pyodbc is None:
            raise RuntimeError("pyodbc is required to read history from Access. Install with `pip install pyodbc`.")

        conn_str = f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={self.db_path};"
        conn = self.pyodbc.connect(conn_str)
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

    def format_history_text(self, history):
        lines = []
        for record in history:
            lines.append(f"ID: {record.get('ID', '')}")
            lines.append(f"Timestamp: {record.get('Timestamp', '')}")
            lines.append(f"Method: {record.get('Command', '')}")
            lines.append(f"Resource: {record.get('Resource', '')}")
            lines.append(f"User ID: {record.get('UserID', '')}")
            lines.append(f"Resource ID: {record.get('ResourceID', '')}")
            lines.append(f"Title: {record.get('Title', '')}")
            lines.append(f"Body: {record.get('Body', '')}")
            lines.append(f"Successful: {record.get('Successful', '')}")
            lines.append("-" * 86)
        return "\n".join(lines)

    def show_history_popup(self, parent):
        try:
            history = self.read_history()
        except Exception as exc:
            messagebox.showerror("History Error", f"Unable to load request history:\n{exc}")
            return None

        if not history:
            messagebox.showinfo("History", "No previous API calls were found.")
            return None

        popup = tk.Toplevel(parent)
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
        history_text.insert("end", self.format_history_text(history))
        history_text.configure(state="disabled")

        tk.Button(popup, text="Close", width=12, command=popup.destroy).pack(pady=(0, 10))
        return popup
