import os
import sys
from PIL import Image

def resize_images(input_path, target_width, target_height, quality=95):
    supported_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    
    if not os.path.exists(input_path):
        print(f"错误：输入路径 '{input_path}' 不存在")
        return
    
    if os.path.isfile(input_path):
        if input_path.lower().endswith(supported_formats):
            image_files = [os.path.basename(input_path)]
            output_dir = os.path.dirname(input_path)
        else:
            print("错误：输入的文件不是支持的图片格式")
            return
    else:
        image_files = [f for f in os.listdir(input_path) 
                       if os.path.isfile(os.path.join(input_path, f)) 
                       and f.lower().endswith(supported_formats)]
        output_dir = input_path
    
    if not image_files:
        print("未找到任何支持的图片文件")
        return
    
    print(f"找到 {len(image_files)} 个图片文件")
    print(f"输出目录: {output_dir}")
    
    for filename in image_files:
        try:
            full_input_path = os.path.join(output_dir, filename)
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_像素调整{ext}"
            output_path = os.path.join(output_dir, output_filename)
            
            with Image.open(full_input_path) as img:
                img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                
                if img.mode == 'RGBA' and filename.lower().endswith(('.jpg', '.jpeg')):
                    img = img.convert('RGB')
                
                img.save(output_path, quality=quality)
                print(f"已处理: {filename}")
        
        except Exception as e:
            print(f"处理 {filename} 时出错: {str(e)}")
    
    print("处理完成")

def get_input(prompt, required=True, default=None):
    while True:
        value = input(prompt)
        if value.strip() == '':
            if required:
                print("该选项不能为空，请重新输入")
                continue
            else:
                return default
        return value.strip()

def get_int_input(prompt, required=True, default=None, min_val=1):
    while True:
        value = input(prompt)
        if value.strip() == '':
            if required:
                print("该选项不能为空，请重新输入")
                continue
            else:
                return default
        try:
            int_val = int(value)
            if int_val < min_val:
                print(f"值必须大于等于 {min_val}")
                continue
            return int_val
        except ValueError:
            print("请输入有效的数字")

if __name__ == '__main__':
    print("=" * 40)
    print("      图片尺寸调整工具")
    print("=" * 40)
    print("支持输入：文件夹路径（批量处理）或单个图片文件路径")
    print("处理后的图片将保存在源文件夹下，文件名添加 '_像素调整' 后缀")
    print("=" * 40)
    
    input_dir = get_input("请输入图片文件夹或图片文件路径: ")
    target_width = get_int_input("请输入目标宽度（像素）: ")
    target_height = get_int_input("请输入目标高度（像素）: ")
    quality_input = get_input("请输入图片质量（1-100，默认95）: ", required=False)
    
    quality = 95
    if quality_input:
        try:
            quality = int(quality_input)
            if quality < 1 or quality > 100:
                print("质量值超出范围，使用默认值 95")
                quality = 95
        except ValueError:
            print("无效的质量值，使用默认值 95")
    
    print("\n开始处理...")
    resize_images(input_dir, target_width, target_height, quality)