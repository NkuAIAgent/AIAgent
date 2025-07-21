

# load_more.py

from playwright.sync_api import Page

def load_more(page):
    """
    点击页面上的“加载更多”按钮指定次数。

    参数：
        page: Playwright 的 Page 实例
        times: 点击次数，默认点击两次
        wait_ms: 每次点击后等待时间（毫秒），默认 2000ms
    """
    for i in range(0):
        try:
            load_more_btn = page.locator('button:has-text("加载更多")')
            ###等待按钮可见并执行
            load_more_btn.wait_for(state="visible", timeout=5000)
            load_more_btn.click()
            print(f" 第 {i + 1} 次点击“加载更多”")
            # page.wait_for_timeout(wait_ms)
        except Exception as e:
            print(f"第 {i + 1} 次点击加载更多失败:", e)
            break

    page.wait_for_timeout(300)###0.3秒（300 毫秒）。