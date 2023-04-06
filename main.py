#!/usr/bin/python3

from urllib.request import urlopen
from bs4 import BeautifulSoup, ResultSet

URL = 'https://hagalo.mx/2805-ferreteria-y-herrajes'


def get_soup(url:str) -> BeautifulSoup:
    """Gets the page source code and returns an BeautifulSoup object"""
    print("Getting page source code...")
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode('utf-8')
    return BeautifulSoup(html, 'html.parser')

def get_page_numbers(soup:BeautifulSoup) -> int:
    """Gets the page numbers, and returns the number"""
    print("Getting number of pages...")
    text = soup.find_all('a', ['class', 'js-search-link'])
    *frst, num, last = text
    return int(num.string)

def extract_articles(page:str, actual_page:int, last_page:int) -> list[dict]:
    """Extracts the articles of the store and returns a list with the articles"""
    soup = get_soup(page)
    print("Extracting articles, page %1d of %2d" % (actual_page, last_page))
    articles = soup.find_all('article', class_='style_product_default')
    article_list = list()

    for article in articles:
        article_name = article.find('a', class_='product_name').string
        article_price = float((article.find('span', class_='price').string).replace('$','').replace(',',''))
        artile_image = article.find('img', class_='first-image').get('src')
        article_stock = article.find('div', class_='availability-list').find('span').string
        if article_stock == 'Out of stock':
            article_stock = 0
        else:
            article_stock = int(article_stock.split()[0])
        # Fills the article dictionary
        article_dict:dict = {
            'name':article_name,
            'price':article_price,
            'image':artile_image,
            'stock':article_stock,
        }

        article_list.append(article_dict)

    return article_list

def main():
    # Gets the page quantity
    main_page = get_soup(URL)
    page_numbers = get_page_numbers(main_page)
    all_articles = list()
    # Extracts articles from every page
    for page in range(1, page_numbers):
        url = 'https://hagalo.mx/2805-ferreteria-y-herrajes?page={page}'
        article_list = extract_articles(url.format(page=page), page, page_numbers)
        for article in article_list:
            all_articles.append(article)
    print(all_articles)

    print(page_numbers)

if __name__ == '__main__':
    main()