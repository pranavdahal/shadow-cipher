def aud_steg():
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from PIL import ImageTk, Image

    def encode_aud_data(filename):
        import wave

        nameoffile=filename
        song = wave.open(nameoffile, mode='rb')

        nframes=song.getnframes()
        frames=song.readframes(nframes)
        frame_list=list(frames)
        frame_bytes=bytearray(frame_list)

        data = entry.get()

        res = ''.join(format(i, '08b') for i in bytearray(data, encoding ='utf-8'))     
        print("\nThe string after binary conversion :- " + (res))   
        length = len(res)
        print("\nLength of binary after conversion :- ",length)

        data = data + '*^*^*'

        result = []
        for c in data:
            bits = bin(ord(c))[2:].zfill(8)
            result.extend([int(b) for b in bits])

        j = 0
        for i in range(0,len(result),1): 
            res = bin(frame_bytes[j])[2:].zfill(8)
            if res[len(res)-4]== result[i]:
                frame_bytes[j] = (frame_bytes[j] & 253)      #253: 11111101
            else:
                frame_bytes[j] = (frame_bytes[j] & 253) | 2
                frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
            j = j + 1
        
        frame_modified = bytes(frame_bytes)

        stegofile=filedialog.asksaveasfilename(title="Save audio file", defaultextension=".wav")
        with wave.open(stegofile, 'wb') as fd:
            fd.setparams(song.getparams())
            fd.writeframes(frame_modified)
        print("\nEncoded the data successfully in the audio file.")    
        song.close()

    def decode_aud_data(filename):
        import wave

        nameoffile=filename
        song = wave.open(nameoffile, mode='rb')

        nframes=song.getnframes()
        frames=song.readframes(nframes)
        frame_list=list(frames)
        frame_bytes=bytearray(frame_list)

        extracted = ""
        p=0
        for i in range(len(frame_bytes)):
            if(p==1):
                break
            res = bin(frame_bytes[i])[2:].zfill(8)
            if res[len(res)-2]==0:
                extracted+=res[len(res)-4]
            else:
                extracted+=res[len(res)-1]
        
            all_bytes = [ extracted[i: i+8] for i in range(0, len(extracted), 8) ]
            decoded_data = ""
            for byte in all_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*":
                    messagebox.showinfo("Encoded data ",decoded_data[:-5])
                    print("The Encoded data was :--",decoded_data[:-5])
                    p=1
                    break

    def encode_audio():
        filename = filedialog.askopenfilename(title="Select Audio File")
        if filename:
            try:
                encode_aud_data(filename)
                messagebox.showinfo("Success", "Text message encoded successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def decode_audio():
        filename = filedialog.askopenfilename(title="Select Audio File")
        if filename:
            try:
                decode_aud_data(filename)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("Audio Steganography")
    root.geometry("800x600")

    bg_image = Image.open(r"./icons/back.jpg")
    bg_image = bg_image.resize((800, 600), Image.Resampling.BICUBIC)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_canvas = tk.Canvas(root, width=800, height=600)
    bg_canvas.pack(fill="both", expand=True)

    # Add the image to the Canvas
    bg_canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    title_label = bg_canvas.create_text(400, 50, text="AUDIO STEGANOGRAPHY", font=("Arial", 20, "bold"), fill="white")

    border_frame = tk.Frame(bg_canvas, bg="white", bd=1)
    border_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.5)

    box_frame = tk.Frame(border_frame, bg="black")  # Semi-transparent frame
    box_frame.pack(expand=True, fill="both", padx=2, pady=2)  # Packed inside the border frame

    encode_label = tk.Label(box_frame, text="Enter the data to be Encoded:", font=("Arial", 14), bg="black", fg="white")
    encode_label.pack(padx=(20, 20), pady=(20, 10))

    entry = tk.Entry(box_frame, width=30, font=("Arial", 14), bg="white", fg="black")
    entry.pack(pady=(0, 20), padx=(20, 20))

    def on_enter(e):
        e.widget['background'] = 'grey' 

    def on_leave(e):
        e.widget['background'] = 'black'


    encode_button = tk.Button(box_frame, text="Encode Data", width=25, font=("Arial", 14), command=encode_audio, bg="black", fg="white", highlightbackground="white")
    encode_button.pack(pady=20, padx=(20, 20))
    encode_button.bind("<Enter>", on_enter)
    encode_button.bind("<Leave>", on_leave)

    decode_button = tk.Button(box_frame, text="Decode Data", width=25, font=("Arial", 14), command=decode_audio, bg="black", fg="white", highlightbackground="white")
    decode_button.pack(pady=10, padx=(20, 20))
    decode_button.bind("<Enter>", on_enter)
    decode_button.bind("<Leave>", on_leave)

    root.mainloop()
