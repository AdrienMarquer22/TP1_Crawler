import threading


class MyThread(threading.Thread):
    def __init__(self,cr,url):
        threading.Thread.__init__(self)
        self.cr = cr
        self.url = url

    def run(self):
        if len(self.cr.output) <= self.cr.limit:
            self.cr.crawl_page(self.url)
