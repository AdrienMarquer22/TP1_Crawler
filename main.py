from crawler import Crawler

crawler=Crawler("https://www.ensai.fr/",300)
crawler.run()
print(crawler.get_output())
crawler.save("data")