from workers.wikiWorker import WikiWorker, WikiWorkerIndia
from workers.yahooFinanceWorker import YahooFinanceWorker
from workers.postgresWorker import PostgresWorker
from multiprocessing import Queue

# obj = WikiWorker()
obj = WikiWorkerIndia()

workers = []
symbol_queue = Queue()
output_queue = Queue()
no_of_workers = 8
for _ in range(no_of_workers):
    worker =  YahooFinanceWorker(symbol_queue, output_queue)
    workers.append(worker)
    
output_workers = []
for _ in range(no_of_workers):
    worker =  PostgresWorker(output_queue)
    output_workers.append(worker) 
    
for symbol in obj.get_companies():
    symbol_queue.put(symbol)

# putting 'DONE' to denote end of the queue
for _ in range(no_of_workers):
    symbol_queue.put("DONE")

for w in workers:
    w.join()

for w in output_workers:
    w.join()