from playwright.sync_api import sync_playwright
from CrawlModule.InputAndEnter import input_and_enter
from CrawlModule.Crawl import get_all_links
from CrawlModule.LoadMore import load_more
from CrawlModule.WriteToJson import write_to_json


def get_page_source(url,code):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            # page.wait_for_timeout(5000000)
            # 调用密码输入模块
            input_and_enter(page, code)
            # 等待5秒页面渲染
            # 等待 URL 改变或页面加载
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
            ###加载更多
            load_more(page)

            # html = page.content()
            # print(html[:20000])
            print("调用抓取模块")# 打印前2000字符看有无加载成功
            links= get_all_links(page)
            print("抓取完成")
            ##写入json
            write_to_json(links)
        except Exception as e:
            print("页面加载失败：", e)
        finally:
            browser.close()

