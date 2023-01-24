# Adrien MARQUER - TP1 Crawler


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage

There is 4 arguments to use :

- `--url` : That take the url thaht you want to crawl
- `--limit` : The limit of pages thaht we want to crawl (`default=50`)
- `--save_csv` : Put the name for the csv (`defaul="crawled_wepages"`)
- `--save_base` : Put the name for the database (`defaul="TP_Crawler"`)
- `--save_table` : Put the name for the table in database (`defaul="Crawler"`)
- `--sitemap` : If set we will use the sitemap.xml to crawl



```bash
python3 main.py --url https://www.ensai.fr/ --limit 15 --save crawled_webpages

# With sitemap : 
python3 main.py --url https://www.ensai.fr/ --limit 25 --sitemap
```


## Class

### Crawler
The `Crawler` class is a web crawler that can be used to scrape links and other information from a website. The class has several methods that can be used to customize the behavior of the crawler and retrieve information from the website.


The `__init__` method initializes the class with a URL, a limit for the number of links to retrieve, and an output list. 

The `run_loop` method then retrieves the page content from the URL and parses it to extract all of the links on the page. 

The `init_robot` method checks whether a robots.txt file exists for the website and, if it does, reads it to determine which links the crawler is allowed to access.

The `run` method then iterates through the list of links and, for each one, calls the `run_loop` method again to extract any additional links. If the limit for the number of links is reached, the method returns the output list.

The `site_map` method retrieves the sitemap for the website, if one exists, and extracts the links and last modification dates for each page. 

The `save_html_in_db` method can be used to save the HTML content of the pages in a database. If the last modification date has already been extracted, it is included in the database along with the URL and HTML content.Otherwise, it scans the meta of the page to find the date. 

### Database 

The `Database` class is a simple class that can be used to connect to a SQLite database and perform basic CRUD operations. The class has several methods that can be used to interact with the database.


The `__init__` method initializes the class with the name of the database, and creates a connection to the database using the sqlite3 library.

The `init_table` method is used to create a new table in the database with the specified name, and can also drop an existing table with the same name.

The `insert` method is used to insert data into the specified table, and takes in a list of elements to insert. 

The `create_html_from_link` method is used to recreate the html page from the specified link in the database.




