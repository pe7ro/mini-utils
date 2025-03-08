import pathlib
import re
import tkinter as tk
from datetime import datetime
import logging


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Taker")

        # Create main frame
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)

        # Create left frame for text input
        left_frame = tk.Frame(main_frame, bg="#f0f0f0", highlightbackground="#ccc", highlightthickness=1, highlightcolor='#999')
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Create text input field
        self.text_label = tk.Label(left_frame, text="Text:", bg="#f0f0f0", font=("Arial", 12, "bold"))
        self.text_label.pack()
        self.text_entry = tk.Text(left_frame, font=("Latin Modern Mono", 12), bg="#fff", highlightbackground="#eee",
                                  highlightthickness=1)
        self.text_entry.bind_all("<Control-a>", lambda e: self.text_entry.tag_add("sel", "1.0", "end"))
        self.text_entry.pack(fill="both", expand=True, padx=10, pady=10)

        # Create right frame for tag and submit button
        right_frame = tk.Frame(main_frame, bg="#f0f0f0", highlightbackground="#ccc", highlightthickness=1, highlightcolor='#999')
        right_frame.pack(side="right", fill="y", padx=10, pady=10)

        # Create tag input field
        self.tag_label = tk.Label(right_frame, text="Tag:", bg="#f0f0f0", font=("Arial", 12, "bold"))
        self.tag_label.pack(fill="x")
        self.tag_entry = tk.Entry(right_frame, font=("Latin Modern Mono", 12), bg="#fff", highlightbackground="#ccc",
                                  highlightthickness=1)
        self.tag_entry.pack(fill="x", padx=10, pady=10)

        # Create submit button
        self.submit_button = tk.Button(right_frame, text="Submit", command=self.submit_note, font=("Arial", 12, "bold"),
                                       bg="#4CAF50", fg="#fff", highlightbackground="#ccc", highlightthickness=1)
        self.submit_button.pack(fill="x", padx=10, pady=10)

        # tmp = tk.(right_frame) #, bg="#f0f0f0")
        # right_frame.pack(fill="y", padx=10, pady=10)

        self.clear_button = tk.Button(right_frame, text="Clear", command=self.clear_text, font=("Arial", 12, "bold"),
                                      bg="#f44336", fg="#fff", highlightbackground="#ccc", highlightthickness=1)
        # self.clear_button.pack(fill="x", padx=10, pady=10)
        self.clear_button.pack(side="bottom", fill="x", padx=10, pady=10)

    def clear_text(self):
        self.text_entry.delete("1.0", tk.END)
        # self.tag_entry.update()

    def submit_note(self):
        tag = self.tag_entry.get()
        text = self.text_entry.get("1.0", tk.END)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        tag = tag.strip()
        tag = re.sub(r'[./?<>\\:*|"\'\[\]{}]', '_', tag)
        tag = re.sub(r'_+', '_', tag)
        filename = pathlib.Path(f"{tag}.md")
        with filename.open("a") as file:
            file.write(f"\n\n---\n### {timestamp}\n\n{text}\n\n")

        logging.info(f'Appended to {filename.absolute()}, len={len(text)}')
        self.text_entry.delete("1.0", tk.END)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)
    root = tk.Tk()
    app = App(root)
    root.mainloop()
