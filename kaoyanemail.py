"""本模块用于考研邮件提醒，包括早晚励志语和倒计时功能。"""

import smtplib
import datetime
import os
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

import requests
from apscheduler.schedulers.blocking import BlockingScheduler  # type: ignore

# 获取脚本所在目录的绝对路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ====== 配置信息 ======
EMAIL_SENDER = "1958232837@qq.com"
EMAIL_PASSWORD = "pjsvghoxgcozbddb"  # 这是你的 SMTP 授权码
EMAIL_RECEIVER = "1958232837@qq.com"  # 收件人邮箱（可以和发送人一样）
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465


KIMI_API_KEY = "sk-CM1pZOKfLJUSRyds59sHcvBwxRG1lHbWcNSYVC7EWjULzvtc"  # 这是你的 Kimi API 密钥
KIMI_API_URL = "https://api.moonshot.cn/v1/chat/completions"
KAOYAN_DATE = datetime.datetime(2025, 12, 20)


# ====== 发送邮件函数 ======
def send_email(subject, html_body):
    """发送邮件。"""
    message = MIMEText(html_body, "html", "utf-8")
    message["From"] = formataddr(("考研提醒小助手", EMAIL_SENDER))
    message["To"] = formataddr(("亲爱的旺仔", EMAIL_RECEIVER))
    message["Subject"] = Header(subject, "utf-8")

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, [EMAIL_RECEIVER], message.as_string())
        server.quit()
        print("✅ 邮件发送成功")
    except smtplib.SMTPException as e:
        print(f"❌ 邮件发送失败：{e}")


# ====== Kimi 接口调用函数 ======
def generate_kimi_motivation():
    """调用 Kimi API 生成励志语。"""
    headers = {
        "Authorization": f"Bearer {KIMI_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "kimi-k2-0711-preview",
        "messages": [
            {
                "role": "system",
                "content": "你是一个鼓励考研学生的AI，每天生成一句简短但真诚的励志语。",
            },
            {
                "role": "user",
                "content": "请给我一句今天的考研励志语，积极、温暖、不敷衍。",
            },
        ],
        "temperature": 0.9,
        "max_tokens": 100,
    }

    try:
        response = requests.post(
            url=KIMI_API_URL, headers=headers, json=data, timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Kimi 请求失败，使用备用语句。错误信息：{e}")
        return "坚持不一定成功，但放弃一定失败。今天也要加油哦！"


# ====== 倒计时函数 ======
def get_countdown():
    """计算考研倒计时天数。"""
    now = datetime.datetime.now()
    days_left = (KAOYAN_DATE - now).days
    return f"📅 距离 26 考研还有 {days_left} 天"


# ====== 读取 HTML 模板函数 ======
def read_html_template(template_path):
    """读取 HTML 模板文件内容。"""
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ 模板文件未找到：{template_path}")
        return "<html><body><h1>模板文件未找到</h1></body></html>"
    except OSError as e:
        print(f"❌ 读取模板文件时出错：{e}")
        return "<html><body><h1>读取模板时出错</h1></body></html>"


# ====== 早晚邮件封装 ======
def send_morning():
    """发送早安邮件。"""
    print("📩 正在发送早安提醒邮件……")

    # 获取日期和星期
    now = datetime.datetime.now()
    weekday_map = ["一", "二", "三", "四", "五", "六", "日"]
    weekday = weekday_map[now.weekday()]
    date_str = now.strftime(f"%Y年%m月%d日 星期{weekday}")

    motivation = generate_kimi_motivation()
    countdown = get_countdown()

    # 读取并填充 HTML 模板
    template_path = os.path.join(SCRIPT_DIR, "morning_template.html")
    html_template = read_html_template(template_path)
    html_content = html_template.format(
        date_str=date_str, countdown=countdown, motivation=motivation
    )

    send_email("考研早安提醒", html_content)


def send_evening():
    """发送晚安邮件。"""
    print("📩 正在发送晚安提醒邮件……")
    motivation = generate_kimi_motivation()

    # 读取并填充 HTML 模板
    template_path = os.path.join(SCRIPT_DIR, "evening_template.html")
    html_template = read_html_template(template_path)
    html_content = html_template.format(motivation=motivation)

    send_email("考研晚安提醒", html_content)


# ====== 定时器设置 ======
def main():
    """设置并启动定时任务。"""
    scheduler = BlockingScheduler()
    scheduler.add_job(send_morning, "cron", hour=8, minute=0)
    scheduler.add_job(send_evening, "cron", hour=22, minute=0)
    print("✅ 邮件提醒服务已启动，等待触发中……")
    scheduler.start()


if __name__ == "__main__":
    main()  # 正式启动
    # send_morning()  # 你可以先用这个测试早上那封邮件
    # send_evening()  # 然后测试晚上的邮件
