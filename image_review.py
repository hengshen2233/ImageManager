import tkinter as tk
from PIL import Image, ImageTk
import os

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("图片像素坐标查看器")
        
        self.label_frame = tk.Frame(root, padx=10, pady=10)
        self.label_frame.pack()
        
        self.path_label = tk.Label(self.label_frame, text="请输入图片完整路径:")
        self.path_label.pack(side=tk.LEFT)
        
        self.path_entry = tk.Entry(self.label_frame, width=80)
        self.path_entry.pack(side=tk.LEFT, padx=5)
        self.path_entry.bind('<Return>', self.load_image)
        
        self.load_button = tk.Button(self.label_frame, text="加载图片", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack()
        
        self.canvas = tk.Canvas(self.canvas_frame)
        self.canvas.pack()
        
        self.coord_label = tk.Label(root, text="坐标: (0, 0)", font=("Arial", 12))
        self.coord_label.pack(pady=10)
        
        self.canvas.bind('<Motion>', self.show_coordinates)
        
        self.image = None
        self.tk_image = None
    
    def load_image(self, event=None):
        path = self.path_entry.get().strip()
        
        if not path:
            tk.messagebox.showwarning("警告", "请输入图片路径")
            return
        
        if not os.path.exists(path):
            tk.messagebox.showerror("错误", "文件不存在")
            return
        
        try:
            self.image = Image.open(path)
            self.tk_image = ImageTk.PhotoImage(self.image)
            
            self.canvas.config(width=self.tk_image.width(), height=self.tk_image.height())
            self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)
            
            self.root.geometry(f"{self.tk_image.width() + 50}x{self.tk_image.height() + 100}")
        except Exception as e:
            tk.messagebox.showerror("错误", f"无法加载图片: {str(e)}")
    
    def show_coordinates(self, event):
        x = event.x
        y = event.y
        
        if self.image:
            if 0 <= x < self.image.width and 0 <= y < self.image.height:
                self.coord_label.config(text=f"坐标: ({x}, {y})")
            else:
                self.coord_label.config(text="坐标: (超出范围)")
        else:
            self.coord_label.config(text=f"坐标: ({x}, {y})")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()