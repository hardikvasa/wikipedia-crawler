#Wikipedia Crawler v3 (inserting results into MySQL)

#Import Libraries
import time     #For Delay
import urllib.request    #Extracting web pages
import re


#Defining pages
starting_page = "https://en.wikipedia.org/wiki/Spacetime"
seed_page = "https://en.wikipedia.org"  #Crawling the English Wikipedia


#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        respData = str(resp.read())
        return respData
    except Exception as e:
        print(str(e))


#Extract the title tag
def extract_title(page):
    start_title = page.find("<span dir")
    end_start_title = page.find(">",start_title+1)
    stop_title = page.find("</span>", end_start_title + 1)
    title = page[end_start_title + 1 : stop_title]
    return title



#####################################################################
#Extract the see also section elements
def extract_see_also(page):
    if 'id="See_also">' in page:
        start_see_also = page.find('id="See_also">')
        start_list_items = page.find('<li>', start_see_also + 1)
        end_see_also = page.find('<h2>', start_list_items + 1)
        see_also_section = page[start_list_items: end_see_also]
        pure_item_raw = (re.sub(r'<.+?>', '', see_also_section)).replace('\n', ',')
        pure_item_raw2 = pure_item_raw.replace(',,', ',')
        pure_item = pure_item_raw2.replace(',,', ',')
        flag = 0
    else:
        pure_item = "No Related Links"
        flag = 1
    return pure_item, flag


#Extract just the Introduction part of the page
def extract_introduction(page):
    start_introduction = page.find("<p>")
    stop_introduction = page.find('<div id="toctitle">', start_introduction + 1)
    
    #If the page onl has introduction
    if '<div id="toctitle">' not in page:
        stop_introduction = page.find('</p>', start_introduction + 1)
    else:
        pass
    
    
    raw_introduction = page[start_introduction : stop_introduction]
    return raw_introduction



#Extract all the links
#Finding 'Next Link' on a given web page
def get_next_link(s):
    start_link = s.find("<a href")
    if start_link == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_quote = s.find('"', start_link)
        end_quote = s.find('"',start_quote+1)
        link = str(s[start_quote+1:end_quote])
        return link, end_quote
          

#Getting all links with the help of 'get_next_links'
def get_all_links(page):
    links = []
    while True:
        link, end_link = get_next_link(page)
        if link == "no_links":
            break
        else:
            links.append(link)      #Append all the links in the list named 'Links'
            #time.sleep(0.1)
            page = page[end_link:]
    return links 



#Remove all the HTML tags from the introduction to get the pure text
#Eliminate all the text inside '<' & '>'
def extract_pure_introduction(page):
    pure_introduction = (re.sub(r'<.+?>', '', page))       #From '<' to the next '>'
    return pure_introduction



#Crawl Initiation
#Check for file type in URL so crawler does not crawl images and text files
def extension_scan(url):
    a = ['.png','.jpg','.jpeg','.gif','.tif','.txt']
    j = 0
    while j < (len(a)):
        if a[j] in url:
            #print("There!")
            flag2 = 1
            break
        else:
            #print("Not There!")
            flag2 = 0
            j = j+1
    #print(flag2)
    return flag2


#URL parsing for incomplete or duplicate URLs
def url_parse(url):
    try:
        from urllib.parse import urlparse
    except ImportError:
        from urlparse import urlparse
    url = url  #.lower()    #Make it lower case
    s = urlparse(url)       #parse the given url
    seed_page_n = seed_page #.lower()       #Make it lower case
    #t = urlparse(seed_page_n)     #parse the seed page (reference page)
    i = 0
    flag = 0
    while i<=9:
        if url == "/":
            url = seed_page_n
            flag = 0  
        elif not s.scheme:
            url = "http://" + url
            flag = 0
        elif "#" in url:
            url = url[:url.find("#")]
            flag = 0
        elif "?" in url:
            url = url[:url.find("?")]
            flag = 0
        elif s.netloc == "":
            url = seed_page + s.path
            flag = 0
        #elif "www" not in url:
        #    url = "www."[:7] + url[7:]
        #    flag = 0
            
        elif url[len(url)-1] == "/":
            url = url[:-1]
            flag = 0
        #elif s.netloc != t.netloc:
        #    url = url
        #    flag = 1
        #    break        
        else:
            url = url
            flag = 0
            break
        
        i = i+1
        s = urlparse(url)   #Parse after every loop to update the values of url parameters
    return(url, flag)


     
t0 = time.time()
database = {}   #Create a dictionary




#Main Crawl function that calls all the above function and crawls the entire site sequentially
def web_crawl():  
    to_crawl = [starting_page]      #Define list name 'Seed Page'
    #print(to_crawl)
    crawled=[]      #Define list name 'Seed Page'
    #database = {}   #Create a dictionary
    #k = 0;
    for k in range(0, 3):
        i=0        #Initiate Variable to count No. of Iterations
        while i<3:     #Continue Looping till the 'to_crawl' list is not empty
            urll = to_crawl.pop(0)      #If there are elements in to_crawl then pop out the first element
            urll,flag = url_parse(urll)
            #print(urll)
            flag2 = extension_scan(urll)
            time.sleep(3)
            
            #If flag = 1, then the URL is outside the seed domain URL
            if flag == 1 or flag2 == 1:
                pass        #Do Nothing
                
            else:       
                if urll in crawled:     #Else check if the URL is already crawled
                    pass        #Do Nothing
                else:       #If the URL is not already crawled, then crawl i and extract all the links from it
                    print("Link = " + urll)
                    
                    raw_html = download_page(urll)
                    #print(raw_html)
                    
                    title_upper = str(extract_title(raw_html))
                    title = title_upper.lower()     #Lower title to match user queries
                    print("Title = " + title)
                    
                    
                    see_also,flag2 = extract_see_also(raw_html)
                    print("Related Links = " + see_also)
                    
                    
                    raw_introduction = extract_introduction(raw_html)
                    #print("Raw Introduction = " + raw_introduction)
                    
                    to_crawl = to_crawl + get_all_links(raw_introduction)
                    crawled.append(urll)
                    
                    pure_introduction = extract_pure_introduction(raw_introduction)
                    print("Introduction = " + pure_introduction.replace('   ',' '))
                    
                    database [title] = pure_introduction        #Add title and its introduction to the dict
                    
                    #file = open('database.txt', 'a')        #Open the text file called database.txt
                    #file.write(title + ": " + "\n")         #Write the title of the page
                    #file.write(pure_introduction + "\n\n")      #write the introduction of that page
                    #file.close()                            #Close the file
                    
                    
                    #db = MySQLdb.connect(
                    #host = 'localhost',
                    #user = 'vir12870_hnvasa',
                    #passwd = 'standrose@123',
                    #db = 'vir12870_cleoria'
                    #)
                    #cursor = db.cursor()
                    
                    #cursor.execute ("""INSERT IGNORE INTO `database` (title, introduction) VALUES (%s, %s)""", (title, pure_introduction))
                    
                    #db.commit()
                    #db.close()
    
                    #Remove duplicated from to_crawl
                    n = 1
                    j = 0
                    #k = 0
                    while j < (len(to_crawl)-n):
                        if to_crawl[j] in to_crawl[j+1:(len(to_crawl)-1)]:
                            to_crawl.pop(j)
                            n = n+1
                        else:
                            pass     #Do Nothing
                        j = j+1
                i=i+1
                print(i)
                print(k)
                #print(to_crawl)
                #print("Iteration No. = " + str(i))
                #print("To Crawl = " + str(len(to_crawl)))
                #print("Crawled = " + str(len(crawled)))
    return ""

print (web_crawl())

t1 = time.time()
total_time = t1-t0
print(total_time)
