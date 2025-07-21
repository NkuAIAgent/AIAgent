import json
import re

def load_links_from_json(json_path):###这里的json_path是一个路径，是一个文件对象
    """
    从JSON文件加载链接
    
    Args:
        json_path (pathlib.Path): JSON文件路径
        
    Returns:
        tuple: (链接列表, 序号到链接的映射字典)
    """
    print(f"读取JSON文件: {json_path}")
    
    with open(json_path, "r", encoding="utf-8") as f:
        records = json.load(f)
    
    links = [item["link"] for item in records if "link" in item]####这里是html链接列表
    links_dict = {i: item["link"] for i, item in enumerate(records, 1) if "link" in item}###键是它们的序号，值是对应的链接。序号从1开始
    
    print(f"成功加载 {len(links)} 个链接")
    return links, links_dict#######返回链接列表和序号到链接的映射字典

def clean_filename(title):
    """
    清理文件名中的非法字符
    
    Args:
        title (str): 原始标题
        
    Returns:
        str: 清理后的文件名
    """
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    title = title.replace('\n', ' ').replace('\r', ' ')
    return title[:100]  # 限制文件名长度

def extract_page_number(filename):
    """
    从文件名提取页码
    
    Args:
        filename (str): 文件名
        
    Returns:
        int or None: 页码
    """
    match = re.search(r'page_(\d+)', filename)
    return int(match.group(1)) if match else None
