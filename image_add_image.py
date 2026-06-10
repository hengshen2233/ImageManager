from PIL import Image
import os

def composite_images():
    print("图片合成工具")
    print("=" * 30)
    
    base_image_path = input("请输入底图的完整路径：").strip()
    
    if not os.path.exists(base_image_path):
        print(f"错误：底图文件不存在！路径: {base_image_path}")
        return
    
    overlay_image_path = input("请输入贴图的完整路径：").strip()
    
    if not os.path.exists(overlay_image_path):
        print(f"错误：贴图文件不存在！路径: {overlay_image_path}")
        return
    
    try:
        x = int(input("请输入贴图左上角在底图上的X坐标：").strip())
        y = int(input("请输入贴图左上角在底图上的Y坐标：").strip())
    except ValueError:
        print("错误：坐标必须是整数！")
        return
    
    try:
        width = int(input("请输入贴图的宽度：").strip())
        height = int(input("请输入贴图的高度：").strip())
    except ValueError:
        print("错误：尺寸必须是整数！")
        return
    
    try:
        rotation_input = input("请输入旋转角度（默认为0）：").strip()
        rotation_angle = float(rotation_input) if rotation_input else 0.0
    except ValueError:
        print("错误：角度必须是数字！")
        return
    
    try:
        base_image = Image.open(base_image_path).convert("RGBA")
        overlay_image = Image.open(overlay_image_path).convert("RGBA")
        
        overlay_image = overlay_image.resize((width, height), Image.Resampling.LANCZOS)
        
        overlay_image = overlay_image.rotate(rotation_angle, expand=True)
        
        result_image = base_image.copy()
        
        result_image.paste(overlay_image, (x, y), overlay_image)
        
        base_dir = os.path.dirname(base_image_path)
        base_name = os.path.splitext(os.path.basename(base_image_path))[0]
        output_path = os.path.join(base_dir, f"{base_name}_添加贴图.png")
        
        result_image.save(output_path)
        
        print(f"\n合成成功！结果保存到：{output_path}")
        
    except Exception as e:
        print(f"处理过程中发生错误：{e}")

if __name__ == "__main__":
    composite_images()