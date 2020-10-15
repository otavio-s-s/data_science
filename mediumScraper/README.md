[![author](https://badgen.net/badge/Author/otavio-s-s/blue)](https://www.linkedin.com/in/otavioss28/) [![python](https://badgen.net/badge/Python/3.6+/yellow)](https://www.python.org) [![license](https://img.shields.io/badge/License-MIT-red)](https://github.com/otavio-s-s/data_science/blob/master/LICENSE) [![contributions](https://badgen.net/badge/Contributions/Welcome/green)](https://github.com/otavio-s-s/data_science/issues) 

# **Medium Scraper**
This code was designed to scrape data from Medium publications. It consists of one solo function that receives the publication URL and the year from which the data should be scraped. Read more about it [here](https://hackernoon.com/how-to-scrape-a-medium-publication-a-python-tutorial-for-beginners-o8u3t69).

The code returns a *DataFrame* and exports a *.csv* file. For every story in the publication and date specified the following information is scraped:

* Date;
* Title;
* Subtitle;
* Number of Claps;
* Number of Responses,
* Author's URL;
* Story's URL;
* Reading Time (mins);
* Number of sections;
* Section Titles;
* Number of Paragraphs;
* Paragraphs.

## **Prerequisites**

* Python 3.6+
* The following Python libraries:
  * [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
  * [requests](https://requests.readthedocs.io/en/master/)
  * [beautfulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
  
 ### **Running the code**
 `python mediumScraper.py`
  
 *** 
Feel free to contribute.
