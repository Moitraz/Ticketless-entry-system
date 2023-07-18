import cv2 as cv
from pyzbar.pyzbar import decode
import time
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
from PIL import ImageFilter

customtkinter.set_appearance_mode("dark")


class App(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self, val, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("CustomTkinter example_background_image.py")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        
        img = Image.open("S:\PG\hackathon\monuments.jpg")    
        self.bg_image = customtkinter.CTkImage(img,
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        self.result_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.result_frame.grid(row=0, column=0, sticky="ns")
        self.result_label = customtkinter.CTkLabel(self.result_frame, text=val,
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.result_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        self.result_button = customtkinter.CTkButton(self.result_frame, text="Done", command=self.result_event, width=200)
        self.result_button.grid(row=3, column=0, padx=30, pady=(15, 15))

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def result_event(self):
        self.destroy()

cam = cv.VideoCapture(0)
cam.set(5, 640)
cam.set(6, 480)
camera = True

while camera == True : 
    success, frame = cam.read()

    for i in decode(frame):
        val = i.data.decode('utf-8')
        if __name__ == "__main__":
            app = App(val)
            app.mainloop()

    cv.imshow("the_code", frame)
    cv.waitKey(1)