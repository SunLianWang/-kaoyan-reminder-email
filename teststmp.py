"""一个用于测试 SMTP 邮件发送的脚本。"""

import smtplib
from email.mime.text import MIMEText

msg = MIMEText("测试内容", "plain", "utf-8")
msg["Subject"] = "测试邮件"
msg["From"] = "1958232837@qq.com"
msg["To"] = "1958232837@qq.com"

try:
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.set_debuglevel(1)  # 添加这行，打开详细日志
    server.login("1958232837@qq.com", "pjsvghoxgcozbddb")  # 这是你的 SMTP 授权码
    server.sendmail(
        from_addr="1958232837@qq.com",
        to_addrs=["1958232837@qq.com"],
        msg=msg.as_string(),
    )
    server.quit()
    print("✅ 测试成功")
except smtplib.SMTPException as e:
    print("❌ 测试失败:", e)
