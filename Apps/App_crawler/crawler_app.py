import requests
from System.Crawler.crawler import Crawler

import time


def add_document(doc, port):
    # defining the api-endpoint
    API_ENDPOINT = f"http://127.0.0.1:{port}/add_document"

    data = str(doc)
    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=data)
    path = doc.split('\n')[0]
    print(f"Sent document {path} to slave with port number {port}")


if __name__ == '__main__':
    crawler = Crawler(downloaded=False)
    print(crawler.downloaded)
    crawler.get_collection()

    while True:
        # g = input()
        doc = crawler.retrieve_docs()
        try:
            add_document(doc, 5500)
        except:
            pass

        try:
            add_document(doc, 6500)
        except:
            pass
        time.sleep(2.5)
