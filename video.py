def vid_steg(): 
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from PIL import ImageTk, Image
    import numpy as np
    import cv2

    def msgtobinary(msg):
        if type(msg) == str:
            result = ''.join([ format(ord(i), "08b") for i in msg ])
        elif type(msg) == bytes or type(msg) == np.ndarray:
            result = [ format(i, "08b") for i in msg ]
        elif type(msg) == int or type(msg) == np.uint8:
            result = format(msg, "08b")
        else:
            raise TypeError("Input type is not supported in this function")
        return result

    def KSA(key):
        key_length = len(key)
        S = list(range(256)) 
        j = 0
        for i in range(256):
            j = (j+S[i]+key[i % key_length]) % 256
            S[i],S[j] = S[j],S[i]
        return S

    def PRGA(S, n):
        i = 0
        j = 0
        key = []
        while n > 0:
            n = n - 1
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i],S[j] = S[j],S[i]
            K = S[(S[i] + S[j]) % 256]
            key.append(K)
        return key

    def preparing_key_array(s):
        return [ord(c) for c in s]

    def encryption(plaintext):
        key = key_entry.get()
        key = preparing_key_array(key)

        S = KSA(key)

        keystream = np.array(PRGA(S, len(plaintext)))
        plaintext = np.array([ord(i) for i in plaintext])

        cipher = keystream ^ plaintext
        ctext = ''
        for c in cipher:
            ctext = ctext + chr(c)
        return ctext

    def decryption(ciphertext):
        key = key_entry.get()
        key = preparing_key_array(key)

        S = KSA(key)

        keystream = np.array(PRGA(S, len(ciphertext)))
        ciphertext = np.array([ord(i) for i in ciphertext])

        decoded = keystream ^ ciphertext
        dtext = ''
        for c in decoded:
            dtext = dtext + chr(c)
        return dtext

    def embed(frame):
        data = data_entry.get()
        data = encryption(data)
        if (len(data) == 0): 
            raise ValueError('Data is empty')

        data += '*^*^*'
        
        binary_data = msgtobinary(data)
        length_data = len(binary_data)
        
        index_data = 0
        
        for i in frame:
            for pixel in i:
                r, g, b = msgtobinary(pixel)
                if index_data < length_data:
                    pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                    index_data += 1
                if index_data < length_data:
                    pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                    index_data += 1
                if index_data < length_data:
                    pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                    index_data += 1
                if index_data >= length_data:
                    break
        return frame

    def extract(frame):
        data_binary = ""
        final_decoded_msg = ""
        for i in frame:
            for pixel in i:
                r, g, b = msgtobinary(pixel) 
                data_binary += r[-1]  
                data_binary += g[-1]  
                data_binary += b[-1]  
                total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
                decoded_data = ""
                for byte in total_bytes:
                    decoded_data += chr(int(byte, 2))
                    if decoded_data[-5:] == "*^*^*": 
                        for i in range(0,len(decoded_data)-5):
                            final_decoded_msg += decoded_data[i]
                        final_decoded_msg = decryption(final_decoded_msg)
                        messagebox.showinfo("Encoded data",final_decoded_msg)
                        return 

    def encode_video():
        video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
        cap=cv2.VideoCapture(video_path)
        vidcap = cv2.VideoCapture(video_path)    
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frame_width = int(vidcap.get(3))
        frame_height = int(vidcap.get(4))

        size = (frame_width, frame_height)
        out = cv2.VideoWriter('stego_video.mp4',fourcc, 25.0, size)
        max_frame=0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            max_frame+=1
        cap.release()
        n = int(frame_entry.get())
        frame_number = 0
        while(vidcap.isOpened()):
            frame_number += 1
            ret, frame = vidcap.read()
            if ret == False:
                break
            if frame_number == n:    
                change_frame_with = embed(frame)
                frame_ = change_frame_with
                frame = change_frame_with
            out.write(frame)
        
        messagebox.showinfo("Success", "Data encoded successfully in the video file.")
        return frame_

    def decode_video(frame_):
        cap = cv2.VideoCapture('stego_video.mp4')
        max_frame=0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            max_frame+=1
        n = int(frame_entry.get())
        vidcap = cv2.VideoCapture('stego_video.mp4')
        frame_number = 0
        while(vidcap.isOpened()):
            frame_number += 1
            ret, frame = vidcap.read()
            if ret == False:
                break
            if frame_number == n:
                extract(frame_)
                return

    root = tk.Toplevel()
    root.title("Video Steganography")
    root.geometry("800x600")

    bg_image = Image.open(r"./icons/back.jpg")
    bg_image = bg_image.resize((800, 600), Image.Resampling.BICUBIC)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_canvas = tk.Canvas(root, width=800, height=600)
    bg_canvas.pack(fill="both", expand=True)

    bg_canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    title_label = bg_canvas.create_text(400, 50, text="VIDEO STEGANOGRAPHY", font=("Arial", 20, "bold"), fill="white")

    border_frame = tk.Frame(bg_canvas, bg="white", bd=1)
    border_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.5)

    box_frame = tk.Frame(border_frame, bg="black")
    box_frame.pack(expand=True, fill="both", padx=2, pady=2)

    data_entry = tk.Entry(box_frame, width=30, font=("Arial", 14), bg="white", fg="black")
    data_entry.pack(pady=(0, 20))

    key_entry = tk.Entry(box_frame, width=30, font=("Arial", 14), bg="white", fg="black")
    key_entry.pack(pady=(0, 20))

    frame_entry = tk.Entry(box_frame, width=30, font=("Arial", 14), bg="white", fg="black")
    frame_entry.pack(pady=(0, 20))

    encode_button = tk.Button(box_frame, text="Encode Video", width=25, font=("Arial", 14), command=encode_video, bg="black", fg="white")
    encode_button.pack(pady=20)

    decode_button = tk.Button(box_frame, text="Decode Video", width=25, font=("Arial", 14), command=lambda: decode_video(frame_entry), bg="black", fg="white")
    decode_button.pack(pady=20)

    root.mainloop()
