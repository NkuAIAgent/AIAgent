import time
import random
import requests
from playwright.sync_api import sync_playwright
from playwright.sync_api import sync_playwright
from .utils import load_links_from_json


class HTMLDownloader:
    """HTML下载器"""
    
    def __init__(self, config):
        self.config = config
    
    def fetch_html(self, url, retries=3):
        """
        获取单个网页HTML
        
        Args:
            url (str): 网页URL
            retries (int): 重试次数

            
        Returns:
            str or None: HTML内容
        """



        for i in range(retries):
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)  # 可设为 False 调试用
                    page = browser.new_page()
                    page.goto(url, timeout=60000)  # 60秒超时
                    page.wait_for_load_state("load",timeout=60000)  # 等待页面资源加载完毕
                    html = page.content()  # 获取渲染后的 HTML 源码
                    browser.close()
                    return html
                # resp = requests.get(url, headers=self.config.headers)
                # if resp.status_code == 200:
                #     resp.encoding = resp.apparent_encoding
                #     return resp.text####成功返回html内容
                # print(f"状态码 {resp.status_code}: {url}")
            except requests.RequestException as e:
                print(f"请求错误 {url}: {e}")
            
            time.sleep(2 + random.random())
        
        return None
    
    def download_all_html(self):
        """
        下载所有HTML文件

        Returns:
            dict: 成功下载的文件路径映射 {序号: 文件路径}
        """
        links, links_dict = load_links_from_json(self.config.json_input_path)
        downloaded_files = {}

        print(f"开始下载HTML文件到: {self.config.html_output_dir}")

        for idx, url in enumerate(links, 1):
            print(f"下载第 {idx}/{len(links)} 个链接...")
            html = self.fetch_html(url)

            if html:
                html_file_path = self.config.html_output_dir / f"page_{idx:03d}.html"
                html_file_path.write_text(html, encoding="utf-8")
                downloaded_files[idx] = html_file_path
                print(f"已保存: {html_file_path.name}")
            else:
                print(f"下载失败: {url}")

        print(f"HTML下载完成，成功 {len(downloaded_files)}/{len(links)} 个文件")
        return downloaded_files


