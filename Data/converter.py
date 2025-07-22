import re
import pathlib
from bs4 import BeautifulSoup
from .utils import load_links_from_json, clean_filename, extract_page_number


class HTMLToTXTConverter:
    """HTML到TXT转换器"""
    
    def __init__(self, config):
        self.config = config
    
    def html_to_txt(self, html_file_path, original_url=""):
        """
        将单个HTML文件转换为TXT
        
        Args:
            html_file_path (pathlib.Path): HTML文件路径
            original_url (str): 原始链接
            
        Returns:
            pathlib.Path or None: 生成的TXT文件路径
        """
        try:
            # 读取HTML文件
            with open(html_file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 提取标题
            title, original_title = self._extract_title(soup, html_file_path)
            
            # 提取发布时间
            publish_time = self._extract_publish_time(soup, html_file_path)
            
            # 提取正文内容
            content_text = self._extract_content(soup)
            
            # 生成txt文件内容
            txt_content = self._generate_txt_content(original_title, content_text, original_url, publish_time)
            
            # 保存txt文件
            txt_file_path = self.config.txt_output_dir / f"{title}.txt"
            with open(txt_file_path, "w", encoding="utf-8") as f:
                f.write(txt_content)
            
            return txt_file_path
            
        except Exception as e:
            print(f"转换失败 {html_file_path.name}: {e}")
            return None
    
    def _extract_title(self, soup, html_file_path):
        """提取标题"""
        h1_tag = soup.find('h1', class_='rich_media_title')
        if h1_tag:
            original_title = h1_tag.get_text().strip()
            title = clean_filename(original_title)
        else:
            title = f"未知标题_{html_file_path.stem}"
            original_title = "未知标题"
        
        return title, original_title
    
    def _extract_publish_time(self, soup, html_file_path):
        """提取发布时间"""
        publish_time_tag = soup.find('em', id='publish_time')
        if publish_time_tag:
            publish_time = publish_time_tag.get_text().strip()
            print(f"成功提取发布时间: {publish_time}")
        else:
            publish_time = "未知时间"
            print(f"未找到发布时间标签，文件: {html_file_path.name}")
        
        return publish_time
    
    def _extract_content(self, soup):
        """提取正文内容"""
        content_div = soup.find('div', class_='rich_media_content')
        if content_div:
            # 移除不需要的元素
            for tag in content_div.find_all(['script', 'style', 'iframe']):
                tag.decompose()
            
            # 提取纯文本并删除所有空格和换行
            content_text = content_div.get_text(separator='').strip()
            content_text = re.sub(r'\s+', '', content_text)
        else:
            content_text = "未找到正文内容"
        
        return content_text
    
    def _generate_txt_content(self, title, content, url, publish_time):
        """生成TXT文件内容"""
        txt_content = f"标题:{title}\n"
        txt_content += f"{content}\n"
        txt_content += f"原文链接: {url}\n"
        txt_content += f"发布时间: {publish_time}\n"
        txt_content += "#" * 100 + "\n"
        return txt_content
    
    def convert_all_html_to_txt(self, html_dir_path=None):
        """
        批量将HTML文件转换为TXT
        
        Args:
            html_dir_path (str): HTML文件目录路径
            
        Returns:
            dict: 转换结果 {html_file: txt_file}
        """
        if html_dir_path is None:
            html_dir_path = self.config.html_output_dir
        else:
            html_dir_path = pathlib.Path(html_dir_path)
        
        print(f"开始转换HTML文件: {html_dir_path} -> {self.config.txt_output_dir}")
        
        # 加载链接映射
        try:
            _, links_dict = load_links_from_json(self.config.json_input_path)
        except FileNotFoundError:
            print("未找到JSON文件，将使用空链接")
            links_dict = {}
        
        converted_files = {}
        html_files = list(html_dir_path.glob("*.html"))
        
        for html_file in html_files:
            print(f"转换: {html_file.name}")
            
            # 从文件名提取序号
            page_num = extract_page_number(html_file.name)
            original_url = links_dict.get(page_num, "") if page_num else ""
            
            txt_file = self.html_to_txt(html_file, original_url)
            if txt_file:
                converted_files[html_file] = txt_file
                print(f"已转换: {txt_file.name}")
        
        print(f"TXT转换完成，成功 {len(converted_files)}/{len(html_files)} 个文件")
        return converted_files
