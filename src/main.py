import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class Application:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1920x1080")
        self.master.title("Portrait Grabber by Felix Silva")

        self.cropWidth = 250
        self.cropHeight = 300

        self.currentImage = None
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
        self.canvas.configure(yscrollcommand=self.scrollbar.set, cursor="none")

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        imagePath = filedialog.askdirectory()

        if imagePath:
            # Create "cropped" subfolder if it doesn't exist
            self.croppedFolder = os.path.join(imagePath, "cropped")
            os.makedirs(self.croppedFolder, exist_ok=True)

            self.imagePaths = [os.path.join(imagePath, f) for f in os.listdir(imagePath)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg')) and "cropped" not in f.lower()]
            
            self.currentIndex = 0
            self.showImage(self.imagePaths[self.currentIndex])
        else:
            messagebox.showerror("Error", "No folder selected")
            self.loadButton.pack(padx=400, pady=400)

    def showImage(self, imagePath):
        pilImage = Image.open(imagePath)

        self.currentPilImage = pilImage
        self.currentImage = ImageTk.PhotoImage(pilImage)

        # Display on the canvas
        self.canvas.create_image(0, 0, image=self.currentImage, anchor="nw")

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind("<ButtonPress-1>", self.onPress)
        self.canvas.bind("<Motion>", self.updateCrosshair)

    def updateCrosshair(self, event):
        self.canvas.delete("crosshair")

        yOffset = self.canvas.canvasy(0)

        x = event.x
        y = event.y + yOffset
        
        halfWidth = self.cropWidth // 2
        halfHeight = self.cropHeight // 2

        self.canvas.create_line(x - halfWidth, y, x + halfWidth, y, tags="crosshair", width=3)  # Horizontal line
        self.canvas.create_line(x, y - halfHeight, x, y + halfHeight, tags="crosshair", width=3)  # Vertical line

    def onPress(self, event):
        yOffset = self.canvas.canvasy(0)
        
        x = event.x
        y = event.y + yOffset

        print("Cropping at x:", x, "y:", y)

        # Calculate cropping box
        left = max(x - self.cropWidth // 2, 0)
        upper = max(y - self.cropHeight // 2, 0)
        right = min(x + self.cropWidth // 2, self.currentPilImage.width)
        lower = min(y + self.cropHeight // 2, self.currentPilImage.height)

        croppedImage = self.currentPilImage.crop((left, upper, right, lower))

        # Get original filename without extension
        originalFilename = os.path.basename(self.imagePaths[self.currentIndex])
        nameWithoutExt, ext = os.path.splitext(originalFilename)

        # Save the cropped image with "cropped_" prefix
        savePath = os.path.join(self.croppedFolder, f"cropped_{nameWithoutExt}.png")
        croppedImage.save(savePath)

        print(f"Cropped image saved to: {savePath}")

        # Load next image
        if self.currentIndex < len(self.imagePaths) - 1:
            self.currentIndex += 1
            self.showImage(self.imagePaths[self.currentIndex])
        else:
            messagebox.showinfo("End of Folder", "No more images left.")

root = tk.Tk()
root.title("Portrait Grabber by Felix Silva")
root.state('zoomed')

Application(root)
root.mainloop()
