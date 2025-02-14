import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class Application:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1920x1080")
        self.master.title("Portrait Grabber by Felix Silva")

        self.cropWidth = 200
        self.cropHeight = 300

        self.current_image = None
        self.currentPilImage = None

        # Load Folder Button
        self.loadButton = tk.Button(
            self.master, text="Load Folder", command=self.loadImages,
            width=20, height=5, font=("Arial", 24, "bold")
        )
        self.loadButton.pack(pady=50, side="top")
        
        
    def loadImages(self):
        self.loadButton.destroy()

        # Create Canvas and Scrollbar for scrolling images
        self.canvas = tk.Canvas(self.master)
        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)

        # Frame inside Canvas (for scrollable content)
        self.scrollableFrame = tk.Frame(self.canvas)
        self.scrollableFrame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollableFrame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        imagePath = filedialog.askdirectory()

        if imagePath:
            self.image_paths = [os.path.join(imagePath, f) for f in os.listdir(imagePath) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.current_index = 0
            self.show_image(self.image_paths[self.current_index])
        else:
            messagebox.showerror("Error", "No folder selected")
            self.loadButton.pack(padx=400, pady=400)


        print(imagePath) # test print

    def show_image(self, image_path):
        pilImage = Image.open(image_path)

        self.currentPilImage = pilImage
        self.current_image = ImageTk.PhotoImage(pilImage)

        # Display on the canvas
        label = tk.Label(self.scrollableFrame, image=self.current_image)
        label.pack()
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onPress(self, event):
        print("x: ", event.x, ", y: ", event.y)

root = tk.Tk()
root.title("Portrait Grabber by Felix Silva")
root.state('zoomed')

Application(root)
root.mainloop()