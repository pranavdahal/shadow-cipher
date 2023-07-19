def vid_steg():
    import tkinter as tk
    from tkinter import ttk
    from PIL import ImageTk, Image
    from tkinter import filedialog, messagebox
    import cv2
    import numpy as np

    def msgtobinary(msg):
            if type(msg) == str:
                # ord() returns ASCII value of a character, 08b to convert to 8bit binary.
                result= ''.join([ format(ord(i), "08b") for i in msg ])

            elif type(msg) == bytes or type(msg) == np.ndarray:
                result= [ format(i, "08b") for i in msg ]
            
            elif type(msg) == int or type(msg) == np.uint8:
                result=format(msg, "08b")

            else:
                raise TypeError("Input type is not supported in this function")
            
            return result

    def KSA(key):
        key_length = len(key)
        S=list(range(256)) 
        j=0
        for i in range(256):
            j=(j+S[i]+key[i % key_length]) % 256
            S[i],S[j]=S[j],S[i]
        return S

    def PRGA(S,n):
        i=0
        j=0
        key=[]
        while n>0:
            n=n-1
            i=(i+1)%256
            j=(j+S[i])%256
            S[i],S[j]=S[j],S[i]
            K=S[(S[i]+S[j])%256]
            key.append(K)
        return key

    def preparing_key_array(s):
        return [ord(c) for c in s]

    def encryption(plaintext):
        # print("Enter the key : ")
        key=entry_key.get()
        key=preparing_key_array(key)

        S=KSA(key)

        keystream=np.array(PRGA(S,len(plaintext)))
        plaintext=np.array([ord(i) for i in plaintext])

        cipher=keystream^plaintext
        ctext=''
        for c in cipher:
            ctext=ctext+chr(c)
        return ctext

    def decryption(ciphertext):
        # print("Enter the key : ")
        key=entry_dec_key.get()
        key=preparing_key_array(key)

        S=KSA(key)

        keystream=np.array(PRGA(S,len(ciphertext)))
        ciphertext=np.array([ord(i) for i in ciphertext])

        decoded=keystream^ciphertext
        dtext=''
        for c in decoded:
            dtext=dtext+chr(c)
        return dtext

    def embed(frame):
        data=entry_data.get()
        data=encryption(data)
        print("The encrypted data is : ",data)
        if (len(data) == 0): 
            raise ValueError('Data entered to be encoded is empty')

        data +='*^*^*'
        
        binary_data=msgtobinary(data)
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
                        messagebox.showinfo("Encoded data ",final_decoded_msg)
                        print("\n\nThe Encoded data which was hidden in the Video was :--\n",final_decoded_msg)
                        return 

    def encode_video():
        filename = filedialog.askopenfilename(title="Select Video File")
        cap=cv2.VideoCapture(filename)
        vidcap = cv2.VideoCapture(filename)    
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frame_width = int(vidcap.get(3))
        frame_height = int(vidcap.get(4))

        size = (frame_width, frame_height)
        out = cv2.VideoWriter('stego_video.mp4',fourcc, 25.0, size)
        max_frame=0;
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            max_frame+=1
        cap.release()
        print("Total number of Frame in selected Video :",max_frame)
        # print("Enter the frame number where you want to embed data : ")
        n=12
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
        
        print("\nEncoded the data successfully in the video file.")

    def decode_video():
        filename = filedialog.askopenfilename(title="Select Video File")
        cap = cv2.VideoCapture(filename)
        max_frame=0;
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            max_frame+=1
        print("Total number of Frame in selected Video : ",max_frame)
        # print("Enter frame number to extract data from : ")
        n=12
        vidcap = cv2.VideoCapture(filename)
        frame_number = 0
        while(vidcap.isOpened()):
            frame_number += 1
            ret, frame = vidcap.read()
            if ret == False:
                break
            if frame_number == n:
                extract(frame)
                return

    def exit_program():
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            root.destroy()

    # root = tk.Tk()
    # root.title("Video Steganography")

    # title_label = tk.Label(root, text="VIDEO STEGANOGRAPHY OPERATIONS", font=("Arial", 16, "bold"))
    # title_label.pack(pady=20)

    # encode_frame = tk.Frame(root)
    # encode_frame.pack(pady=10)

    # encode_label = tk.Label(encode_frame, text="Enter the key:")
    # encode_label.pack(side=tk.LEFT)

    # entry_key = tk.Entry(encode_frame, width=30)
    # entry_key.pack(side=tk.LEFT)

    # encode_frame = tk.Frame(root)
    # encode_frame.pack(pady=10)

    # encode_label = tk.Label(encode_frame, text="Enter the data to encode:")
    # encode_label.pack(side=tk.LEFT)

    # entry_data = tk.Entry(encode_frame, width=30)
    # entry_data.pack(side=tk.LEFT)


    # encode_button = tk.Button(root, text="Encode Text", width=25, command=encode_video)
    # encode_button.pack(pady=10)

    # encode_frame = tk.Frame(root)
    # encode_frame.pack(pady=10)

    # encode_label = tk.Label(encode_frame, text="Enter the key:")
    # encode_label.pack(side=tk.LEFT)

    # entry_dec_key = tk.Entry(encode_frame, width=30)
    # entry_dec_key.pack(side=tk.LEFT)

    # decode_button = tk.Button(root, text="Decode Text", width=25, command=decode_video)
    # decode_button.pack(pady=10)

    # exit_button = tk.Button(root, text="Exit", width=10, command=exit_program)
    # exit_button.pack(pady=20)

    # root.mainloop()

    # root = tk.Tk()
    # root.title("Video Steganography")
    # root.geometry("800x600")

    # bg_image = Image.open(r"./icons/back.jpg")  # Adjust the path according to your project directory
    # bg_image = bg_image.resize((800, 600), Image.Resampling.BICUBIC)
    # bg_photo = ImageTk.PhotoImage(bg_image)

    # bg_canvas = tk.Canvas(root, width=800, height=600)
    # bg_canvas.pack(fill="both", expand=True)
    # bg_canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # bg_canvas.create_text(400, 50, text="VIDEO STEGANOGRAPHY", font=("Arial", 20, "bold"), fill="white")

    # border_frame = tk.Frame(bg_canvas, bg="white", bd=1)
    # border_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.5)

    # box_frame = tk.Frame(border_frame, bg="black")
    # box_frame.pack(expand=True, fill="both", padx=2, pady=2)

    # encode_label = tk.Label(box_frame, text="Enter the key:", font=("Arial", 14), bg="black", fg="white")
    # encode_label.pack(padx=(20, 20), pady=(20, 10))

    # entry_key = tk.Entry(box_frame, width=30, font=("Arial", 14), bg="white", fg="black")
    # entry_key.pack(pady=(0, 20), padx=(20, 20))

    # encode_label = tk.Label(box_frame, text="Enter the data to encode:", font=("Arial", 14), bg="black", fg="white")
    # encode_label.pack(padx=(20, 20), pady=(20, 10))

    # entry_data = tk.Entry(box_frame, width=30, font=("Arial", 14), bg="white", fg="black")
    # entry_data.pack(pady=(0, 20), padx=(20, 20))

    # def on_enter(e):
    #     e.widget['background'] = 'grey'

    # def on_leave(e):
    #     e.widget['background'] = 'black'

    # encode_button = tk.Button(box_frame, text="Encode Text", width=25, font=("Arial", 14), command=encode_video, bg="black", fg="white", highlightbackground="white")
    # encode_button.pack(pady=20, padx=(20, 20))
    # encode_button.bind("<Enter>", on_enter)
    # encode_button.bind("<Leave>", on_leave)

    # encode_label = tk.Label(box_frame, text="Enter the key to decode:", font=("Arial", 14), bg="black", fg="white")
    # encode_label.pack(padx=(20, 20), pady=(20, 10))

    # entry_dec_key = tk.Entry(box_frame, width=30, font=("Arial", 14), bg="white", fg="black")
    # entry_dec_key.pack(pady=(0, 20), padx=(20, 20))

    # decode_button = tk.Button(box_frame, text="Decode Text", width=25, font=("Arial", 14), command=decode_video, bg="black", fg="white", highlightbackground="white")
    # decode_button.pack(pady=20, padx=(20, 20))
    # decode_button.bind("<Enter>", on_enter)
    # decode_button.bind("<Leave>", on_leave)

    # root.mainloop()

    root = tk.Tk()
    root.title("Video Steganography")
    root.geometry("800x600")

    bg_image = Image.open(r"./icons/back.jpg")  # Adjust the path according to your project directory
    bg_image = bg_image.resize((800, 600), Image.Resampling.BICUBIC)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_canvas = tk.Canvas(root, width=800, height=600)
    bg_canvas.pack(fill="both", expand=True)
    bg_canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    bg_canvas.create_text(400, 50, text="VIDEO STEGANOGRAPHY", font=("Arial", 20, "bold"), fill="white")

    border_frame = tk.Frame(bg_canvas, bg="white", bd=1)
    border_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.7)

    box_frame = tk.Frame(border_frame, bg="black")
    box_frame.pack(expand=True, fill="both", padx=2, pady=2)

    # Encode Section

    encode_label = tk.Label(box_frame, text="Encode:", font=("Arial", 14), bg="black", fg="white")
    encode_label.pack(padx=(20, 20), pady=(20, 10))

    entry_key = tk.Entry(box_frame, width=30, font=("Arial", 14), bg="white", fg="black")
    entry_key.pack(pady=(0, 20), padx=(20, 20))

    entry_data = tk.Entry(box_frame, width=30, font=("Arial", 14), bg="white", fg="black")
    entry_data.pack(pady=(0, 20), padx=(20, 20))

    def on_enter(e):
        e.widget['background'] = 'grey'

    def on_leave(e):
        e.widget['background'] = 'black'

    encode_button = tk.Button(box_frame, text="Encode Text", width=25, font=("Arial", 14), command=encode_video, bg="black", fg="white", highlightbackground="white")
    encode_button.pack(pady=20, padx=(20, 20))
    encode_button.bind("<Enter>", on_enter)
    encode_button.bind("<Leave>", on_leave)

    # Separator
    ttk.Separator(box_frame, orient='horizontal').pack(fill='x')

    # Decode Section

    decode_label = tk.Label(box_frame, text="Decode:", font=("Arial", 14), bg="black", fg="white")
    decode_label.pack(padx=(20, 20), pady=(20, 10))

    entry_dec_key = tk.Entry(box_frame, width=30, font=("Arial", 14), bg="white", fg="black")
    entry_dec_key.pack(pady=(0, 20), padx=(20, 20))

    decode_button = tk.Button(box_frame, text="Decode Text", width=25, font=("Arial", 14), command=decode_video, bg="black", fg="white", highlightbackground="white")
    decode_button.pack(pady=20, padx=(20, 20))
    decode_button.bind("<Enter>", on_enter)
    decode_button.bind("<Leave>", on_leave)

    root.mainloop()