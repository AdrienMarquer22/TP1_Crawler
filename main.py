from crawl.crawler import Crawler
from crawl.database import Database
import argparse



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url')
    parser.add_argument('--limit', type=int,default=50)
    parser.add_argument('--save_csv',default="crawled_wepages")

    parser.add_argument('--save_base',default="TP_Crawler")

    parser.add_argument('--save_table',default="Crawler")

    parser.add_argument('--sitemap', action='store_true',default=False)



    args = parser.parse_args()

    crawler=Crawler(args.url,args.limit)

    if args.sitemap:
        crawler.site_map()
    else:
        crawler.run()

    crawler.save(args.save)

    

    base= Database(args.save_base)
    base.init_tabe(args.save_table)
    crawler.save_html_in_db(base,args.save_table)



    #crawler=Crawler("https://www.ensai.fr/",3)
    # crawler.run()
    # crawler.save("crawled_webpages")

    # base= Database("sitemap")
    # base.init_tabe("Crawler")

    # crawler.save_html_in_db(base,"Crawler")
