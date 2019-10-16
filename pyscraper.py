
#URL = "https://kickasstorrents.to/"
import requests 
from bs4 import BeautifulSoup 
from prettytable import PrettyTable
import json,time
import textwrap 
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import system
from requests.exceptions import HTTPError


# intialization 

chromedriver = "/usr/lib/chromium-browser/chromedriver"
x = PrettyTable()
x.field_names = ["ID", "Related Search"]

# ==================================================

def checkconnection():
    print("Checking Connection Please Wait!!!")
    for url in ['https://kickasstorrents.to/']:
        try:
            response = requests.get(url)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Connection Stablished!')
            filewrites("w+","") 
            initscraper()



def initsel(main_url):
    #####################configurations#############################
    option = Options()
    option.add_argument("--disable-infobars")
    # option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", { \
        "profile.default_content_setting_values.media_stream_mic": 1, 
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1, 
        "profile.default_content_setting_values.notifications": 1 
    })

    # Open main window with URL A
    browser= webdriver.Chrome(chrome_options=option, executable_path=chromedriver)
    browser.maximize_window()
    browser.get(main_url)
 
  
def checkurl(url):
    if "http" in url:
        pass
    else: 
        url="https://kickasstorrents.to"+str(url)
    return url

def scrapdownloadlink(url):
    if "http" in url:
        pass
    else: 
        url="https://kickasstorrents.to"+str(url)
    # print(url)
    req = requests.get(url) 
    soup_req = BeautifulSoup(req.content, 'html5lib') 
    widget = soup_req.find('div', attrs = {'class':'sharingWidget borderrad3px floatleft'})
    downloadlink=widget.a['href']
    return downloadlink 



def getgenre(argument): 
    switcher = { 
        "V":{'class':'markeredBlock torType filmType'}, 
        "v":{'class':'markeredBlock torType filmType'}, 
        "M": {'class':'markeredBlock torType musicType'}, 
        "m": {'class':'markeredBlock torType musicType'}, 
        "A": {'class':'markeredBlock torType exeType'},
        "a": {'class':'markeredBlock torType exeType'},
        "O": {'class':'markeredBlock torType Type'},
        "o": {'class':'markeredBlock torType Type'}
    } 

    return switcher.get(argument, "nothing") 
def deletefile():
    system("rm scrap.json")

def filewrites(mode,txt):
    f=open("scrap.json",mode)
    f.write(txt)
    f.close()
def fileread():
    f= open("scrap.json","r+")
    txt=f.read()
    f.close()
    return txt

def mainops(attribute,keyword):
    try:
        URL = "https://kickasstorrents.to/usearch/"+str(keyword)
        r = requests.get(URL) 
        soup = BeautifulSoup(r.content, 'html5lib') 
        # print(soup.prettify()) 
        table = soup.find('table', attrs = {'class':'doublecelltable'}) 
        print("Loading Please Wait...")
        i=0
        maindic={}
        quote={}
        x.clear_rows()
        for row in table.findAll('div', attrs = attribute):
        
            wrapper = textwrap.TextWrapper(width=50) 
            shortened = textwrap.shorten(text=row.a.text, width=100) 
            shortened_wrapped = wrapper.fill(text=shortened) 
            emptyrow=[]
            xrow=[]
            i+=1
            xrow.append(i)
            emptyrow.append("-"*5)
            xrow.append(shortened_wrapped)
            emptyrow.append("-"*100)
            
            quote[i] = {} 
            quote[i]["ID"] = i
        
            quote[i]["Name"] =  row.a.text
            Urlinks=checkurl(row.a['href'])
            quote[i]["URL"] = Urlinks
            
            maindic=json.dumps(quote)
            
            x.add_row(xrow)
            x.add_row(emptyrow)

        filewrites("w+",str(maindic))
        if len(maindic)>0:
            print(x)
            readops()
        else:
            print("Search Not Found....")
            time.sleep(1)
            banner()
            initscraper()
    except Exception as err:
            print(f'Other error occurred: {err}') 

def readops():
    txt=fileread()
    # print(x)
    linkdic = json.loads(txt)
    # print(txt[1])
    z=PrettyTable()
    z.field_names=['View Page','Magnet Link','Quit','Search Again']
    z.add_row(['V Or v','D or d',"Q or q","S or s"])
    print(z)
    selection = input("Enter your command: ")
    if selection=="V" or selection=="v":
        ID = input("Enter the Result ID : ")
        # print(linkdic[ID]['URL'])
        initsel(linkdic[ID]['URL'])
        banner()
        readops()
    elif selection=="D" or selection=="d":
        ID = input("Enter the Result ID : ")
        downloadlink=scrapdownloadlink(linkdic[ID]['URL'] )
        # print(downloadlink)
        webbrowser.open(downloadlink)
        banner()
        readops()
    elif selection=="Q" or selection=="q":
        quit()
    elif selection=="S" or selection=="s":
        deletefile()
        banner()
        initscraper()

    else:
        readops()
def initscraper():
    # Taking Input from user
    keyword = input("Enter your Search Keyword : ") 
    banner()
    y=PrettyTable()
    y.field_names=['Movies,TV Series, Anime','Music','Games & APPs','Others']
    y.add_row(['V Or v','M or m',"A or a","O or o"])
    print(y)
    genre=input("Enter the Genre : ") 
    banner()
    # =============================================

    # checking attribute and keyword
    attribute=getgenre(genre)
    if attribute=="nothing":
        print("Genre mismatched Please try Again")
        quit()

    keyword=keyword.replace(" ", "%20")
    mainops(attribute,keyword)
    # ===============================================

def banner():
    system('clear') 
    print("########::'##:::'##::'######:::'######::'########:::::'###::::'########::'########:'########::")
    print("##.... ##:. ##:'##::'##... ##:'##... ##: ##.... ##:::'## ##::: ##.... ##: ##.....:: ##.... ##:")
    print("##:::: ##::. ####::: ##:::..:: ##:::..:: ##:::: ##::'##:. ##:: ##:::: ##: ##::::::: ##:::: ##:")
    print("########::::. ##::::. ######:: ##::::::: ########::'##:::. ##: ########:: ######::: ########::")
    print("##.....:::::: ##:::::..... ##: ##::::::: ##.. ##::: #########: ##.....::: ##...:::: ##.. ##:::")
    print("##::::::::::: ##::::'##::: ##: ##::: ##: ##::. ##:: ##.... ##: ##:::::::: ##::::::: ##::. ##::")
    print("##::::::::::: ##::::. ######::. ######:: ##:::. ##: ##:::: ##: ##:::::::: ########: ##:::. ##:")
    print("..::::::::::::..::::::......::::......:::..:::::..::..:::::..::..:::::::::........::..:::::..::")
    print("================================Created By D-eviloper==========================================")
    print("=================Search Movies,TV series,Music, Anime,Games,Applications Etc======================")
    print("\n")


banner()
checkconnection()




