import tkinter as tk
from tkinter import ttk, Text, Scrollbar, messagebox
import json
import requests
import os

class CustomButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        style = ttk.Style()
        style.configure("GradientButton.TButton", padding=(10, 10, 10, 10), font=('Arial', 12), background="#1E90FF", foreground="black")
        ttk.Button.__init__(self, master, style="GradientButton.TButton", **kwargs)

class KeyGeneratorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Generate Key Example")

        # Set the Lexend font in the ttk.Style configuration
        style = ttk.Style()

        # Set a clean and modern color scheme
        style.configure("TNotebook", background="#f0f0f0")  # Light gray background
        style.configure("TFrame", background="#f0f0f0")  # Light gray background
        style.configure("TButton", padding=(10, 10, 10, 10), font=('Arial', 12), background="#1E90FF", foreground="black")

        # Configure a custom style for the tabs
        style.configure("TNotebook.Tab", background="#1E90FF", foreground="white", padding=(10, 5, 10, 5), borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", "#333")], foreground=[("selected", "black")])

        # Create a notebook with tabs for Python and JSON keys
        self.notebook = ttk.Notebook(self.root, style="TNotebook")

        # Create frames for each tab
        self.python_page = ttk.Frame(self.notebook)
        self.json_page = ttk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.python_page, text="Python Keys")
        self.notebook.add(self.json_page, text="JSON Keys")

        # Set up the Python page
        self.setup_python_page()

        # Set up the JSON page
        self.setup_json_page()

        # Pack the notebook
        self.notebook.pack(padx=10, pady=10)

    def setup_python_page(self):
        # Create a Text widget for Python keys output
        self.python_output_area = Text(self.python_page, wrap=tk.WORD, height=15, width=60, background="#f0f0f0", foreground="black", font=('Arial', 12))
        self.python_output_area.pack(padx=10, pady=10)

        # Add a scrollbar to the Text widget
        self.python_scrollbar = Scrollbar(self.python_page, command=self.python_output_area.yview)
        self.python_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.python_output_area.config(yscrollcommand=self.python_scrollbar.set)

        # Create a custom gradient button for Python
        self.generate_python_button = CustomButton(self.python_page, text="Generate Key in Python", command=self.generate_key_python)
        self.generate_python_button.pack(pady=10)

        # Create a custom gradient button for copying Python key
        copy_python_button = CustomButton(self.python_page, text="Copy Python Key", command=self.copy_key_python)
        copy_python_button.pack(pady=10)

    def setup_json_page(self):
        # Create a Text widget for JSON keys output
        self.json_output_area = Text(self.json_page, wrap=tk.WORD, height=15, width=60, background="#f0f0f0", foreground="black", font=('Arial', 12))
        self.json_output_area.pack(padx=10, pady=10)

        # Add a scrollbar to the Text widget
        self.json_scrollbar = Scrollbar(self.json_page, command=self.json_output_area.yview)
        self.json_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.json_output_area.config(yscrollcommand=self.json_scrollbar.set)

        # Create a custom gradient button for JSON
        self.generate_json_button = CustomButton(self.json_page, text="Generate Key in JSON", command=self.generate_key_json)
        self.generate_json_button.pack(pady=10)

        # Create a custom gradient button for copying JSON key
        copy_json_button = CustomButton(self.json_page, text="Copy JSON Key", command=self.copy_key_json)
        copy_json_button.pack(pady=10)

    def generate_key_python(self):
        sex_key = self.sexkey()
        output_text = f"{sex_key}\n"

        # Insert the output into the Text widget on the Python page
        self.python_output_area.insert(tk.END, output_text)
        self.python_output_area.yview(tk.END)

    def generate_key_json(self):
        sex_key = self.sexkey()
        url = "https://byfron.xyz/dash/redeem-key"
        headers = {'Content-Type': 'application/json'}
        data = {'key': sex_key}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an error for HTTP errors (status codes >= 400)

            content_type = response.headers.get('content-type', '')

            if 'application/json' in content_type:
                try:
                    response_json = response.json()
                    # Insert the output into the Text widget on the JSON page
                    self.json_output_area.insert(tk.END, json.dumps(response_json, indent=2) + "\n")
                    self.json_output_area.yview(tk.END)
                except json.JSONDecodeError:
                    self.json_output_area.insert(tk.END, "Error: Invalid JSON in response\n")
                    self.json_output_area.yview(tk.END)
            else:
                self.json_output_area.insert(tk.END, f"Error: Unexpected content type: {content_type}\n")
                self.json_output_area.insert(tk.END, "Raw response content:\n")
                self.json_output_area.insert(tk.END, response.text + "\n")
                self.json_output_area.yview(tk.END)

        except requests.RequestException as e:
            self.json_output_area.insert(tk.END, f"Error: {e}\n")
            self.json_output_area.yview(tk.END)

    def copy_key_python(self):
        # Copy Python key to clipboard
        python_key = self.sexkey()
        self.root.clipboard_clear()
        self.root.clipboard_append(python_key)
        self.root.update()
        messagebox.showinfo("Copy Success", "Python key copied to clipboard!")

    def copy_key_json(self):
        # Copy JSON key to clipboard
        json_key = self.sexkey()
        self.root.clipboard_clear()
        self.root.clipboard_append(json_key)
        self.root.update()
        messagebox.showinfo("Copy Success", "JSON key copied to clipboard!")

    def sexkey(self):
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        key_format = 'VISION-xxxxxx-xxxxxx-xxxxxx-xxxxxx-xxxxxx'
        random_key = ''
        for char in key_format:
            if char == 'x':
                random_key += characters[ord(os.urandom(1)) % len(characters)]
            else:
                random_key += char
        return random_key

    def run(self):
        # Run the Tkinter event loop
        self.root.mainloop()

# Create an instance of the KeyGeneratorApp class
app = KeyGeneratorApp()

# Run the Tkinter event loop
app.run()
