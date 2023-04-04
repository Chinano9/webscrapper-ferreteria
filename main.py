from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_soup(url:str) -> BeautifulSoup:
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode('utf-8')
    return BeautifulSoup(html, "html.parser")

def get_page_numbers(soup:BeautifulSoup) -> int:
    text = soup.find_all('a', ['class', 'js-search-link'])
    *frst,num,extra = text
    return int(num.string)

def main():
    soup = get_soup("https://hagalo.mx/2805-ferreteria-y-herrajes")
    page_numbers = get_page_numbers(soup)
    print(page_numbers)

if __name__ == '__main__':
    main()