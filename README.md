# wikipedia-crawler
This is a program to crawl entire Wikipedia using *breath-first* method and extract information from all the pages.

## Summary
This is a Python program to crawl Wikipedia pages and extract relevant information from the pages. It crawls in breath-first fashion and stores all the links that it has to crawl, thus slowly covering **all** of the Wikipedia. The program can be edited to extract customized information according to one's choice. MySQLdb library is then used to write the information into a MySQL table for further use. 

## Compatability
This program is written in Python 3.4 and can run on any version of Python (3.x). It is a download-and-run program with couple of changes according to user's requirements.

## Status
This is the first stable version of the program which is ready-to-run, but still under development. Many more features will be added to it later.

## Disclaimer
This program lets you crawl the pages of Wikipedia for information. It downloads the entire page of Wikipedia that it is currently crawling. If this program is let to run for a long period of time, **it can crawl the entire online database of Wikipedia, which is highly discouraged!!!**

Please, only use this program for educational purposes, by reviewing the content (in form of text, images, graphics, or any other form), copyright, and its licence. Also, crawling multiple different pages puts **a lot of pressure** on Wikipedia servers. Please follow the Wikipedia `robots.txt` guidelines to understand the restrictions on requests-per-second that can be made by an external robot. According to Wikipedia, slow bots are allowed to crawl!
