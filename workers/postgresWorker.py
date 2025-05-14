import threading, sqlalchemy
from urllib.parse import quote_plus
from datetime import datetime

class PostgresWorker(threading.Thread):
    def __init__(self, output_queue, **kwargs):
        super().__init__(**kwargs)
        self._output_queue = output_queue
        self._engine = sqlalchemy.create_engine('postgresql+psycopg2://root:%s@localhost:5432/test' % quote_plus('souvik@linux'))
        self.start()

    def run(self):
        while True:
            symbol, price, company = self._output_queue.get()
            # print(symbol, price, company)
            if symbol == 'DONE':
                break
            with self._engine.connect() as conn:
                obj = conn.execute(sqlalchemy.text("SELECT * FROM symbol_price WHERE symbol_price.symbol = :symbol"), {"symbol":symbol})
                chk = obj.fetchone()
                if chk is None:
                    # print("Inserting", symbol)
                    conn.execute(sqlalchemy.text("INSERT INTO symbol_price(symbol, price, company, updated_at) VALUES(:symbol, :price, :company, :updated_at)"), {
                        "symbol":symbol, 
                        "price":price, 
                        "company":company,
                        "updated_at":datetime.now()
                        })
                    conn.commit()
                else:
                    # print("Updating", symbol)
                    conn.execute(sqlalchemy.text("UPDATE symbol_price SET price=:price, company=:company, updated_at=:updated_at WHERE symbol=:symbol"), {
                        "symbol":symbol, 
                        "price":price, 
                        "company":company,
                        "updated_at":datetime.now()
                        })
                    conn.commit()

