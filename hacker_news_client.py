import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def fetch_hacker_news():
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


def filter_news_by_time(news_data, start_datetime=None, end_datetime=None):
    # 获取当前时间
    now = datetime.now()

    filtered_news = []

    for news in news_data:
        # 处理新闻发布的时间（简化版本，只检查“小时”）
        if news['age'] == "unknown":
            continue

        # 计算新闻的发布时间
        if "hour" in news['age']:
            hours_ago = int(news['age'].split()[0])
            news_time = now - timedelta(hours=hours_ago)
        elif "day" in news['age']:
            days_ago = int(news['age'].split()[0])
            news_time = now - timedelta(days=days_ago)
        else:
            continue

        # 筛选出符合条件的新闻
        if (not start_datetime or news_time >= start_datetime) and (not end_datetime or news_time <= end_datetime):
            filtered_news.append(news)

    return filtered_news

if __name__ == '__main__':
    # 获取热门新闻
    news_data = fetch_hacker_news()
    # 输入开始时间和结束时间，精确到小时（格式：YYYY-MM-DD HH:MM）
    start_datetime_str = '2024-11-01 00:00'  # 示例：开始时间
    end_datetime_str = '2024-11-05 23:59'  # 示例：结束时间

    # 将字符串转换为 datetime 对象
    start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M')
    end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M')

    # 根据时间筛选新闻
    filtered_news = filter_news_by_time(news_data, start_datetime, end_datetime)

    # 打印筛选后的新闻
    for news in filtered_news:
        print(f"Title: {news['title']}\nLink: {news['link']}\nScore: {news['score']}\nAge: {news['age']}\n")
