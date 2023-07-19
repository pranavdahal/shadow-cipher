import tkinter as tk
from PIL import ImageTk, Image
from image import img_steg
from text import txt_steg
from audio import aud_steg
from video import vid_steg

root = tk.Tk()
root.title("Steganography")
root.geometry("1920x1080")
root.configure(bg="black")

title_label = tk.Label(root, text="STEGANOGRAPHY", font=("Arial",20 , "bold"), bg="black", fg="white")
title_label.pack(pady=(30, 5))

description_label = tk.Label(root, text="Hide your content securely and safely.", font=("Arial", 14), bg="black", fg="white")
description_label.pack(pady=10)

button_frame = tk.Frame(root, bg="black")
button_frame.pack()

def create_custom_button(frame, img_path, description, command):
    img = Image.open(img_path)
    img = img.resize((250, 250), Image.Resampling.BICUBIC)
    photo = ImageTk.PhotoImage(img)

    canvas = tk.Canvas(frame, width=650, height=250, bg="black", highlightthickness=1, highlightbackground="white")
    canvas.image = photo
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    header_font = ("Arial", 20, "bold")
    content_font = ("Arial", 12)
    header, content = description.split("\n", 1)

    header_item = canvas.create_text(260, 30, anchor=tk.NW, text=header, font=header_font, fill="white")
    content_item = canvas.create_text(260, 60, anchor=tk.NW, text=content, font=content_font, fill="white")

    def on_enter(event):
        canvas.itemconfig(header_item, fill='black')
        canvas.itemconfig(content_item, fill='black')
        canvas.config(bg='white')

    def on_leave(event):
        canvas.itemconfig(header_item, fill='white')
        canvas.itemconfig(content_item, fill='white')
        canvas.config(bg='black')

    # mouse events
    canvas.bind("<Button-1>", lambda event: command()) 
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)

    return canvas

img_button = create_custom_button(button_frame, r".\icons\image.png", "IMAGE STEGANOGRAPHY \n Hide your content inside an image.\n Extract the hidden content in image.\n Click to Explore.", img_steg)
txt_button = create_custom_button(button_frame, r".\icons\text.jpg", "TEXT STEGANOGRAPHY \n Hide your content inside a text file.\n Extract the hidden content in the text.\n Click to Explore.", txt_steg)
aud_button = create_custom_button(button_frame, r".\icons\audio.jpg", "AUDIO STEGANOGRAPHY \n Hide your content inside an audio.\n Extract the hidden content in an audio.\n Click to Explore.", aud_steg)
vid_button = create_custom_button(button_frame, r".\icons\video.png", "VIDEO STEGANOGRAPHY \n Hide your content inside a video.\n Extract the hidden content in a video.\n Click to Explore.", vid_steg)

img_button.grid(row=0, column=0, padx=20, pady=20)
txt_button.grid(row=0, column=1, padx=20, pady=20)
aud_button.grid(row=1, column=0, padx=20, pady=20)
vid_button.grid(row=1, column=1, padx=20, pady=20)

root.mainloop()
