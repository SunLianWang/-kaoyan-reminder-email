"""一个用于测试 SMTP 邮件发送功能的独立脚本。"""

import smtplib
from email.mime.text import MIMEText

# --- 请修改以下配置 ---
SENDER_EMAIL = "1958232837@qq.com"  # 你的发件邮箱
SENDER_AUTH_CODE = "你的授权码"  # 你的邮箱授权码
RECEIVER_EMAIL = "1958232837@qq.com"  # 收件人邮箱
# ---------------------

msg = MIMEText("这是一封从服务器发送的测试邮件。", "plain", "utf-8")
msg["Subject"] = "SMTP 功能测试"
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL

try:
    # 连接到 QQ 邮箱的 SMTP 服务器，SSL 加密，端口 465
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)

    # 启用 Debug 模式，打印出详细的交互信息
    server.set_debuglevel(1)

    # 登录邮箱
    server.login(SENDER_EMAIL, SENDER_AUTH_CODE)

    # 发送邮件
    server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())

    # 关闭连接
    server.quit()
    print("✅ 邮件发送成功！")

except smtplib.SMTPException as e:
    print(f"❌ 邮件发送失败，原因: {e}")
