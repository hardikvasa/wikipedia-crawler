# wikipedia-crawler
This is a program to crawl entire Wikipedia using breath-first method and extract information from all the pages.

## Summary
This is a Python program to crawl wikipedia pages and extract relevant inforation from the pages. It crawls in breath-first fashion and stores all the links that it has to crawl thus slowly covering all of the wikipedia. The program can be edited to extract customized information according to one's choice. MySQLdb library is then used to write the information into a MySQL table for further use. 

## Compatability
This program is written in Python 3.4 and can run on any version of Ptyhon (3.x). It is a download-and-run program with couple of changes according to user's requirements.

## Status
This is first stable version of the program which is ready-to-run, but still under development. Many more features will be added to it shortly.

## Disclaimer
This program lets you crawl the pages of wikipedia for information. It downloads then entire page of wikipedia that it is currently crawling. If this program is let to run for a long period of time, it can crawl the entire online database of wikipedia, which is highly discouraged!!!

Please use this program only for educational purpose by reviewing the content (in form of text, images, graphics or any other form) copyright and its licence. Also, crawling pages in a sequential manner puts a lot of pressure on Wikipedia servers. Please follow the Wikipedia robot.txt guidelines to understand thee restrictions on number of requests per second that can be made by an external robot. According to wikipedia friendly, low speed bots are allowed to crawl!
