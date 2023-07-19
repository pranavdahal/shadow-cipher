def img_steg():
    import tkinter as tk
    from tkinter import filedialog, messagebox
    import cv2
    import numpy as np
    from PIL import ImageTk, Image

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

    def encode_img_data(img, data):
        # data=input("\nEnter the data to be Encoded in Image :")    
        if (len(data) == 0): 
            raise ValueError('Data entered to be encoded is empty')
    
        nameoffile = filedialog.asksaveasfilename(title="Save Stego Image", defaultextension=".png")
        
        no_of_bytes=(img.shape[0] * img.shape[1] * 3) // 8
        
        print("\t\nMaximum bytes to encode in Image :", no_of_bytes)
        
        if(len(data)>no_of_bytes):
            raise ValueError("Insufficient bytes Error, Need Bigger Image or give Less Data !!")
        
        data +='*^*^*'    
        
        binary_data=msgtobinary(data)
        print("\n")
        print(binary_data)
        length_data=len(binary_data)
        
        print("\nThe Length of Binary data",length_data)
        
        index_data = 0
        
        for i in img:
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
        cv2.imwrite(nameoffile,img)
        print("\nEncoded the data successfully in the Image and the image is successfully saved with name ",nameoffile)

    def decode_img_data(img):
        data_binary = ""
        for i in img:
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
                        messagebox.showinfo("Encoded data ",decoded_data[:-5])
                        return 

    def encode_image():
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if image_path:
            image = cv2.imread(image_path)
            data = entry.get()
            try:
                encode_img_data(image, data)
                messagebox.showinfo("Success", "Text message encoded successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def decode_image():
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
        if image_path:
            image = cv2.imread(image_path)
            decode_img_data(image)

    root = tk.Tk()
    root.title("Image Steganography")
    root.geometry("800x600")  # Set a preferred window size

    # Load the image
    bg_image = Image.open(r"./icons/back.jpg")
    bg_image = bg_image.resize((800, 600), Image.Resampling.BICUBIC)  # Resize the image to fit the window
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a Canvas, set its size to the window's size
    bg_canvas = tk.Canvas(root, width=800, height=600)
    bg_canvas.pack(fill="both", expand=True)

    # Add the image to the Canvas
    # bg_canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Add title directly on the canvas
    title_label = bg_canvas.create_text(400, 50, text="IMAGE STEGANOGRAPHY", font=("Arial", 20, "bold"), fill="white")

    # Create a larger frame with white color as a border
    border_frame = tk.Frame(bg_canvas, bg="white",bd=1)
    border_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.5)

    box_frame = tk.Frame(border_frame, bg="black")  # Semi-transparent frame
    box_frame.pack(expand=True, fill="both", padx=2, pady=2)  # Packed inside the border frame

    encode_label = tk.Label(box_frame, text="Enter the data to be Encoded in Image:", font=("Arial", 14), bg="black", fg="white")
    encode_label.pack(padx=(20, 20), pady=(20, 10))  # Add padding to the right

    entry = tk.Entry(box_frame, width=30, font=("Arial", 14), bg="white", fg="black")
    entry.pack(pady=(0, 20), padx=(20, 20))  # Add padding at bottom and sides

    def on_enter(e):
        e.widget['background'] = 'grey'  # Changes the background color of the widget being hovered over

    def on_leave(e):
        e.widget['background'] = 'black'  # Changes the background color of the widget not being hovered over

    encode_button = tk.Button(box_frame, text="Encode Text", width=25, font=("Arial", 14), command=encode_image, bg="black", fg="white", highlightbackground="white")
    encode_button.pack(pady=20, padx=(20, 20))
    encode_button.bind("<Enter>", on_enter)
    encode_button.bind("<Leave>", on_leave)

    decode_button = tk.Button(box_frame, text="Decode Text", width=25, font=("Arial", 14), command=decode_image, bg="black", fg="white", highlightbackground="white")
    decode_button.pack(pady=10, padx=(20, 20))
    decode_button.bind("<Enter>", on_enter)
    decode_button.bind("<Leave>", on_leave)

    root.mainloop()


