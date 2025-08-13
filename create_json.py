import json
import os
from urllib.parse import quote

def generate_json_for_folder(folder_path, root_output_dir):
    """
    为一个指定的子文件夹生成图标JSON文件，并将其保存在根输出目录中。
    :param folder_path: 要扫描的图标子文件夹路径 (e.g., "icon/kelee")
    :param root_output_dir: 所有JSON文件的保存位置 (e.g., "icon")
    """
    
    folder_name = os.path.basename(folder_path)
    
    # GitHub Raw 基础 URL
    base_url = f"https://raw.githubusercontent.com/yssqtao/plugins/main/icon/{folder_name}/"
    
    # JSON 文件信息
    json_name = f"{folder_name} 图标库"
    
    icons_list = []
    
    # 扫描子文件夹内的所有 .png 文件
    image_files = [f for f in sorted(os.listdir(folder_path)) if f.endswith(".png")]
            
    if not image_files:
        print(f"⏩ 在 '{folder_path}' 中未找到 .png 文件，已跳过。")
        return

    # 为找到的每个图片文件创建条目
    for filename in image_files:
        name = os.path.splitext(filename)[0]
        encoded_filename = quote(filename)
        url = base_url + encoded_filename
        icons_list.append({"name": name, "url": url})

    final_json = {
        "name": json_name,
        "icons": icons_list
    }

    # 将 Python 字典转换为格式化的 JSON 字符串
    json_output = json.dumps(final_json, indent=2, ensure_ascii=False)
    
    # --- 主要修改点 ---
    # 将输出路径从子文件夹改为了根目录
    output_filepath = os.path.join(root_output_dir, f"{folder_name}.json")

    # 写入文件
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(json_output)

    print(f"✅ 文件 {os.path.basename(output_filepath)} 已成功生成在 '{root_output_dir}' 目录（包含 {len(image_files)} 个图标）。")


# --- 主程序 ---
if __name__ == "__main__":
    # 主图标目录，既是扫描的起点，也是JSON文件的保存位置
    root_icon_dir = "icon"
    
    if not os.path.isdir(root_icon_dir):
        print(f"❌ 错误：主图标目录 '{root_icon_dir}' 不存在。")
    else:
        print(f"🔍 开始扫描 '{root_icon_dir}' 目录，生成的 JSON 将保存在此。")
        # 遍历 icon 文件夹下的所有条目
        for entry_name in os.listdir(root_icon_dir):
            entry_path = os.path.join(root_icon_dir, entry_name)
            # 检查这个条目是否是一个文件夹
            if os.path.isdir(entry_path):
                # 将主目录和子目录路径都传入函数
                generate_json_for_folder(entry_path, root_icon_dir)
        print("\n🎉 所有文件夹处理完毕！")