from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep

import sqlite3

def scrapper(driver_,URL,thread_name):

    connection = sqlite3.connect('scrappy.db')
    c = connection.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS House (
            AdvertTitle text,
            PropertyAddress text,
            PropertyPrice text,
            AdvertAgent text,
            AdvertAgentAddress text,
            NearestStation text,
            ListingHistory text,
            PhoneNumber text,
            Href text
            )''')

    connection.commit()
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('-window-size=320,920')
    browser = webdriver.Chrome(driver_,options=options)
    browser.get(URL)

    try:
        browser.find_element_by_xpath("//div[@class='errorbox']")
        print("None!")

        browser.close()
        connection.close()
        return None
    except:
        pass

    select = Select(browser.find_element_by_xpath("//select[@id='maxDaysSinceAdded']"))
    select = select.select_by_value('1')
    submit_query = browser.find_element_by_xpath("//*[@id='submit' and 1]")
    submit_query.click()
    
    if browser.find_element_by_xpath("""//*[@id="searchFilters"]/div[2]/div[2]/div/div[1]/span[1]""").get_attribute("innerHTML") == '0':
        print("None")
        browser.close()
        connection.close()
        return None

    counter = 1
    n_pages = browser.find_element_by_xpath("/html//div[@id='l-container']//div[@class='l-propertySearch-paginationAndSearchFooter']//div[@class='pagination-pageSelect']/span[3]").text
    n_pages = n_pages.replace(",","")

    for page in range(int(n_pages)):

        cards = browser.find_elements_by_xpath("//a[@class='propertyCard-priceLink propertyCard-salePrice']")
        try:
            browser.find_element_by_xpath("//div[@class='propertyCard-moreInfoFeaturedTitle']")
            cards = cards[1:len(cards)]
        except:
            pass
        
        for i in cards:
            # if counter < 25:
            #     counter += 1
            #     continue

            href = i.get_attribute('href')
            browser.execute_script(f'window.open("{href}","_blank");')
            browser.switch_to.window(browser.window_handles[1])

            print(f'>> {thread_name} - {counter} #WORKING {href}')

            advert_title        = browser.find_element_by_xpath("//h1[@class='fs-22']").text
            property_address    = browser.find_element_by_xpath("//address[@class='pad-0 fs-16 grid-25']").text
            property_price      = browser.find_element_by_css_selector('.primary-content .cell #propertyHeaderPrice strong').get_attribute('innerHTML').strip()
            advert_address      = browser.find_element_by_css_selector('.secondary-content .cell .agent-details-display address').get_attribute('innerHTML')
            phone_number        = browser.find_element_by_css_selector('.secondary-content .cell .request-property-details a strong').get_attribute('innerHTML')

            try:
                nearest_station     = '{} {}'.format(
                                        browser.find_element_by_xpath("//div[@class='bdr-2 box-1 pad-8']/ul[@class='stations-list' and 1]/li[1]/span").get_attribute('innerHTML'),
                                        browser.find_element_by_xpath("//div[@class='bdr-2 box-1 pad-8']/ul[@class='stations-list' and 1]/li[1]/small[1]").get_attribute('innerHTML'))
            except:
                nearest_station     = "Not Found!"
            
            try:    advert_agent    =  browser.find_element_by_xpath("//p[@class='pad-0']/strong[1]").text 
            except: advert_agent    =  browser.find_element_by_xpath("//*[@id='aboutBranchLink']/strong[1]").text 
            try:    listing_history = browser.find_element_by_xpath("//div[@id='firstListedDateValue']").get_attribute('innerHTML')
            except: listing_history = "Not Found!"
           
            advert_title   = advert_title.replace("for sale","")
            property_price = property_price[0:(len(property_price)-4)]
            advert_address = " ".join(advert_address.split())
        
            c.execute("INSERT INTO House VALUES (?,?,?,?,?,?,?,?,?)",
                    (advert_title,property_address,property_price,
                    advert_agent,advert_address,nearest_station,
                    listing_history,phone_number,href))
            connection.commit()

            print(f'>> {thread_name} - {counter} #ADD {href}')
            counter += 1
            
            browser.close()
            browser.switch_to.window(browser.window_handles[0])

        try:
            button = browser.find_element_by_xpath("//button[@class='pagination-button pagination-direction pagination-direction--next']")
            button.click()
            sleep(.5)
        except:
            pass

    browser.close()
    connection.close()

if __name__ == "__main__":
    scrapper('C:/chromedriver.exe','')