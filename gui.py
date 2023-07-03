# Importing necessary libraries
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model

# Loading the model
model = load_model('Age_Sex_Detection.h5')

# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title("Age & Sex Detector")
top.configure(background='#CDCDCD')

# Initializing the labels
label1 = Label(top, background='#CDCDCD', font=('arial', 15, "bold"))
label2 = Label(top, background='#CDCDCD', font=('arial', 15, "bold"))
sign_image = Label(top)

# Defining detect function which detects the age and gender of the person in the image using the model
def Detect(file_path):
    global label1, label2
    image = Image.open(file_path).convert('L')  # Convert to grayscale
    image = image.resize((48, 48))  # Resize the image
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=-1)  # Add channel dimension
    image = np.expand_dims(image, axis=0)
    sex_f = ['Male', 'Female']
    pred = model.predict(image)
    age = int(np.round(pred[0][0]))
    sex = int(np.round(pred[1][0]))
    print("Predicted Age is " + str(age))
    print("Predicted Gender is " + sex_f[sex])
    label1.configure(foreground="#011638", text=age)
    label2.configure(foreground="#011638", text=sex_f[sex])



# Defining show detect button function
def show_detect_button(file_path):
    Detect_b = Button(top, text='Detect image', command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background="#364156", foreground="white", font=('arial', 10, 'bold'))
    Detect_b.place(relx=0.79, rely=0.46)

# Defining upload image function
def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), top.winfo_height() / 2.25))
        im = ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text='')
        label2.configure(text='')
        show_detect_button(file_path)
    except:
        pass

upload = Button(top, text="Upload an image", command=upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground="white", font=('arial', 10, 'bold'))
upload.pack(side='bottom', expand=True)

sign_image.pack(side='bottom', expand=True)
label1.pack(side='bottom', expand=True)
label2.pack(side='bottom', expand=True)

heading = Label(top, text='Age & Gender Detector', pady=20, font=('arial', 20, "bold"))
heading.configure(background="#cdcdcd", foreground="#364156")
heading.pack()

top.mainloop()
