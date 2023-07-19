def txt_steg():
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from PIL import ImageTk, Image

    def txt_encode(text,file):
        l=len(text)
        i=0
        add=''
        while i<l:
            t=ord(text[i])
            if(t>=32 and t<=64):
                t1=t+48
                t2=t1^170       #170: 10101010
                res = bin(t2)[2:].zfill(8)
                add+="0011"+res
            
            else:
                t1=t-48
                t2=t1^170
                res = bin(t2)[2:].zfill(8)
                add+="0110"+res
            i+=1
        res1=add+"111111111111"
        print("The string after binary conversion appyling all the transformation :- " + (res1))   
        length = len(res1)
        print("Length of binary after conversion:- ",length)
        HM_SK=""
        ZWC={"00":u'\u200C',"01":u'\u202C',"11":u'\u202D',"10":u'\u200E'}      
        file1 = open(file,"r", encoding="utf-8")

        nameoffile = filedialog.asksaveasfilename(title="Save text file", defaultextension=".txt")
        file3= open(nameoffile,"w+", encoding="utf-8")
        word=[]
        for line in file1: 
            word+=line.split()
        i=0
        while(i<len(res1)):  
            s=word[int(i/12)]
            print(s)
            j=0
            x=""
            HM_SK=""
            while(j<12):
                x=res1[j+i]+res1[i+j+1]
                HM_SK+=ZWC[x]
                j+=2
            s1=s+HM_SK
            file3.write(s1)
            file3.write(" ")
            i+=12
        t=int(len(res1)/12)     
        while t<len(word): 
            file3.write(word[t])
            file3.write(" ")
            t+=1
        # file3.close()  
        # file1.close()
        print("\nStego file has successfully generated")

    def encode_txt_data(data):
        count2=0
        file1 = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        for line in file1: 
            for word in line.split():
                count2=count2+1
        # file1.close()       
        bt=int(count2)
        print("Maximum number of words that can be inserted :- ",int(bt/6))
        text1=data
        l=len(text1)
        if(l<=bt):
            print("\nInputed message can be hidden in the cover file\n")
            txt_encode(text1,file1)
        else:
            print("\nString is too big please reduce string size")
            encode_txt_data()

    def BinaryToDecimal(binary):
        string = int(binary, 2)
        return string

    def decode_txt_data():
        ZWC_reverse={u'\u200C':"00",u'\u202C':"01",u'\u202D':"11",u'\u200E':"10"}
        stego=filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        file4= open(stego,"r", encoding="utf-8")
        temp=''
        for line in file4: 
            for words in line.split():
                T1=words
                binary_extract=""
                for letter in T1:
                    if(letter in ZWC_reverse):
                        binary_extract+=ZWC_reverse[letter]
                if binary_extract=="111111111111":
                    break
                else:
                    temp+=binary_extract
        print("\nEncrypted message presented in code bits:",temp) 
        lengthd = len(temp)
        print("\nLength of encoded bits:- ",lengthd)
        i=0
        a=0
        b=4
        c=4
        d=12
        final=''
        while i<len(temp):
            t3=temp[a:b]
            a+=12
            b+=12
            i+=12
            t4=temp[c:d]
            c+=12
            d+=12
            if(t3=='0110'):
                decimal_data = BinaryToDecimal(t4)
                final+=chr((decimal_data ^ 170) + 48)
            elif(t3=='0011'):
                decimal_data = BinaryToDecimal(t4)
                final+=chr((decimal_data ^ 170) - 48)

        messagebox.showinfo("Encoded data ",final)
        print("\nMessage after decoding from the stego file:- ",final)

    def encode_text():
        data = entry.get()
        try:
            encode_txt_data(data)
            messagebox.showinfo("Success", "Text message encoded successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def decode_text():
        decode_txt_data()

    def exit_program():
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            root.destroy()

    root = tk.Tk()
    root.title("Text Steganography")
    root.geometry("800x600")

    # Load the image
    bg_image = Image.open(r"./icons/back.jpg")
    bg_image = bg_image.resize((800, 600), Image.Resampling.BICUBIC)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a Canvas
    bg_canvas = tk.Canvas(root, width=800, height=600)
    bg_canvas.pack(fill="both", expand=True)

    # Add the image to the Canvas
    bg_canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Add title directly on the canvas
    title_label = bg_canvas.create_text(400, 50, text="TEXT STEGANOGRAPHY", font=("Arial", 20, "bold"), fill="white")

    # Create a larger frame with white color as a border
    border_frame = tk.Frame(bg_canvas, bg="white", bd=1)
    border_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.5)

    box_frame = tk.Frame(border_frame, bg="black")  # Semi-transparent frame
    box_frame.pack(expand=True, fill="both", padx=2, pady=2)  # Packed inside the border frame

    encode_label = tk.Label(box_frame, text="Enter the data to be Encoded:", font=("Arial", 14), bg="black", fg="white")
    encode_label.pack(padx=(20, 20), pady=(20, 10))

    entry = tk.Entry(box_frame, width=30, font=("Arial", 14), bg="white", fg="black")
    entry.pack(pady=(0, 20), padx=(20, 20))

    def on_enter(e):
        e.widget['background'] = 'grey'  # Changes the background color of the widget being hovered over

    def on_leave(e):
        e.widget['background'] = 'black'  # Changes the background color of the widget not being hovered over

    encode_button = tk.Button(box_frame, text="Encode Text", width=25, font=("Arial", 14), command=encode_text, bg="black", fg="white", highlightbackground="white")
    encode_button.pack(pady=20, padx=(20, 20))
    encode_button.bind("<Enter>", on_enter)
    encode_button.bind("<Leave>", on_leave)

    decode_button = tk.Button(box_frame, text="Decode Text", width=25, font=("Arial", 14), command=decode_text, bg="black", fg="white", highlightbackground="white")
    decode_button.pack(pady=10, padx=(20, 20))
    decode_button.bind("<Enter>", on_enter)
    decode_button.bind("<Leave>", on_leave)

    root.mainloop()

