import smtplib
import requests
import threading
import schedule
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 邮件配置信息
smtp_server = config['EmailConfig']['smtp_server']
smtp_port = int(config['EmailConfig']['smtp_port'])
sender_email = config['EmailConfig']['sender_email']

# 支持多个接收邮箱
receiver_emails = config['EmailConfig']['receiver_email'].split(',')

email_password = config['EmailConfig']['email_password']


def send_email(subject, body):
    """ 发送邮件函数 """
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # 将多个接收邮箱作为收件人
    msg['To'] = ', '.join(receiver_emails)

    try:
        # 使用 TLS 加密连接
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # 启用 TLS 加密
            server.login(sender_email, email_password)  # 使用授权码进行登录
            server.sendmail(sender_email, receiver_emails, msg.as_string())
        print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送失败: {e}")


def fetch_hacker_news():
    """ 获取 Hacker News 热门新闻 """
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    response.raise_for_status()

    # 解析 HTML 内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有新闻条目
    items = soup.select('.athing')

    news_data = []
    for item in items:
        title_tag = item.select_one('.storylink')
        title = title_tag.get_text() if title_tag else None
        link = title_tag['href'] if title_tag else None
        subtext = item.find_next_sibling('tr').select_one('.subtext')

        if subtext:
            score = subtext.select_one('.score')
            score = int(score.get_text().split()[0]) if score else 0

            # 提取日期并处理
            age_tag = subtext.select_one('.age a')
            age = age_tag.get_text() if age_tag else "unknown"

            news_data.append({
                'title': title,
                'link': link,
                'score': score,
                'age': age
            })

    return news_data


def fetch_github_progress():
    """ 模拟获取 GitHub 项目进展并生成报告 """
    # 假设我们已经有 GitHub 项目进展的提取代码
    repo_name = "GitHub-Sentinel"
    date_str = datetime.now().strftime("%Y-%m-%d")
    issues = ["Issue 1", "Issue 2", "Issue 3"]
    pull_requests = ["PR 1", "PR 2", "PR 3"]

    report = f"GitHub 项目报告 - {repo_name} ({date_str})\n\n"
    report += "## Issues\n" + "\n".join([f"- {issue}" for issue in issues]) + "\n\n"
    report += "## Pull Requests\n" + "\n".join([f"- {pr}" for pr in pull_requests]) + "\n"

    send_email(f"GitHub 项目进展报告 - {repo_name}", report)
    print(f"GitHub 项目报告已发送：{repo_name}")


def hacker_news_report():
    """ 获取 Hacker News 热门新闻并发送报告 """
    news_data = fetch_hacker_news()
    report = "Hacker News 热门新闻报告\n\n"
    for news in news_data[:5]:  # 只取前5条新闻
        report += f"标题: {news['title']}\n链接: {news['link']}\n分数: {news['score']}\n年龄: {news['age']}\n\n"

    send_email("Hacker News 热门新闻报告", report)
    print("Hacker News 热门新闻报告已发送！")


def schedule_github_progress():
    """ 设置 GitHub 项目进展的定时任务 """
    schedule.every().day.at("09:00").do(fetch_github_progress)


def schedule_hacker_news():
    """ 设置获取 Hacker News 热门新闻的定时任务 """
    schedule.every().hour.do(hacker_news_report)


def start_scheduler():
    """ 启动调度器，执行守护进程任务 """
    while True:
        schedule.run_pending()
        time.sleep(1)


# 启动守护进程来获取 GitHub 项目进展和 Hacker News 热门新闻
if __name__ == "__main__":
    # 启动 GitHub 项目进展调度
    schedule_github_progress()

    # 启动 Hacker News 新闻调度
    schedule_hacker_news()

    # 在后台启动调度器守护进程
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()

    print("守护进程正在运行...")
    while True:
        time.sleep(60)  # 主线程保持运行
