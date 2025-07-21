"""每日考研倒计时和励志语录企业微信推送脚本。"""

import datetime

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

# ====== 你的配置 ======
WEBHOOK_URL = "your_webhook_url"
KIMI_API_KEY = "your_api_key"
KIMI_API_URL = "https://api.moonshot.cn/v1/chat/completions"
考研日期 = datetime.datetime(2025, 12, 20)


# ====== Kimi 接口调用函数 ======
def generate_kimi_motivation():
    headers = {
        "Authorization": f"Bearer {KIMI_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "kimi-k2-0711-preview",  # 你可以换成 kimi-k2-0711-preview
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
        response = requests.post(KIMI_API_URL, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Kimi 请求失败，使用备用语句。错误信息：{e}")
        return "坚持不一定成功，但放弃一定失败。今天也要加油哦！"


# ====== 倒计时函数 ======
def get_countdown():
    now = datetime.datetime.now()
    days_left = (考研日期 - now).days
    return f"📅 距离 26 考研还有 {days_left} 天"


# ====== 获取今日日期信息 ======
def get_today_info():
    now = datetime.datetime.now()
    weekdays = ["一", "二", "三", "四", "五", "六", "日"]
    weekday = weekdays[now.weekday()]
    date_str = now.strftime("%Y年%m月%d日")
    return date_str, weekday


# ====== 发送到企业微信群的函数 ======
def send_message(content):
    data = {"msgtype": "text", "text": {"content": content}}
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        print(f"消息发送成功：{response.status_code}")
    except Exception as e:
        print(f"消息发送失败：{e}")


# ====== 早晚消息封装 ======
def send_morning():
    print("正在发送早安提醒...")
    motivation = generate_kimi_motivation()
    date_str, weekday = get_today_info()
    countdown = get_countdown()

    content = (
        f"📆 {date_str} (星期{weekday})\n{countdown}\n☀️ 早安，旺仔！\n{motivation}"
    )
    send_message(content)


def send_evening():
    print("正在发送晚安提醒...")
    motivation = generate_kimi_motivation()
    date_str, weekday = get_today_info()

    content = f"📆 {date_str} (星期{weekday})\n🌙 旺仔，今天辛苦了！\n别忘了复盘总结今日所学。\n{motivation}"
    send_message(content)


# ====== 定时器设置 ======
def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(send_morning, "cron", hour=6, minute=0)
    scheduler.add_job(send_evening, "cron", hour=18, minute=0)
    print("✅ 考研每日提醒服务已启动，等待触发中……")
    scheduler.start()


# ====== 测试函数 ======
def test_messages():
    """测试消息发送功能"""
    print("=== 测试早安消息 ===")
    send_morning()
    print("\n=== 测试晚安消息 ===")
    send_evening()


if __name__ == "__main__":
    # 测试消息发送功能（测试完成后可以注释掉）
    test_messages()

    # 启动定时服务
    # main()
