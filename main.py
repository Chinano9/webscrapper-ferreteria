#!/usr/bin/python3

from urllib.request import urlopen
from bs4 import BeautifulSoup, ResultSet

def get_soup(url:str) -> BeautifulSoup:
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode('utf-8')
    return BeautifulSoup(html, 'html.parser')

def get_page_numbers(soup:BeautifulSoup) -> int:
    text = soup.find_all('a', ['class', 'js-search-link'])
    *frst, num, last = text
    return int(num.string)

def extract_articles(page:str) -> list[dict[str, str]]:
    soup = get_soup(page)
    articles = soup.find_all('article', class_='style_product_default')
    article_list = list()

    for article in articles:
        # Defines the types that the dict will have
        article_dict:dict = {
            'name':str,
            'price':str,
        }
        article_name = article.find('a', class_='product_name')
        article_price = article.find('span', class_='price')
        # Fills the article dictionary
        article_dict['name'] = article_name.string
        article_dict['price'] = article_price.string
        print(article_dict)
        article_list.append(article_dict)

    return article_list

def main():
    # Gets the page quantity
    main_page = get_soup('https://hagalo.mx/2805-ferreteria-y-herrajes')
    page_numbers = get_page_numbers(main_page)

    # Extracts articles from every page
    for page in range(1, page_numbers):
        url = 'https://hagalo.mx/2805-ferreteria-y-herrajes?page={page}'
        article_list = extract_articles(url.format(page=page))

    print(page_numbers)

if __name__ == '__main__':
    main()