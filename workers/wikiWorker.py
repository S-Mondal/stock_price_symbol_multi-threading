import requests
from bs4 import BeautifulSoup
from lxml import html

class WikiWorker:
    def __init__(self):
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    @staticmethod
    def _extract_company_symbols(page_html):
        soup = BeautifulSoup(page_html, 'lxml')
        table = soup.find(id='constituents')
        tablerows = table.find_all('tr')
        for row in tablerows[1:]:
            symbol = row.find('td').text.strip()
            yield symbol

    def get_companies(self):
        response = requests.get(self._url)
        if response.ok:
            yield from self._extract_company_symbols(response.text)
        
class WikiWorkerIndia:
    def __init__(self):
        self._url = "https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_National_Stock_Exchange_of_India"

    @staticmethod
    def _extract_company_symbols(page_html):
        contents = html.fromstring(page_html)
        for i in range(2, 29):
            count = 2
            while True:
                data = contents.xpath(f'/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table[{i}]/tbody/tr[{count}]/td[1]/a[2]')
                if not data:
                    break
                symbol=data[0].text
                if symbol is None:
                    break
                count += 1
                yield f"{symbol}.NS"


    def get_companies(self):
        response = requests.get(self._url)
        if response.ok:
            yield from self._extract_company_symbols(response.text)
        

if __name__ == '__main__':
    worker = WikiWorkerIndia()
    for x in worker.get_companies():
        print(x)
