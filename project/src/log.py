import json
import logging
from logging.handlers import RotatingFileHandler

import os
import random
import time

from tqdm import tqdm
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from env import get_all

PATH = os.path.join(os.path.dirname(__file__))

SAVE_PATH = os.path.join(PATH, '../', 'output', 'log')

if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

checkpoint_file = os.path.join(SAVE_PATH, 'checkpoint.json')

# 配置日志
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(os.path.join(SAVE_PATH, 'log.txt'), maxBytes=1024 * 1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 存储已完成任务的文件

CHECKPOINT_PATH = os.path.join(SAVE_PATH, 'checkpoint')

def save_checkpoint(task_id, status):
    # 失败任务需要记录在文件中
    # 数据结构如下
    # failed_tasks
    # current_task

    # 首先尝试读取文件
    try:
        with open(CHECKPOINT_PATH, 'r') as f:
            data = f.read()
            if data:
                data = eval(data)
            else:
                data = {}
    except:
        data = {}

    # 如果是失败任务，记录在 failed_tasks 中
    if status == 'failed':
        if 'failed_tasks' not in data:
            data['failed_tasks'] = []
        data['failed_tasks'].append(task_id)
    # 记录当前任务
    data['current_task'] = task_id

    # 写入文件
    with open(CHECKPOINT_PATH, 'w') as f:
        f.write(str(data))
    
def load_checkpoint():
    try:
        with open(CHECKPOINT_PATH, 'r') as f:
            data = f.read()
            if data:
                data = eval(data)
            else:
                data = {}
    except:
        data = {}
    return data
  
def get_logger():
    return logger

def send_email(subject, body, log_file_path):

    from_email, from_password, to_email = get_all()

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(log_file_path, 'rb') as f:
        attachment = MIMEText(f.read(), 'base64', 'utf-8')
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(log_file_path))
        msg.attach(attachment)

    try:
        # 改为使用SSL
        server = smtplib.SMTP_SSL('smtp.163.com', 465)
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        logging.info("邮件发送成功")
    except Exception as e:
        logging.error(f"邮件发送失败: {e}")


if __name__ == "__main__":
    # 测试日志
    logger.info("测试日志")
    # 测试发送邮件
    send_email("测试邮件", "这是一封测试邮件", os.path.join(SAVE_PATH, 'log.txt'))

# # 读取已完成任务
# def load_completed_tasks():
#     if os.path.exists(checkpoint_file):
#         with open(checkpoint_file, 'r') as f:
#             return set(json.load(f))
#     return set()

# # 保存已完成任务
# def save_completed_task(task_id):
#     completed_tasks = load_completed_tasks()
#     completed_tasks.add(task_id)
#     with open(checkpoint_file, 'w') as f:
#         json.dump(list(completed_tasks), f)

# # 模拟爬虫任务
# def scrape_task(total_tasks):
#     completed_tasks = load_completed_tasks()
#     for i in tqdm(range(total_tasks), desc="Scraping"):
#         if i in completed_tasks:
#             continue  # 跳过已完成的任务
#         # 模拟处理时间
#         time.sleep(0.1)
#         # 随机产生成功或错误
#         if random.choice([True, False]):
#             logger.info(f'Task {i + 1}/{total_tasks} completed successfully.')
#             save_completed_task(i)  # 保存已完成任务
#         else:
#             logger.error(f'Task {i + 1}/{total_tasks} failed with an error.')

# if __name__ == "__main__":
#     total_tasks = 10
#     scrape_task(total_tasks)

#     # 重新运行
#     load_completed_tasks()
#     scrape_task(total_tasks)
