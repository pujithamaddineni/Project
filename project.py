import tkinter as tk
from tkinter import ttk

# Create the main application window
app = tk.Tk()
app.title("Language Translator")
app.geometry("1000x700")
app.resizable(False, False)

# Title Label
title_label = tk.Label(app, text="Language Translator", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

language_label = tk.Label(app, text="Select Input Language:")
language_label.pack(anchor="w", padx=20, pady=5)
language_dropdown = ttk.Combobox(app, values=["తేలుగు ", "English", "हिन्दी ","ಕನ್ನಡ ","ଓଡିଆ","ମାଲାୟଲମ"])
language_dropdown.pack(padx=20, fill="x")
language_dropdown.set("English") 

# Input Text Area
input_label = tk.Label(app, text="Enter Text:")
input_label.pack(anchor="w", padx=20)
input_text_area = tk.Text(app, height=6, width=55)
input_text_area.pack(padx=20)

# Language Dropdown
language_label = tk.Label(app, text="Select Target Language:")
language_label.pack(anchor="w", padx=20, pady=5)
language_dropdown = ttk.Combobox(app, values=["తేలుగు ", "English", "हिन्दी ","ಕನ್ನಡ ","ଓଡିଆ","ମାଲାୟଲମ"])
language_dropdown.pack(padx=20, fill="x")
language_dropdown.set("English")  # Set default language

language = list(LANGUAGES.values())

dest_lang= ttk.Combobox(app, values= language, width=22)
dest_lang.place(x=130, y=180)
dest_lang.set('choose language')
#root.mainloop()

# Translate Button
translate_button = tk.Button(app, text="Translate", bg="#007BFF", fg="white", font=("Arial", 12, "bold"))
translate_button.pack(pady=15)

# Output Text Area
output_label = tk.Label(app, text="Translated Text:")
output_label.pack(anchor="w", padx=20)
output_text_area = tk.Text(app, height=6, width=55, state="normal")
output_text_area.pack(padx=20)

# Run the application
app.mainloop()
