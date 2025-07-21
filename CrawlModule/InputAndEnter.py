# auth_input.py

from playwright.sync_api import Page

def input_and_enter(page: Page, code: str):
    try:
        # 等待输入框加载
        page.wait_for_selector('input[placeholder="请输入auth code"]', timeout=10000)
        print("成功找到输入框")
        # 输入密码
        page.fill('input[placeholder="请输入auth code"]', code)
        print("成功输入密码")
        # 点击“确认”按钮
        confirm_button = page.locator('button', has_text="确认")
        confirm_button.click()
        print("成功点击确认按钮")
        # page.wait_for_timeout(300000)
        # 提交（点击按钮或按回车）
        # try:
        #     page.click('button:has-text("进入")')
        # except:
        #     page.keyboard.press("Enter")
        #
        #     # 等待跳转或页面加载
        #     page.wait_for_load_state("networkidle")
        #     page.wait_for_timeout(3000)
    except Exception as e:
        print("❌ 输入 auth code 或点击确认按钮失败：", e)
        raise