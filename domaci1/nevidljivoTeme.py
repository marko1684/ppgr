import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def cross(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    
    cross_x = y1 * z2 - z1 * y2  
    cross_y = z1 * x2 - x1 * z2  
    cross_z = x1 * y2 - y1 * x2  
    
    return (cross_x, cross_y, cross_z)  

def calculate_missing_point(points):

    points = [p for p in points if p is not None]

    if len(points) < 7:
        return None

    Xb = cross(cross(points[1], points[4]), cross(points[0], points[3]))
    Yb = cross(cross(points[3], points[4]), cross(points[5], points[6]))

    missing_point = cross(cross(points[6], Xb), cross(points[2], Yb))

    return missing_point

class CubePointSelector:
    def __init__(self, master):
        self.master = master
        self.points = [None] * 8 
        self.image_path = None
        self.original_image = None
        self.image = None
        self.scale_x = 1
        self.scale_y = 1
        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.load_button = tk.Button(master, text="Load Image", command=self.load_image)
        self.load_button.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.scale_x = 800 / self.original_image.width
            self.scale_y = 600 / self.original_image.height
            self.image = self.original_image.resize((800, 600), Image.ANTIALIAS)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

    def on_click(self, event):
        original_x = event.x / self.scale_x
        original_y = event.y / self.scale_y
        z_coord = 1

        if None in self.points:
            index = self.points.index(None)
            self.points[index] = (original_x, original_y, z_coord)
            print(f"Point {index + 1}: ({original_x:.2f}, {original_y:.2f}, {z_coord})")
            self.canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill='red')
            self.canvas.create_text(event.x, event.y-10, text=f"({original_x:.2f}, {original_y:.2f}, {z_coord})", fill='white')

            if self.points.count(None) == 1:
                missing_point = calculate_missing_point(self.points)
                print(f"Missing Point: {missing_point}")
                if missing_point:
                    self.points[self.points.index(None)] = missing_point
                    missing_point = (missing_point[0] / missing_point[2], missing_point[1] / missing_point[2], 1)
                    canvas_x = missing_point[0] * self.scale_x
                    canvas_y = missing_point[1] * self.scale_y
                    self.canvas.create_oval(canvas_x-5, canvas_y-5, canvas_x+5, canvas_y+5, fill='blue')
                    self.canvas.create_text(canvas_x, canvas_y-10, text=f"({missing_point[0]:.2f}, {missing_point[1]:.2f}, {missing_point[2]:.2f})", fill='blue')

root = tk.Tk()
app = CubePointSelector(root)
root.mainloop()
