from .config import Config
from .downloader import HTMLDownloader
from .converter import HTMLToTXTConverter


class WeChatArticleProcessor:
    """微信公众号文章处理器"""
    
    def __init__(self, **kwargs):
        self.config = Config(**kwargs)####Config是配置文件，自动映射成config对象，**kwargs是可变参数，传入的参数会自动映射成config对象的属性
        self.downloader = HTMLDownloader(self.config)
        self.converter = HTMLToTXTConverter(self.config)
    
    def process_all(self):
        """
        完整流程：下载HTML → 转换TXT
        
        Returns:
            dict: 处理结果统计
        """
        print("开始完整处理流程...")
        print(f"输入JSON: {self.config.json_input_path}")
        print(f"HTML输出目录: {self.config.html_output_dir}")
        print(f"TXT输出目录: {self.config.txt_output_dir}")
        print("-" * 50)
        
        # 第一步：下载HTML
        downloaded_files = self.downloader.download_all_html()
        print("-" * 50)
        
        # 第二步：转换TXT
        converted_files = self.converter.convert_all_html_to_txt()
        
        result = {
            "downloaded_count": len(downloaded_files),
            "converted_count": len(converted_files),
            "html_output_dir": str(self.config.html_output_dir),
            "txt_output_dir": str(self.config.txt_output_dir)
        }
        
        print("-" * 50)
        print("处理完成")
        print(f"下载HTML: {result['downloaded_count']} 个")
        print(f"转换TXT: {result['converted_count']} 个")
        
        return result
