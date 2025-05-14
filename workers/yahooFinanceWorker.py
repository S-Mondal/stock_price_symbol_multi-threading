import threading, requests, time, random
from lxml import html

class YahooFinanceWorker(threading.Thread):
    def __init__(self, symbol_queue, output_queue, **kwargs):
        super().__init__(**kwargs)
        self.base_url = 'https://finance.yahoo.com/quote/'
        self.symbol_queue = symbol_queue
        self.output_queue = output_queue
        self.start()
        # print("Threading started")

    def _execute(self, symbol):
        self._url = f"{self.base_url}{symbol}/"
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        response = requests.get(self._url, headers=headers)
        if not response.ok:
            headers = {
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)",
            }
            response = requests.get(self._url, headers=headers)
        if not response.ok:
            headers = {
                "User-Agent":"Mozilla/5.0",
            }
            response = requests.get(self._url, headers=headers)
        if not response.ok:
            print(symbol, response.status_code)
        if response.ok:
            contents = html.fromstring(response.text)
            try:
                price = round(float(contents.xpath('/html/body/div[2]/main/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[1]/span/text()')[0].replace(',','')), 2)
                company = contents.xpath('/html/body/div[2]/main/section/section/section/article/section[1]/div[1]/div/div[1]/section/h1/text()[1]')[0]
            except:
                return
            self.output_queue.put((symbol,price,company))

    def run(self):
        while True:
            symbol = self.symbol_queue.get()
            if symbol == "DONE":
                print("END OF THE QUEUE, TERMINATING...")
                self.output_queue.put(('DONE',0, ''))
                break
            self._execute(symbol)
            # time.sleep(20*random.random())


if __name__ == '__main__':
    # testing
    symbol = '63MOONS.NS'
    from multiprocessing import Queue
    symbol_queue = Queue()
    output_queue = Queue()
    obj = YahooFinanceWorker(symbol_queue, output_queue)
    symbol_queue.put(symbol)
    symbol_queue.put('DONE')
    obj.join()

