import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont
import platform

class ImageManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片管理器")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        # 设置窗口居中
        self.center_window(500, 500)
        
        # 创建主界面
        self.create_main_ui()
    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_main_ui(self):
        # 标题
        title_label = tk.Label(self.root, text="图片管理器", font=("微软雅黑", 20, "bold"), pady=20)
        title_label.pack()
        
        # 功能按钮框架
        button_frame = tk.Frame(self.root, padx=20, pady=20)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # 按钮样式
        button_style = {"font": ("微软雅黑", 14), "width": 20, "height": 2}
        
        # 四个功能按钮
        self.btn_view = tk.Button(button_frame, text="查看图片", command=self.open_view_image, **button_style)
        self.btn_view.pack(pady=10)
        
        self.btn_resize = tk.Button(button_frame, text="调整尺寸", command=self.open_resize_image, **button_style)
        self.btn_resize.pack(pady=10)
        
        self.btn_add_text = tk.Button(button_frame, text="添加文字", command=self.open_add_text, **button_style)
        self.btn_add_text.pack(pady=10)
        
        self.btn_composite = tk.Button(button_frame, text="图片合成", command=self.open_composite_image, **button_style)
        self.btn_composite.pack(pady=10)
    
    def open_view_image(self):
        ViewImageWindow(self.root)
    
    def open_resize_image(self):
        ResizeImageWindow(self.root)
    
    def open_add_text(self):
        AddTextWindow(self.root)
    
    def open_composite_image(self):
        CompositeImageWindow(self.root)

class ViewImageWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("图片像素坐标查看器")
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.center_window(600, 500)
        
        self.image = None
        self.tk_image = None
        self.original_width = 0
        self.original_height = 0
        self.scale_ratio = 1.0
        self.image_offset_x = 0
        self.image_offset_y = 0
        
        # 路径输入
        path_frame = tk.Frame(self.window, padx=10, pady=10)
        path_frame.pack(fill=tk.X)
        
        tk.Label(path_frame, text="图片路径:").pack(side=tk.LEFT)
        self.path_entry = tk.Entry(path_frame, width=50)
        self.path_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = tk.Button(path_frame, text="浏览", command=self.browse_image)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        load_btn = tk.Button(path_frame, text="加载", command=self.load_image)
        load_btn.pack(side=tk.LEFT, padx=5)
        
        # 画布区域
        self.canvas = tk.Canvas(self.window, bg="#f0f0f0")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 坐标显示
        self.coord_label = tk.Label(self.window, text="坐标: (0, 0)", font=("Arial", 12))
        self.coord_label.pack(pady=5)
        
        self.canvas.bind('<Motion>', self.show_coordinates)
    
    def browse_image(self):
        path = filedialog.askopenfilename(filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
    
    def load_image(self):
        path = self.path_entry.get().strip()
        
        if not path:
            messagebox.showwarning("警告", "请输入图片路径")
            return
        
        if not os.path.exists(path):
            messagebox.showerror("错误", "文件不存在")
            return
        
        try:
            original_image = Image.open(path)
            self.original_width, self.original_height = original_image.size
            # 调整图片大小以适应窗口
            max_width, max_height = 550, 380
            width, height = original_image.size
            
            if width > max_width or height > max_height:
                self.scale_ratio = min(max_width/width, max_height/height)
                width = int(width * self.scale_ratio)
                height = int(height * self.scale_ratio)
                self.image = original_image.resize((width, height), Image.Resampling.LANCZOS)
            else:
                self.scale_ratio = 1.0
                self.image = original_image
            
            self.tk_image = ImageTk.PhotoImage(self.image)
            
            # 设置窗口尺寸，确保最小尺寸为600x500
            window_width = max(self.tk_image.width() + 50, 600)
            window_height = max(self.tk_image.height() + 120, 500)
            self.window.geometry(f"{window_width}x{window_height}")
            
            # 让画布充满可用空间
            self.canvas.config(width=window_width - 50, height=window_height - 120)
            
            # 计算图片居中位置
            canvas_width = self.canvas.winfo_reqwidth()
            canvas_height = self.canvas.winfo_reqheight()
            self.image_offset_x = (canvas_width - self.tk_image.width()) // 2
            self.image_offset_y = (canvas_height - self.tk_image.height()) // 2
            
            # 清空画布并居中绘制图片
            self.canvas.delete("all")
            self.canvas.create_image(self.image_offset_x, self.image_offset_y, image=self.tk_image, anchor=tk.NW)
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片: {str(e)}")
    
    def show_coordinates(self, event):
        x = event.x
        y = event.y
        
        if self.image:
            # 减去图片偏移量得到相对于图片的坐标
            img_x = x - self.image_offset_x
            img_y = y - self.image_offset_y
            
            if 0 <= img_x < self.image.width and 0 <= img_y < self.image.height:
                # 将缩放后的坐标转换为原图坐标
                original_x = int(img_x / self.scale_ratio)
                original_y = int(img_y / self.scale_ratio)
                self.coord_label.config(text=f"坐标: ({original_x}/{self.original_width}, {original_y}/{self.original_height})")
            else:
                self.coord_label.config(text="坐标: (超出范围)")
        else:
            self.coord_label.config(text=f"坐标: ({x}, {y})")
    
    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")

class ResizeImageWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("图片尺寸调整")
        self.window.geometry("450x300")
        self.window.transient(parent)
        self.center_window(450, 300)
        
        # 输入路径
        path_frame = tk.Frame(self.window, padx=10, pady=10)
        path_frame.pack(fill=tk.X)
        
        tk.Label(path_frame, text="图片/文件夹路径:").pack(side=tk.LEFT)
        self.path_entry = tk.Entry(path_frame, width=30)
        self.path_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = tk.Button(path_frame, text="浏览", command=self.browse_path)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # 尺寸设置
        size_frame = tk.Frame(self.window, padx=10, pady=5)
        size_frame.pack(fill=tk.X)
        
        tk.Label(size_frame, text="目标宽度:").pack(side=tk.LEFT)
        self.width_entry = tk.Entry(size_frame, width=10)
        self.width_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(size_frame, text="像素").pack(side=tk.LEFT)
        
        tk.Label(size_frame, text="目标高度:").pack(side=tk.LEFT, padx=10)
        self.height_entry = tk.Entry(size_frame, width=10)
        self.height_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(size_frame, text="像素").pack(side=tk.LEFT)
        
        # 质量设置
        quality_frame = tk.Frame(self.window, padx=10, pady=5)
        quality_frame.pack(fill=tk.X)
        
        tk.Label(quality_frame, text="图片质量:").pack(side=tk.LEFT)
        self.quality_entry = tk.Entry(quality_frame, width=10)
        self.quality_entry.insert(0, "95")
        self.quality_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(quality_frame, text="(1-100)").pack(side=tk.LEFT)
        
        # 进度条
        self.progress = ttk.Progressbar(self.window, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=10, padx=10)
        
        # 处理按钮
        process_btn = tk.Button(self.window, text="开始处理", command=self.process_images, width=20, font=("微软雅黑", 12))
        process_btn.pack(pady=10)
        
        # 状态标签
        self.status_label = tk.Label(self.window, text="", fg="green")
        self.status_label.pack()
    
    def browse_path(self):
        path = filedialog.askopenfilename(filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
    
    def process_images(self):
        input_path = self.path_entry.get().strip()
        if not input_path or not os.path.exists(input_path):
            messagebox.showerror("错误", "请输入有效的路径")
            return
        
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            quality = int(self.quality_entry.get())
            
            if width <= 0 or height <= 0:
                messagebox.showerror("错误", "尺寸必须大于0")
                return
            
            if quality < 1 or quality > 100:
                messagebox.showerror("错误", "质量必须在1-100之间")
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return
        
        supported_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
        
        if os.path.isfile(input_path):
            if input_path.lower().endswith(supported_formats):
                image_files = [os.path.basename(input_path)]
                output_dir = os.path.dirname(input_path)
            else:
                messagebox.showerror("错误", "不支持的图片格式")
                return
        else:
            image_files = [f for f in os.listdir(input_path) 
                          if os.path.isfile(os.path.join(input_path, f)) 
                          and f.lower().endswith(supported_formats)]
            output_dir = input_path
        
        if not image_files:
            messagebox.showwarning("警告", "未找到图片文件")
            return
        
        total = len(image_files)
        self.progress['maximum'] = total
        self.progress['value'] = 0
        
        for i, filename in enumerate(image_files):
            try:
                full_path = os.path.join(output_dir, filename) if os.path.isdir(input_path) else input_path
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(output_dir, f"{name}_像素调整{ext}")
                
                with Image.open(full_path) as img:
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                    
                    if img.mode == 'RGBA' and ext.lower() in ('.jpg', '.jpeg'):
                        img = img.convert('RGB')
                    
                    img.save(output_path, quality=quality)
                
                self.progress['value'] = i + 1
                self.window.update_idletasks()
            except Exception as e:
                messagebox.showerror("错误", f"处理 {filename} 时出错: {str(e)}")
        
        self.status_label.config(text=f"处理完成！共处理 {total} 张图片")
        messagebox.showinfo("完成", f"处理完成！共处理 {total} 张图片")
    
    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")

class AddTextWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("图片添加文字")
        self.window.geometry("500x400")
        self.window.transient(parent)
        self.center_window(500, 400)
        
        # 路径选择
        path_frame = tk.Frame(self.window, padx=10, pady=10)
        path_frame.pack(fill=tk.X)
        
        tk.Label(path_frame, text="图片/文件夹路径:").pack(side=tk.LEFT)
        self.path_entry = tk.Entry(path_frame, width=35)
        self.path_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = tk.Button(path_frame, text="浏览", command=self.browse_path)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # 文字内容
        text_frame = tk.Frame(self.window, padx=10, pady=5)
        text_frame.pack(fill=tk.X)
        
        tk.Label(text_frame, text="文字内容:").pack(side=tk.LEFT)
        self.text_entry = tk.Entry(text_frame, width=40)
        self.text_entry.pack(side=tk.LEFT, padx=5)
        
        # 位置设置
        pos_frame = tk.Frame(self.window, padx=10, pady=5)
        pos_frame.pack(fill=tk.X)
        
        tk.Label(pos_frame, text="X坐标:").pack(side=tk.LEFT)
        self.x_entry = tk.Entry(pos_frame, width=8)
        self.x_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(pos_frame, text="Y坐标:").pack(side=tk.LEFT, padx=10)
        self.y_entry = tk.Entry(pos_frame, width=8)
        self.y_entry.pack(side=tk.LEFT, padx=5)
        
        # 字体设置
        font_frame = tk.Frame(self.window, padx=10, pady=5)
        font_frame.pack(fill=tk.X)
        
        tk.Label(font_frame, text="字体:").pack(side=tk.LEFT)
        self.font_var = tk.StringVar(value="黑体")
        font_options = ["宋体", "黑体", "微软雅黑", "楷体", "仿宋", "隶书", "幼圆"]
        self.font_combo = ttk.Combobox(font_frame, textvariable=self.font_var, values=font_options, width=10)
        self.font_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Label(font_frame, text="字号:").pack(side=tk.LEFT, padx=10)
        self.fontsize_entry = tk.Entry(font_frame, width=8)
        self.fontsize_entry.insert(0, "16")
        self.fontsize_entry.pack(side=tk.LEFT, padx=5)
        
        # 旋转角度
        rotate_frame = tk.Frame(self.window, padx=10, pady=5)
        rotate_frame.pack(fill=tk.X)
        
        tk.Label(rotate_frame, text="旋转角度:").pack(side=tk.LEFT)
        self.rotate_entry = tk.Entry(rotate_frame, width=8)
        self.rotate_entry.insert(0, "0")
        self.rotate_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(rotate_frame, text="度").pack(side=tk.LEFT)
        
        # 进度条
        self.progress = ttk.Progressbar(self.window, orient=tk.HORIZONTAL, length=450, mode='determinate')
        self.progress.pack(pady=10, padx=10)
        
        # 处理按钮
        process_btn = tk.Button(self.window, text="开始处理", command=self.process_images, width=20, font=("微软雅黑", 12))
        process_btn.pack(pady=10)
        
        # 状态标签
        self.status_label = tk.Label(self.window, text="", fg="green")
        self.status_label.pack()
    
    def browse_path(self):
        path = filedialog.askopenfilename(filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
    
    def get_system_font_path(self):
        system = platform.system()
        if system == "Windows":
            return os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
        elif system == "Darwin":
            return "/System/Library/Fonts"
        else:
            return "/usr/share/fonts"
    
    def load_font(self, font_name, font_size):
        font_mapping = {
            "宋体": "simsun.ttc",
            "黑体": "simhei.ttf",
            "微软雅黑": "msyh.ttc",
            "楷体": "simkai.ttf",
            "仿宋": "simfang.ttf",
            "隶书": "simli.ttf",
            "幼圆": "youyuan.ttf"
        }
        
        font_dir = self.get_system_font_path()
        font_candidates = []
        
        if font_name in font_mapping:
            font_candidates.append(os.path.join(font_dir, font_mapping[font_name]))
        else:
            font_candidates.append(os.path.join(font_dir, f"{font_name}.ttf"))
            font_candidates.append(os.path.join(font_dir, f"{font_name}.ttc"))
        
        default_fonts = ["simhei.ttf", "simsun.ttc", "msyh.ttc", "simkai.ttf"]
        for df in default_fonts:
            font_candidates.append(os.path.join(font_dir, df))
        
        font = None
        for font_path in font_candidates:
            try:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                    break
            except Exception:
                continue
        
        if font is None:
            font = ImageFont.load_default()
        
        return font
    
    def process_images(self):
        input_path = self.path_entry.get().strip()
        text = self.text_entry.get().strip()
        
        if not input_path or not os.path.exists(input_path):
            messagebox.showerror("错误", "请输入有效的路径")
            return
        
        if not text:
            messagebox.showerror("错误", "文字内容不能为空")
            return
        
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            font_size = int(self.fontsize_entry.get())
            rotation = int(self.rotate_entry.get())
            
            if font_size <= 0:
                messagebox.showerror("错误", "字号必须大于0")
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return
        
        font_name = self.font_var.get()
        font = self.load_font(font_name, font_size)
        
        supported_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
        
        if os.path.isfile(input_path):
            if input_path.lower().endswith(supported_formats):
                image_files = [os.path.basename(input_path)]
                output_dir = os.path.dirname(input_path)
            else:
                messagebox.showerror("错误", "不支持的图片格式")
                return
        else:
            image_files = [f for f in os.listdir(input_path) 
                          if os.path.isfile(os.path.join(input_path, f)) 
                          and f.lower().endswith(supported_formats)]
            output_dir = input_path
        
        if not image_files:
            messagebox.showwarning("警告", "未找到图片文件")
            return
        
        total = len(image_files)
        self.progress['maximum'] = total
        self.progress['value'] = 0
        
        for i, filename in enumerate(image_files):
            try:
                full_path = os.path.join(output_dir, filename) if os.path.isdir(input_path) else input_path
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(output_dir, f"{name}_添加文字{ext}")
                
                img = Image.open(full_path)
                draw = ImageDraw.Draw(img)
                
                if rotation != 0:
                    text_img = Image.new('RGBA', (img.width, img.height), (255, 255, 255, 0))
                    text_draw = ImageDraw.Draw(text_img)
                    text_draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))
                    text_img = text_img.rotate(rotation, expand=True)
                    img.paste(text_img, (0, 0), text_img)
                else:
                    draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))
                
                img.save(output_path)
                
                self.progress['value'] = i + 1
                self.window.update_idletasks()
            except Exception as e:
                messagebox.showerror("错误", f"处理 {filename} 时出错: {str(e)}")
        
        self.status_label.config(text=f"处理完成！共处理 {total} 张图片")
        messagebox.showinfo("完成", f"处理完成！共处理 {total} 张图片")
    
    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")

class CompositeImageWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("图片合成")
        self.window.geometry("500x350")
        self.window.transient(parent)
        self.center_window(500, 350)
        
        # 底图路径
        base_frame = tk.Frame(self.window, padx=10, pady=10)
        base_frame.pack(fill=tk.X)
        
        tk.Label(base_frame, text="底图路径:").pack(side=tk.LEFT)
        self.base_entry = tk.Entry(base_frame, width=35)
        self.base_entry.pack(side=tk.LEFT, padx=5)
        
        base_browse_btn = tk.Button(base_frame, text="浏览", command=self.browse_base_image)
        base_browse_btn.pack(side=tk.LEFT, padx=5)
        
        # 贴图路径
        overlay_frame = tk.Frame(self.window, padx=10, pady=5)
        overlay_frame.pack(fill=tk.X)
        
        tk.Label(overlay_frame, text="贴图路径:").pack(side=tk.LEFT)
        self.overlay_entry = tk.Entry(overlay_frame, width=35)
        self.overlay_entry.pack(side=tk.LEFT, padx=5)
        
        overlay_browse_btn = tk.Button(overlay_frame, text="浏览", command=self.browse_overlay_image)
        overlay_browse_btn.pack(side=tk.LEFT, padx=5)
        
        # 位置设置
        pos_frame = tk.Frame(self.window, padx=10, pady=5)
        pos_frame.pack(fill=tk.X)
        
        tk.Label(pos_frame, text="起点X坐标:").pack(side=tk.LEFT)
        self.x_entry = tk.Entry(pos_frame, width=8)
        self.x_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(pos_frame, text="起点Y坐标:").pack(side=tk.LEFT, padx=10)
        self.y_entry = tk.Entry(pos_frame, width=8)
        self.y_entry.pack(side=tk.LEFT, padx=5)
        
        # 终点坐标
        end_pos_frame = tk.Frame(self.window, padx=10, pady=5)
        end_pos_frame.pack(fill=tk.X)
        
        tk.Label(end_pos_frame, text="终点X坐标:").pack(side=tk.LEFT)
        self.end_x_entry = tk.Entry(end_pos_frame, width=8)
        self.end_x_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(end_pos_frame, text="终点Y坐标:").pack(side=tk.LEFT, padx=10)
        self.end_y_entry = tk.Entry(end_pos_frame, width=8)
        self.end_y_entry.pack(side=tk.LEFT, padx=5)
        
        # 旋转角度
        rotate_frame = tk.Frame(self.window, padx=10, pady=5)
        rotate_frame.pack(fill=tk.X)
        
        tk.Label(rotate_frame, text="旋转角度:").pack(side=tk.LEFT)
        self.rotate_entry = tk.Entry(rotate_frame, width=8)
        self.rotate_entry.insert(0, "0")
        self.rotate_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(rotate_frame, text="度").pack(side=tk.LEFT)
        
        # 合成按钮
        process_btn = tk.Button(self.window, text="开始合成", command=self.composite_images, width=20, font=("微软雅黑", 12))
        process_btn.pack(pady=15)
        
        # 状态标签
        self.status_label = tk.Label(self.window, text="", fg="green")
        self.status_label.pack()
    
    def browse_base_image(self):
        path = filedialog.askopenfilename(filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
        if path:
            self.base_entry.delete(0, tk.END)
            self.base_entry.insert(0, path)
    
    def browse_overlay_image(self):
        path = filedialog.askopenfilename(filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
        if path:
            self.overlay_entry.delete(0, tk.END)
            self.overlay_entry.insert(0, path)
    
    def composite_images(self):
        base_path = self.base_entry.get().strip()
        overlay_path = self.overlay_entry.get().strip()
        
        if not base_path or not os.path.exists(base_path):
            messagebox.showerror("错误", "请输入有效的底图路径")
            return
        
        if not overlay_path or not os.path.exists(overlay_path):
            messagebox.showerror("错误", "请输入有效的贴图路径")
            return
        
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
        except ValueError:
            messagebox.showerror("错误", "坐标必须是整数")
            return
        
        # 根据起点和终点坐标计算尺寸
        width = None
        height = None
        end_x_str = self.end_x_entry.get().strip()
        end_y_str = self.end_y_entry.get().strip()
        
        if end_x_str and end_y_str:
            try:
                end_x = int(end_x_str)
                end_y = int(end_y_str)
                width = end_x - x
                height = end_y - y
                
                if width <= 0 or height <= 0:
                    messagebox.showerror("错误", "终点坐标必须大于起点坐标")
                    return
            except ValueError:
                messagebox.showerror("错误", "终点坐标必须是整数")
                return
        
        # 获取旋转角度
        try:
            rotation_input = self.rotate_entry.get().strip()
            rotation_angle = float(rotation_input) if rotation_input else 0.0
        except ValueError:
            messagebox.showerror("错误", "角度必须是数字")
            return
        
        try:
            base_image = Image.open(base_path).convert("RGBA")
            overlay_image = Image.open(overlay_path).convert("RGBA")
            
            # 如果指定了尺寸则调整大小
            if width is not None and height is not None:
                overlay_image = overlay_image.resize((width, height), Image.Resampling.LANCZOS)
            elif width is not None:
                ratio = width / overlay_image.width
                height = int(overlay_image.height * ratio)
                overlay_image = overlay_image.resize((width, height), Image.Resampling.LANCZOS)
            elif height is not None:
                ratio = height / overlay_image.height
                width = int(overlay_image.width * ratio)
                overlay_image = overlay_image.resize((width, height), Image.Resampling.LANCZOS)
            
            # 旋转
            overlay_image = overlay_image.rotate(rotation_angle, expand=True)
            
            # 合成
            result_image = base_image.copy()
            result_image.paste(overlay_image, (x, y), overlay_image)
            
            # 保存
            base_dir = os.path.dirname(base_path)
            base_name = os.path.splitext(os.path.basename(base_path))[0]
            output_path = os.path.join(base_dir, f"{base_name}_添加贴图.png")
            result_image.save(output_path)
            
            self.status_label.config(text=f"合成成功！\n{output_path}")
        except Exception as e:
            messagebox.showerror("错误", f"处理过程中发生错误：{str(e)}")
    
    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageManagerApp(root)
    root.mainloop()