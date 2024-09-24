import os
import argparse
import json
import tkinter as tk
from tkinter import ttk, scrolledtext
import pyperclip


def get_default_rules_path():
    xdg_config_home = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
    return os.path.join(xdg_config_home, 'colorizz', 'rules.json')


def load_rules(filepath):
    with open(filepath, 'r') as file:
        rules = json.load(file)
    lookup_dict = {}
    for rule in rules:
        for char in rule["affected_strings"]:
            lookup_dict[char] = rule["color"]["hex"]
    return lookup_dict


def colorize_text(text, lookup_dict):
    colored_text = ""
    for char in text:
        hex_color = lookup_dict.get(char, None)
        if char == "\n":
            colored_text += "<br>"
        elif hex_color is None:
            colored_text += f'<span style="text-decoration: underline;">{char}</span>'
        else:
            colored_text += f'<span style="color:{hex_color}">{char}</span>'
    return colored_text


def main():
    parser = argparse.ArgumentParser(description="Colorizz every letter in the input string based on predefined rules.")
    parser.add_argument('--rules', type=str, default=get_default_rules_path(), help='Path to the rules JSON file')
    parser.add_argument('--gui', action='store_true', help='Open a GUI to input and colorizz text')
    parser.add_argument('--replace-clip-board', action='store_true', help='Colorizz the text from the clipboard')
    args = parser.parse_args()
    lookup_dict = load_rules(args.rules)
    if args.gui:
        launch_gui(lookup_dict)
    elif args.replace_clip_board:
        clipboard_text = pyperclip.paste().strip()
        if clipboard_text:
            if clipboard_text.startswith("<span") or clipboard_text.startswith("<br>"):
                print("Aborting: Detected already colorizzed text in the clipboard.")
                return
            colorized_text = colorize_text(clipboard_text, lookup_dict)
            pyperclip.copy(colorized_text)
            print("Colorizzed text has been copied back to the clipboard.")


def launch_gui(lookup_dict):
    def on_text_change(event=None):
        input_text = input_text_area.get("1.0", tk.END)
        if input_text.strip():
            colorized_html = colorize_text(input_text.strip(), lookup_dict)
            output_text_area.config(state=tk.NORMAL)
            output_text_area.delete("1.0", tk.END)
            output_text_area.insert(tk.END, colorized_html)
            output_text_area.config(state=tk.DISABLED)
            pyperclip.copy(colorized_html)

    def copy_to_clipboard():
        pyperclip.copy(output_text_area.get("1.0", tk.END))

    def close_on_esc(event=None):
        gui.destroy()

    gui = tk.Tk()
    gui.title("Colorizz")

    style = ttk.Style()
    style.theme_use("clam")

    input_text_frame = ttk.Frame(gui, padding="10")
    input_text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    ttk.Label(input_text_frame, text="Your Rizzless Text Here:").pack(anchor=tk.W, pady=5)
    input_text_area = scrolledtext.ScrolledText(input_text_frame, wrap=tk.WORD, height=10)
    input_text_area.pack(fill=tk.BOTH, expand=True)
    input_text_area.bind("<KeyRelease>", on_text_change)
    input_text_area.bind("<Escape>", close_on_esc)

    output_text_frame = ttk.Frame(gui, padding="10")
    output_text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    ttk.Label(output_text_frame, text="Rizzed Text:").pack(anchor=tk.W, pady=5)
    output_text_area = scrolledtext.ScrolledText(output_text_frame, wrap=tk.WORD, height=10, state=tk.DISABLED)
    output_text_area.pack(fill=tk.BOTH, expand=True)

    copy_button = ttk.Button(gui, text="Copy that Rizz", command=copy_to_clipboard)
    copy_button.pack(pady=10)

    gui.bind("<Escape>", close_on_esc)
    gui.mainloop()


if __name__ == "__main__":
    main()
