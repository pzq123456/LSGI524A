from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_email(subject, body, to_email, log_file_path):
    from_email = "你的实际邮箱地址"
    from_password = "你的实际邮箱密码"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(log_file_path, 'rb') as f:
        attachment = MIMEText(f.read(), 'base64', 'utf-8')
        attachment.add_header('Content-Disposition', 'attachment', filename='log.txt')
        msg.attach(attachment)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        logger.info("邮件发送成功")
    except Exception as e:
        logger.error(f"邮件发送失败: {e}")

# 示例调用
send_email(
    subject="测试邮件",
    body="这是一个测试邮件的内容",
    to_email="example@mail.com",
    log_file_path="path/to/your/log.txt"
)
