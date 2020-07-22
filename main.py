import threading, queue

from scrapper import scrapper


PATH_TO_DATABASE    = 'search_queries\cities.txt'
PATH_TO_DRIVER      = 'C://chromedriver.exe'
THREADS             = 4

f = open(PATH_TO_DATABASE ,"r") 
f = f.readlines()
threads = [i for i in range(THREADS)]
k = 0

for n,location in enumerate(f):

    URL = f'https://www.rightmove.co.uk/property-for-sale/search.html?searchLocation={location}&locationIdentifier=&useLocationIdentifier=false&buy=For+sale'
    print(URL)
    threads[k] = threading.Thread(group=None, target=scrapper,args=(PATH_TO_DRIVER,URL,f'T{k}'))
    threads[k].start()
    k += 1

    if k == THREADS or (len(f) - n) == 0:
        for i in threads:
            i.join()
        k = 0