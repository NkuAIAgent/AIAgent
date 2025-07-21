import pathlib
####配置json,html,txt目录
class Config:
    """配置类"""
    
    def __init__(self, 
                 json_input_path="../resources/json_input_path.json",####包含要下载的链接的JSON文件路径
                 html_output_dir="../resources/html_out_dir",  ##HTML文件存放路径
                 txt_output_dir="../resources/txt_out_dir"):##  转换后的TXT文件输出路径



        ##将你传入的字符串路径（如 "C:/Users/k3h4n/Desktop/articles/html"）转换为 Path 对象，以便后续更方便、安全地进行文件或目录操作
        self.json_input_path = pathlib.Path(json_input_path)
        self.html_output_dir = pathlib.Path(html_output_dir)
        self.txt_output_dir = pathlib.Path(txt_output_dir)
        
        # 创建输出目录
        self.html_output_dir.mkdir(exist_ok=True)
        self.txt_output_dir.mkdir(exist_ok=True)
        
        self.headers = {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0 Safari/537.36"),
        }
