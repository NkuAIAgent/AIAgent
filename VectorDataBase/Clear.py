import os
from pathlib import Path

def clear():
    # 要清空的目录路径
    html_out_dir = Path("../resources/html_out_dir")
    txt_out_dir = Path("../resources/txt_out_dir")
    json_out_dir = Path("../resources/json_input_path")
    # def clear_folder(folder: Path):
    #     if folder.exists() and folder.is_dir():
    #         for file in folder.iterdir():
    #             if file.is_file():
    #                 file.unlink()  # 删除文件
    #                 print(f"已删除文件: {file.name}")
    #             elif file.is_dir():
    #                 # 如果还有子目录可递归删除（可选）
    #                 print(f"跳过目录: {file.name}")
    def clear_folder(folder: Path):
        if folder.exists() and folder.is_dir():
            for file in folder.iterdir():
                if file.is_file():
                    if file.name == ".gitkeep":
                        print(f"保留 .gitkeep 文件: {file.name}")
                        continue
                    file.unlink()  # 删除文件
                    print(f"已删除文件: {file.name}")
                elif file.is_dir():
                    print(f"跳过子目录: {file.name}")

    # 清空两个路径下的文件
    clear_folder(html_out_dir)
    clear_folder(txt_out_dir)
