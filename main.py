import base64
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from cryptography.fernet import Fernet

window = Tk()
window.geometry("400x620")
window.config(padx=30, pady=30)
window.title("Secret Notes")


def encryption(note, key):
    combined_content = note + key
    encoded_bytes = base64.b64encode(combined_content.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")
    return encoded_string

def decryption(encoded_note, key):
    decoded_bytes = base64.b64decode(encoded_note.encode("utf-8"))
    decoded_string = decoded_bytes.decode("utf-8")
    original_note = decoded_string[:-len(key)]
    return original_note

def save_note():
    title = title_entry.get()
    note = note_text.get("1.0", "end-1c")
    user_key = key_entry.get()
    encrypted_note = encryption(note, user_key)
    if len(title) == 0 or len(note) == 0 or len(user_key) == 0:
        messagebox.showerror(title="Error!", message="Please enter all information.")
    else:
        try:
            with open("Secret Notes.txt", "a") as data_file:
                data_file.write(f"\n {title} \n {encrypted_note}")
        except FileNotFoundError:
            with open("Secret Notes.txt", "w") as data_file:
                data_file.write(f"\n {title} \n {encrypted_note}")
        finally:
            title_entry.delete(0, END)
            note_text.delete("1.0", END)
            key_entry.delete(0, END)

def decrypt_notes():
    note = note_text.get("1.0", END)
    user_key = key_entry.get()
    if len(note) == 0 or len(user_key) == 0:
        messagebox.showerror(title="Error!", message="Please enter all information.")
    else:
        try:
            d = decryption(note, user_key)
            note_text.delete("1.0",END)
            note_text.insert("1.0", d)
        except:
            messagebox.showerror(title="Error!", message="Please make sure of encrypted info.")

image= Image.open("secret.jpg")
new_image = image.resize((65,65))
tk_image = ImageTk.PhotoImage(new_image)

image_label = Label(window, image=tk_image)
image_label.pack()

title_label = Label(text="Enter your title",font=("ariel", 10,"bold"))
title_label.config(padx=10, pady=10)
title_label.pack()

title_entry = Entry()
title_entry.config(width=35)
title_entry.pack()

note_label = Label(text="Enter your secret note",font=("ariel", 10,"bold"))
note_label.config(padx=10, pady=10)
note_label.pack()

note_text = Text(width=50, height=15)
note_text.pack()

key_label = Label(text="Enter master key",font=("ariel", 10,"bold"))
key_label.config(padx=10, pady=10)
key_label.pack()

key_entry = Entry()
key_entry.config(width=35)
key_entry.pack()

encryption_button = Button(window, text="Save & Encrypt", command=save_note)
encryption_button.config(padx=3, pady=3)
encryption_button.pack()

decrypt_button = Button(window, text="Decrypt", command=decrypt_notes)
decrypt_button.config(padx=3, pady=3)
decrypt_button.pack()

status_label =Label(text="")
status_label.pack()

window.mainloop()