from crawler import Crawler
from database import Database




if __name__=="__main__":
    crawler=Crawler("https://www.ensai.fr/",3)
    crawler.run()
    crawler.save("data2")

    base= Database("sitemap")
    base.init_tabe("Crawler")

    crawler.save_html_in_db(base,"Crawler")
