import configparser
from scheduler import Scheduler

def main():
    # 加载配置文件
    config = configparser.ConfigParser()
    config.read("config.ini")

    # 从配置文件中获取 GitHub 和 OpenAI API 密钥
    github_token = config.get("github", "api_token")
    openai_key = config.get("openai", "api_key")

    # 初始化订阅的仓库列表
    repos = []

    print("欢迎使用 GitHub Sentinel 订阅系统！")
    print("请输入要订阅的 GitHub 仓库 URL。输入 'done' 完成订阅。")

    # 循环输入订阅仓库 URL
    while True:
        repo_url = input("请输入 GitHub 仓库 URL 或输入 'done' 完成：")
        if repo_url.lower() == 'done':
            break
        elif repo_url.startswith("https://github.com/"):
            repos.append(repo_url)
            print(f"已添加仓库：{repo_url}")
        else:
            print("无效的 URL，请输入有效的 GitHub 仓库 URL。")

    if not repos:
        print("没有订阅任何仓库。程序已退出。")
        return

    # 初始化 Scheduler
    scheduler = Scheduler(repos, github_token, openai_key)

    # 设定每日定时任务
    hour = int(input("请输入每日任务的小时（0-23）："))
    minute = int(input("请输入每日任务的分钟（0-59）："))
    scheduler.schedule_daily_task(hour=hour, minute=minute)

if __name__ == "__main__":
    main()
