from requests import get
from lxml import html
import json

# André Marcos Hinckel
# Jose Henrique Lenz Pellet
# Leonardo Souza Nunes

url = 'https://pc.sc.gov.br//?page_id=1258'
response = get(url) # Requisição para o site

tree = html.fromstring(response.content) # Armazena no 'tree' o content do site
articles = tree.xpath("//article[contains(@class, 'elementor-post')]") # Salva na variável a parte do HTML que contem tal classe (Aqui no caso, são todos os artigos do site)

news_articles = [] # Cria um array vazio de novos artigos

for article in articles: # Percorre os artigos da variável 'articles'. Para cada artigo vai definir, Titulo, Descrição, Data, Link da imagem, Link do artigo

    title = article.xpath(".//h3[@class='elementor-post__title']/a/text()")[0].strip() # Para definir o título, procura parte que seja um H3 e tenha tal classe
    description = article.xpath(".//div[@class='elementor-post__excerpt']/p/text()")[0].strip() # Para definir a descrição, procura parte que seja um DIV e tenha tal classe
    date = article.xpath(".//div[@class='elementor-post__meta-data']/span[@class='elementor-post-date']/text()")[
        0].strip() # Para definir a data, procura parte que seja uma DIV e depois SPAN e que tenha tal classe
    image_url = article.xpath(".//div[@class='elementor-post__thumbnail']/img/@src")[0] # Para definir o link da imagem, procura parte que seja uma DIV e depois IMG e pega o @src
    link = article.xpath(".//h3[@class='elementor-post__title']/a/@href")[0] # Para definir o link, procura parte que seja um H3 e pega o href dele

    article_data = {
        'title': title,
        'description': description,
        'date': date,
        'image': image_url,
        'link': link
    } # Cria um objeto com o que foi definido

    news_articles.append(article_data) # Acrescenta no array criado o objeto que acabou de ser preenchido

with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(news_articles, f, ensure_ascii=False, indent=4) # Cria um arquivo JSON chamado news.json e coloca nele o array criado.
