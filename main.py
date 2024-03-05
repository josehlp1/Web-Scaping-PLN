from requests import get
from lxml import html
import json

url = 'https://pc.sc.gov.br//?page_id=1258'
response = get(url)

tree = html.fromstring(response.content)
articles = tree.xpath("//article[contains(@class, 'elementor-post')]")

news_articles = []

for article in articles:

    title = article.xpath(".//h3[@class='elementor-post__title']/a/text()")[0].strip()
    description = article.xpath(".//div[@class='elementor-post__excerpt']/p/text()")[0].strip()
    date = article.xpath(".//div[@class='elementor-post__meta-data']/span[@class='elementor-post-date']/text()")[
        0].strip()
    image_url = article.xpath(".//div[@class='elementor-post__thumbnail']/img/@src")[0]
    link = article.xpath(".//h3[@class='elementor-post__title']/a/@href")[0]

    article_data = {
        'title': title,
        'description': description,
        'date': date,
        'image': image_url,
        'link': link
    }

    news_articles.append(article_data)

with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(news_articles, f, ensure_ascii=False, indent=4)
