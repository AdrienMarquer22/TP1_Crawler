import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import socket
from datetime import datetime
import csv
from crawl.database import Database
import concurrent.futures
from crawl.thread import MyThread
# If an url take too much time too load
socket.setdefaulttimeout(2)





class Crawler():
    def __init__(self,url,limit=50,output=[]) -> None:
        self.url=url
        self.limit = limit
        self.output = output

    def crawl_page(self,url):
        print(url,len(self.output))
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        for l in links : 
            rp = self.init_robot(l)
            if rp and rp.can_fetch("*", l):
                self.output.append([l])
                if len(self.output) == self.limit :
                    return self.output
        return self.output

    def init_robot(self,url):
        rp = RobotFileParser()
        try: ## try If the result is not an url 
            rp.set_url(urlparse(url).scheme + "://" + urlparse(url).hostname + "/robots.txt")
            try : # try If the url didnt't load
                rp.read()
                return rp
            except:
                    return False
        except:
            return False

        

    def run(self):
        self.last_mod=False #We dont have the last modification time n this case
        self.output=self.crawl_page(url=self.url)
        if len(self.output) == self.limit :
                return self.output
        else : 
            for elem in self.output:
                time.sleep(5)
                self.crawl_page(url=elem[0])
                if len(self.output) == self.limit :
                    return self.output
            self.run()




    def site_map(self):
        self.last_mod = True # We store the last modification time 
        rp = self.init_robot(self.url)
        self.sitemap = rp.site_maps()
        if self.sitemap:
            for site in self.sitemap:
                time.sleep(5)
                page = requests.get(site)
                soup = BeautifulSoup(page.content, features="xml")
                for url_tag in soup.find_all('url'):
                    link = url_tag.find('loc').text
                    lastmod = url_tag.find('lastmod').text
                    lastmod_datetime = datetime.strptime(lastmod, "%Y-%m-%dT%H:%M:%S+00:00")
                    self.output.append([link,lastmod_datetime.strftime("%m/%d/%Y, %H:%M:%S")])
                    if len(self.output) == self.limit :
                        return self.output
            return self.output
        else:
            raise Exception("sitemap.xml not found")


    def save_html_in_db(self,db:Database,name_table):
        if self.last_mod: # If we already have the last modification date we dont nned to extract it
            for elem in self.output:
                time.sleep(5)
                db.insert(name_table,[elem[0],elem[1],requests.get(elem[0]).text])
                db.commit()
        else:
            for elem in self.output:
                time.sleep(5)
                page = requests.get(elem[0])
                soup = BeautifulSoup(page.content, features="html.parser")
                try:
                    lastmod=soup.find("meta", {"property":"article:modified_time"}).get('content')
                    lastmod_datetime = datetime.strptime(lastmod, "%Y-%m-%dT%H:%M:%S+00:00")
                    lastmod_datetime_str = lastmod_datetime.strftime("%m/%d/%Y, %H:%M:%S")
                except:
                    lastmod_datetime_str ='NaN'
                
                db.insert(name_table,[elem[0],lastmod_datetime_str,page.text])
                db.commit()

            pass
            

    def reset(self):
        self.output=[]

    def save(self,name="crawled_webpages"):
        with open(name+".csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.output)

    def get_output(self):
        return self.output

    def get_sitemaps(self):
        return self.sitemap
    
    def set_limit(self,limit):
        self.limit = limit

    def run_multi(self, max_threads=3):
        self.last_mod=False
        self.output=self.crawl_page(self.url)
        if len(self.output) >= self.limit :
            return self.output
        else : 
            
            j=0
            while len(self.output) <= self.limit:
                threads = []
                for i in range(max_threads):
                    print("tt   t",self.output[j][0])
                    t = MyThread(cr=self,url=self.output[j][0])
                    j+=1
                    t.start()
                    threads.append(t)

                for t in threads:
                    t.join()
                time.sleep(5)
        self.output=self.output[0:self.limit]
