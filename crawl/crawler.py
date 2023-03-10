import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import socket
from datetime import datetime
import csv
from crawl.database import Database
from crawl.thread import MyThread
# If an url take too much time too load
socket.setdefaulttimeout(2)





class Crawler():
    def __init__(self,url,limit=50,output=[]) -> None:
        self.url=url
        self.limit = limit
        self.output = output
        self.robot_cache={}

    def crawl_page(self,url):
        try: # if page don't load
            page = requests.get(url,timeout=10)
        except:
            pass
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
        if url in self.robot_cache:
            return self.robot_cache[url]
        else:
            rp = RobotFileParser()
            try:## try If the result is not an url 
                rp.set_url(urlparse(url).scheme + "://" + urlparse(url).hostname + "/robots.txt")
                try: # try If the url didnt't load
                    rp.read()
                    self.robot_cache[url] = rp
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
                try: # try if page load
                    page = requests.get(elem[0],timeout=5)
                    soup = BeautifulSoup(page.content, features="html.parser")
                    try: # try if we find a date
                        lastmod=soup.find("meta", {"property":"article:modified_time"}).get('content')
                        lastmod_datetime = datetime.strptime(lastmod, "%Y-%m-%dT%H:%M:%S+00:00")
                        lastmod_datetime_str = lastmod_datetime.strftime("%m/%d/%Y, %H:%M:%S")
                    except:
                        lastmod_datetime_str ='NaN'
                    db.insert(name_table,[elem[0],lastmod_datetime_str,page.text])
                    db.commit()
                except:
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

    def run_multi(self, max_threads=5):
        stop=False
        self.last_mod=False
        self.output=self.crawl_page(self.url)
        if len(self.output) >= self.limit :
            return self.output
        else : 
            
            j=0
            while len(self.output) <= self.limit:
                threads = [] 
                website_in_threads=[]
                for _ in range(max_threads):
                    url = self.output[j][0]
                    website = urlparse(url).scheme + "://" + urlparse(url).hostname
                    if  website in website_in_threads: # to make sure that we dont crawl a page from the same website at once so if website already in the list then we find the closest website that is not in the list 
                        for i in range(j,len(self.output)):
                            website_bis = urlparse(self.output[i][0]).scheme + "://" + urlparse(self.output[i][0]).hostname
                            if website_bis not in website_in_threads:
                                url_bis=url
                                url=self.output[i][0]
                                self.output[i][0]=url_bis
                                break
                            if i == len(self.output)-1 : # in case we reach the end of the list
                                stop=True
            
                        
                    if stop:
                        break
                    t = MyThread(cr=self,url=url)
                    j+=1
                    t.start()
                    threads.append(t)
                    website_in_threads.append(urlparse(url).scheme + "://" + urlparse(url).hostname)
                    
                     
                for t in threads:
                    t.join()
                time.sleep(5)
        self.output=self.output[0:self.limit]
