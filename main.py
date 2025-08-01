from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import time
import pandas as pd
from fake_useragent import UserAgent
import random

# to get proxies from website
try:
    df = pd.read_html("https://free-proxy-list.net/en/")
    ips = df[0]["IP Address"].tolist()
    proxies = ips[1:50]
except Exception as e:
    print("Error fetching proxy list:", e)
    proxies = []

try:
    ua = UserAgent()
    user_agents = ua.random
except:
    user_agents = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."

# search product
search= input("Enter the product name for search ")
search_url=f"https://www.daraz.pk/catalog/?spm=a2a0e.tm80335142.search.d_go&q={search}"
page_count = 0
next_page = 2

# creating lists
mall_product=[]
name_of_product=[]
price_of_product=[]
best_price_product=[]
soldout_product=[]
location_of_product=[]
rating_of_product=[]

# for using random proxies
proxy = random.choice(proxies)
user_agent = random.choice(user_agents)
firefox_options = Options()
firefox_options.add_argument(f'--proxy-server=http://{proxy}')
# firefox_options.set_preference("general.useragent.override", user_agent)
# firefox_options.add_argument("--headless")  # optional
service = Service()
driver = webdriver.Firefox(service=service, options=firefox_options)

# def routate_proxies(proxies):


while search_url:
    try:
        driver.get(search_url)
        time.sleep(random.uniform(4, 6)) 
        html = driver.page_source
        if "captcha" in html.lower():
            print("Captcha detected, changing proxy")
            # if proxiy fails try this
            MAX_RETRIES = 50
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    print(f"[INFO] Trying Page {next_page - 1} with Proxy {proxy}")
                    driver.set_page_load_timeout(20)  # optional: limits hanging
                    driver.get(search_url)
                    time.sleep(random.uniform(4, 6))
                    break  # If successful, exit retry loop
                except (TimeoutException, WebDriverException) as e:
                    print(f"[ERROR] Proxy failed: {proxy}, retrying with new one...")
                    retries += 1
                    try:
                        driver.quit()
                    except:
                        pass  # If already closed
                    
                    proxy = random.choice(proxies)
                    user_agent = random.choice(user_agents)
                    firefox_options = Options()
                    firefox_options.add_argument(f'--proxy-server=http://{proxy}')
                    service = Service()
                    driver = webdriver.Firefox(service=service, options=firefox_options)
            else:
                print(f"[FATAL] All {MAX_RETRIES} retries failed. Skipping this page.")
                pass
        soup = BeautifulSoup(html, 'html.parser')
        container = soup.find('div', class_='_17mcb')

        products= container.find_all('div', class_="Bm3ON")
        for index ,product in enumerate(products):

            product_from_mall= product.find('i', class_="ic-dynamic-badge-116115")
            if product_from_mall:
                data = "This product is from Daraz MALL"
                print(data)
                mall_product.append(data)

            else:
                data = "None"
                print(data)
                mall_product.append(data)

            product_name= product.find('div', class_="RfADt")
            if product_name:
                data=product_name.text
                print("Product Name : " , data,index)
                name_of_product.append(data)
            else:
                data = "None"
                print(data)
                name_of_product.append(data)

            product_price= product.find('div', class_="aBrP0")
            if product_price:
                data=product_price.text
                print("Product price : " , data)
                price_of_product.append(data)
            else:
                data = "None"
                print(data)
                price_of_product.append(data)

            product_best_price= product.find('div', class_="WNoq3")
            if product_best_price:
                data = "This product is from Daraz MALL"
                print(data)
                best_price_product.append(data)

            else:
                data = "None"
                print(data)
                best_price_product.append(data)

            product_soldout= product.find('span', class_="_1cEkb")
            if product_soldout:
                data=product_soldout.text
                print("Product soldout : " , data)
                soldout_product.append(data)
            else:
                data = "None"
                print(data)
                soldout_product.append(data)

            product_location= product.find('span', class_="oa6ri")
            if product_location:
                data=product_location.text
                print("Product location : " , data)
                location_of_product.append(data)
            else:
                data = "None"
                print(data)
                location_of_product.append(data)

            product_rating= product.find('span', class_="qzqFw")
            if product_rating:
                data=product_rating.text
                print("People how rate this product are :" , data)
                rating_of_product.append(data)
            else:
                data = "None"
                print(data)
                rating_of_product.append(data)

        # storing data in csv after each page
        my_dic={"Product":mall_product,"Name of product":name_of_product,"Price of product":price_of_product,"best price product":best_price_product,"Soldout product":soldout_product,"Location of product":location_of_product,"Rating of product":rating_of_product}
        df = pd.DataFrame(my_dic)
        df.to_csv("data.csv", mode='a', index=False , header=False) 
                
        button = soup.find("div", class_="e5J1n")
        if button:
            search_url = f"https://www.daraz.pk/catalog/?q={search}&spm=a2a0e.tm80335142.search.d_go&page={next_page}"
            next_page += 1
            page_count += 1
        else:
            search_url=None
        
        if page_count % 25 == 0 and page_count != 0:
            driver.quit()
            print(f"[INFO] Switching Proxy after {page_count} pages")
            proxy = random.choice(proxies)
            user_agent = random.choice(user_agents)
            firefox_options = Options()
            firefox_options.add_argument(f'--proxy-server=http://{proxy}')
            service = Service()
            driver = webdriver.Firefox(service=service, options=firefox_options)
        
        # print(len(mall_product))
        # print(len(name_of_product))
        # print(len(price_of_product))
        # print(len(best_price_product))
        # print(len(soldout_product))
        # print(len(location_of_product))
        # print(len(rating_of_product))

    except Exception as e:
        print("Exception occurred:", e)

driver.quit()
    
my_dic={"Product":mall_product,"Name of product":name_of_product,"Price of product":price_of_product,"best price product":best_price_product,"Soldout product":soldout_product,"Location of product":location_of_product,"Rating of product":rating_of_product}
df = pd.DataFrame(my_dic)
df.to_csv("data.csv", index=False)  
