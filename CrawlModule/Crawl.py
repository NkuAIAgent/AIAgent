from datetime import datetime

from playwright.sync_api import sync_playwright

import re

from CrawlModule.LoadMore import load_more


# def get_all_links(page)->list:
#     pattern = re.compile(r"https://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+")
#
#     # with sync_playwright() as p:
#     #     browser = p.chromium.launch(
#     #         headless=False,
#     #         executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Windows示例
#     #     )
#     #     page = browser.new_page()
#     #     page.goto(url,wait_until="domcontentloaded",timeout=60000)
#
#         # ###等待页面网络加载稳定（适合SPA  单页应用）
#         # page.wait_for_load_state("networkidle")
#         # # page.wait_for_selector("tr td a[href]", timeout=10000)  # 最多等10秒
#     # print(page.content()[:60000])  # 打印页面前1000字符，确认里面有没有 <tr> 和 <a href=...>
#     # 等待页面关键元素加载（可根据实际情况调整）
#     page.wait_for_selector("a[href]", timeout=10000)###10秒
#
#
#
#     ##抓取所有tr>td>a[href]链接
#     ####选中所有符合 CSS 选择器 tr > td > a[href] 的标签元素
#     ###.all()
#     # 获取全部匹配的元素，返回 ElementHandle 列表
#     elements=page.locator("a[href]").all()
#     hrefs = []
#     for el in elements:
#         try:
#             href = el.get_attribute("href")  # 尝试获取超链接
#             if href:  # 如果成功获取并且不为空
#                 hrefs.append(href)  # 把链接加到列表里
#         except Exception as e:
#             print(f"获取链接失败：{e}")
#     # 过滤匹配微信文章链接的href
#     wechat_links = [href for href in hrefs if pattern.match(href)]
#     ###设置成集合去重
#     print_links(wechat_links)
#     return list(set(wechat_links))
# # 使用例子
# # if __name__ == "__main__":
# #     url = "https://wechat-rag.zeabur.app/dash"
# #     links = get_all_links(url)
# #     print(f"共抓到 {len(links)} 个链接：")
# #     for link in links:
# #         print(link)
def get_datetime_from_text(text: str):
    """从文本中提取时间字符串，并转为 datetime 对象"""
    # 匹配格式：2025-07-21 13:25:45
    match = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", text)
    if match:
        try:
            return datetime.strptime(match.group(), "%Y-%m-%d %H:%M:%S")
        except:
            return None
    return None

def get_all_links(page, threshold_time_str: str):
    pattern = re.compile(r"https://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+")
    threshold_time = datetime.strptime(threshold_time_str, "%Y-%m-%d %H:%M:%S")

    page.wait_for_selector("a[href]", timeout=10000)
    elements = page.locator("a[href]").all()

    links = []
    latest_time = threshold_time  # 初始设为阈值时间

    for el in elements:
        href = el.get_attribute("href")
        if not href or not pattern.match(href):
            continue

        time_text = el.evaluate("""
            el => {
                const td = el.closest('td');
                const next = td?.nextElementSibling;
                return next?.innerText || '';
            }
        """)
        publish_time = get_datetime_from_text(time_text)

        if publish_time is None:
            print(f"未找到时间: {href}")
            continue

        if publish_time > threshold_time:
            print(f"✔ 收录: {href} | 时间: {publish_time}")
            links.append(href)
            # 更新最大时间
            if publish_time > latest_time:
                latest_time = publish_time
        else:
            print(f"✘ 跳过并终止: {href} | 时间: {publish_time}")
            break

    return list(dict.fromkeys(links)), latest_time

def print_links(wechat_links):
    print(f"共抓到 {len(wechat_links)} 个链接：")
    for link in wechat_links:
        print(link)



