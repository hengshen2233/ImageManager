import os
import platform
from PIL import Image, ImageDraw, ImageFont

def get_system_font_path():
    """获取Windows系统字体目录路径"""
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
    elif system == "Darwin":
        return "/System/Library/Fonts"
    else:
        return "/usr/share/fonts"

def select_image_source():
    """输入图片路径（支持单个图片文件或文件夹）"""
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    
    while True:
        path = input("请输入图片文件或文件夹的完整路径: ").strip()
        
        # 检查是否为文件
        if os.path.isfile(path):
            if path.lower().endswith(image_extensions):
                return 'file', path
            else:
                print("输入的文件不是有效的图片格式！")
                print(f"支持的格式: {', '.join(image_extensions)}")
                continue
        
        # 检查是否为文件夹
        if os.path.isdir(path):
            # 检查文件夹中是否有图片
            files = os.listdir(path)
            image_files = [f for f in files if f.lower().endswith(image_extensions)]
            if image_files:
                return 'folder', path
            else:
                print("该文件夹中没有找到图片文件！")
                continue
        
        print("输入的路径无效或不存在！")

def get_user_inputs():
    """获取用户输入的参数"""
    print("=" * 50)
    print("图片添加文字工具")
    print("=" * 50)
    
    # 获取文字位置坐标
    while True:
        try:
            x = int(input("请输入文字的X坐标: "))
            y = int(input("请输入文字的Y坐标: "))
            break
        except ValueError:
            print("请输入有效的数字！")
    
    # 获取文字内容
    text = input("请输入要添加的文字内容: ").strip()
    while not text:
        print("文字内容不能为空！")
        text = input("请输入要添加的文字内容: ").strip()
    
    # 获取文字大小（默认16px）
    while True:
        font_size_input = input("请输入文字大小（默认16px）: ").strip()
        if not font_size_input:
            font_size = 16
            break
        try:
            font_size = int(font_size_input)
            if font_size > 0:
                break
            else:
                print("文字大小必须大于0！")
        except ValueError:
            print("请输入有效的数字！")
    
    # 获取字体（默认宋体）
    font_name = input("请输入字体名称（默认宋体）: ").strip()
    if not font_name:
        font_name = "SimSun"
    
    # 获取旋转角度（默认0度）
    while True:
        rotation_input = input("请输入文字旋转角度（默认0度）: ").strip()
        if not rotation_input:
            rotation = 0
            break
        try:
            rotation = int(rotation_input)
            break
        except ValueError:
            print("请输入有效的数字！")
    
    return x, y, text, font_size, font_name, rotation

def load_font(font_name, font_size):
    """加载字体"""
    font_mapping = {
        "宋体": "simhei.ttf",
        "黑体": "simhei.ttf",
        "微软雅黑": "msyh.ttc",
        "楷体": "simkai.ttf",
        "仿宋": "simfang.ttf",
        "隶书": "simli.ttf",
        "幼圆": "youyuan.ttf"
    }
    
    font_dir = get_system_font_path()
    font_candidates = []
    
    if font_name in font_mapping:
        font_candidates.append(os.path.join(font_dir, font_mapping[font_name]))
    else:
        font_candidates.append(os.path.join(font_dir, f"{font_name}.ttf"))
        font_candidates.append(os.path.join(font_dir, f"{font_name}.ttc"))
        font_candidates.append(os.path.join(font_dir, f"{font_name}.otf"))
    
    default_fonts = ["simhei.ttf", "simsun.ttc", "msyh.ttc", "simkai.ttf"]
    for df in default_fonts:
        font_candidates.append(os.path.join(font_dir, df))
    
    font = None
    for font_path in font_candidates:
        try:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
                print(f"使用字体：{font_path}")
                break
        except Exception as e:
            continue
    
    if font is None:
        print("警告：未找到合适的中文字体，使用默认字体")
        font = ImageFont.load_default()
    
    return font

def add_text_to_image(image_path, x, y, text, font_size, font_name, rotation):
    """给单个图片添加文字"""
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        font = load_font(font_name, font_size)
        
        if rotation != 0:
            text_img = Image.new('RGBA', (img.width, img.height), (255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_img)
            text_draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))
            text_img = text_img.rotate(rotation, expand=True)
            img.paste(text_img, (0, 0), text_img)
        else:
            draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))
        
        folder_path = os.path.dirname(image_path)
        filename = os.path.basename(image_path)
        name, ext = os.path.splitext(filename)
        new_name = f"{name}_添加文字{ext}"
        new_path = os.path.join(folder_path, new_name)
        
        img.save(new_path)
        print(f"已处理：{filename} -> {new_name}")
        return True
    except Exception as e:
        print(f"处理图片时出错：{e}")
        return False

def add_text_to_images(folder_path, x, y, text, font_size, font_name, rotation):
    """给文件夹中的图片添加文字"""
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    files = os.listdir(folder_path)
    image_files = [f for f in files if f.lower().endswith(image_extensions)]
    
    if not image_files:
        print("未找到图片文件！")
        return
    
    print(f"\n找到 {len(image_files)} 个图片文件")
    font = load_font(font_name, font_size)
    
    for image_file in image_files:
        try:
            image_path = os.path.join(folder_path, image_file)
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            
            if rotation != 0:
                text_img = Image.new('RGBA', (img.width, img.height), (255, 255, 255, 0))
                text_draw = ImageDraw.Draw(text_img)
                text_draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))
                text_img = text_img.rotate(rotation, expand=True)
                img.paste(text_img, (0, 0), text_img)
            else:
                draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))
            
            name, ext = os.path.splitext(image_file)
            new_name = f"{name}_添加文字{ext}"
            new_path = os.path.join(folder_path, new_name)
            
            img.save(new_path)
            print(f"已处理：{image_file} -> {new_name}")
        
        except Exception as e:
            print(f"处理 {image_file} 时出错：{e}")
    
    print("\n处理完成！")

def main():
    # 输入图片路径（支持单个文件或文件夹）
    source_type, path = select_image_source()
    
    # 获取用户输入
    x, y, text, font_size, font_name, rotation = get_user_inputs()
    
    # 根据类型处理图片
    if source_type == 'file':
        print("\n开始处理图片...")
        add_text_to_image(path, x, y, text, font_size, font_name, rotation)
        print("\n处理完成！")
    else:
        add_text_to_images(path, x, y, text, font_size, font_name, rotation)

if __name__ == "__main__":
    main()