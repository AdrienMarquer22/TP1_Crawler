import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import socket

socket.setdefaulttimeout(1) # si un site met du temp à charger




class Crawler():
    def __init__(self,url,limit=50,output=[]) -> None:
        self.url=url
        self.limit = limit
        self.output = output

    def run(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        for l in links : 
            rp = RobotFileParser()
            try: ## try si url pas bon
                rp.set_url(urlparse(l).scheme + "://" + urlparse(l).hostname + "/robots.txt")
                try : # try si le site ne charge pas
                    rp.read()
                    if rp.can_fetch("*", l):
                        self.output.append(l)
                    if len(self.output) == self.limit :
                        return self.output
                except:
                    pass

            except:
                pass

        if len(self.output) == self.limit :
                return self.output
        else : 
            for elem in self.output:
                time.sleep(5)
                Crawler_bis=Crawler(elem,self.limit,self.output)
                self.output=Crawler_bis.run()
                if len(self.output) == self.limit :
                    return self.output


    def get_output(self):
        return self.output
    

    def save(self,name):
        with open(name+".txt", 'w') as f:
            f.write("\n".join(map(str, self.output)))
