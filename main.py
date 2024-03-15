from requests import get
from lxml import html
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')

stop_words = set(stopwords.words('portuguese'))
stemmer = RSLPStemmer()

categorias = {
    'Homicídio': ["assassinato", "morte", "investigação", "homicído", "corpo", "homicido", "execução", "dolos", "assassino",
                  "perícia", "cena do crime", "fatalidade"],
    'Latrocínio': ["roubo seguido morte", "assalto fatal", "assalto", "latrocínio", "roubo", "furto", "furtado", "violência",
                   "vítima de roubo", "morte em assalto", "criminalidade", "violento"],
    'Feminicídio': ["assassinato de mulher", "violência doméstica", "crime contra mulher", "feminicídio", "assassinato por parceiro",
                    "morte por violência doméstica", "crime passional", "agressão contra mulher"],
    'Entorpecentes': ["tráfico de drogas", "apreensão de drogas", "operação antidrogas", "entorpecentes", "drogas", "apreensão",
                      "narcotráfico", "ilícitas", "combate ao tráfico", "drogas sintéticas", "operação policial", "substâncias proibidas",
                      "tráfico internacional", "crack", "maconha", "cocaína"],
    'Contra Animais': ["maus-tratos", "abandono de animais", "tráfico de espécies", "caça ilegal", "exploração animal"],
    'Corrupção': ["deflagrar", "corrupção", "desvio", "suborno"],
    'Segurança': ["operações de segurança", "tecnologia em segurança", "estratégia de segurança", "segurança", "câmeras", "monitoramento",
                  "força policial", "policiamento", "vigilânci", "prevenção ao crime", "segurança pública", "patrulhamento",
                  "guarda civil"],
    'CyberCrimes': ["cyberbullying", "virtual", "internet"],
    'Agressão Sexual': ["abuso", "agressão sexual", "estupro", "violação", "vulnerável"],
    'Ações Comunitárias': ["programas comunitários", "engajamento comunitário", "segurança comunitária", "comunitárias",
                           "palestras", "parcerias", "conscientização", "educativas", "planejamento", "seminário", "instituições",
                           "homenagem", "iniciativa social", "apoio à comunidade", "programa de prevenção", "ações sociais",
                           "intervenção comunitária", "projeto social"],
    'Fraudes e Estelionato': ["golpe", "fraude", "estelionato", "crime financeiro", "falsificação", "engano", "fraude online"],
    'Crimes Ambientais': ["desmatamento", "crime ambiental", "apreensão de animais", "poluição", "queimadas", "tráfico de animais",
                          "desmatamento ilegal"],
    'Tráfico de Pessoas': ["exploração", "sequestro", "tráfico humano", "exploração sexual", "trabalho escravo", "resgate de vítimas"]
}


def categorizar(texto):
    palavras = word_tokenize(texto.lower())
    palavras_filtradas = [palavra for palavra in palavras if not palavra in stop_words]
    stems = [stemmer.stem(palavra) for palavra in palavras_filtradas]

    for categoria, keywords in categorias.items():
        if any(stem in stems for keyword in keywords for stem in [stemmer.stem(keyword)]):
            return categoria
    return 'Outros'


url = 'https://pc.sc.gov.br//?page_id=1258'
response = get(url)
tree = html.fromstring(response.content)
articles = tree.xpath("//article[contains(@class, 'elementor-post')]")

news_articles = []

for page in range(1, 4):
    url = f'https://pc.sc.gov.br/?page={page}&page_id=1258'
    response = get(url)
    tree = html.fromstring(response.content)
    articles = tree.xpath("//article[contains(@class, 'elementor-post')]")

    for article in articles:
        title = article.xpath(".//h3[@class='elementor-post__title']/a/text()")[0].strip()
        description = article.xpath(".//div[@class='elementor-post__excerpt']/p/text()")[0].strip()
        date = article.xpath(".//div[@class='elementor-post__meta-data']/span[@class='elementor-post-date']/text()")[0].strip()
        image_url = article.xpath(".//div[@class='elementor-post__thumbnail']/img/@src")[0]
        link = article.xpath(".//h3[@class='elementor-post__title']/a/@href")[0]

        category = categorizar(title + " " + description)

        news_articles.append({
            'title': title,
            'description': description,
            'date': date,
            'image': image_url,
            'link': link,
            'category': category
        })

with open('news_categorized.json', 'w', encoding='utf-8') as f:
    json.dump(news_articles, f, ensure_ascii=False, indent=4)