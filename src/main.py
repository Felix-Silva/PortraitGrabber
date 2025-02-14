import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class Application:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1920x1080")
        self.master.title("Portrait Grabber by Felix Silva")

        self.cropWidth = 200
        self.cropHeight = 300

        self.currentImage = None
        self.currentPilImage = None

        self.loadButton = tk.Button(self.master, text="Load Folder", command=self.loadImages, width=300, height=250, font=("Arial", 42, "bold"))
        self.loadButton.pack(padx=400, pady=400)
        
    def loadImages(self):
        path = filedialog.askdirectory()
        print(path) # test print

root = tk.Tk()
root.title("Portrait Grabber by Felix Silva")
root.state('zoomed')
Application(root)
root.mainloop()