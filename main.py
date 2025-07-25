from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
from fake_useragent import UserAgent
import random
search= input("Enter the product name for search ")
search_url=f"https://www.daraz.pk/catalog/?spm=a2a0e.tm80335142.search.d_go&q={search}"
next_page = 2

ua = UserAgent()
# user_agent = ua.random
try:
    user_agent = ua.random
except:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."

# Setup Firefox options with fake user-agent
firefox_options = Options()
firefox_options.set_preference("general.useragent.override", user_agent)
# firefox_options.add_argument("--headless")  # optional: remove if you want to see browser

# Initialize WebDriver
service = Service()
driver = webdriver.Firefox(service=service, options=firefox_options)
# firefox_options = Options()
# service = Service()  # You can also do Service("path/to/chromedriver")
# driver = webdriver.Firefox(service=service, options=firefox_options)

mall_product=[]
name_of_product=[]
price_of_product=[]
best_price_product=[]
soldout_product=[]
location_of_product=[]
rating_of_product=[]


while search_url:
    try:
        
        driver.get(search_url)
        time.sleep(random.uniform(4, 6)) 

        html = driver.page_source
        if "captcha" in html.lower():
            print("Captcha detected, stopping")
            break

        #driver.quit()

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
                product_name.append(data)

            product_price= product.find('div', class_="aBrP0")
            if product_price:
                data=product_price.text
                print("Product price : " , data)
                price_of_product.append(data)
            else:
                data = "None"
                print(data)
                product_price.append(data)

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
                product_location.append(data)

            product_rating= product.find('span', class_="qzqFw")
            if product_rating:
                data=product_rating.text
                print("People how rate this product are :" , data)
                rating_of_product.append(data)
            else:
                data = "None"
                print(data)
                rating_of_product.append(data)
                
        button = soup.find("div", class_="e5J1n")
        if button:
            search_url=f"https://www.daraz.pk/catalog/?q=phone&spm=a2a0e.tm80335142.search.d_go&page={next_page}"
            next_page += 1
        else:
            search_url=None
            driver.quit()
            break
        
        # print(len(mall_product))
        # print(len(name_of_product))
        # print(len(price_of_product))
        # print(len(best_price_product))
        # print(len(soldout_product))
        # print(len(location_of_product))
        # print(len(rating_of_product))

    except:
        break
    
my_dic={"Product":mall_product,"Name of product":name_of_product,"Price of product":price_of_product,"best price product":best_price_product,"Soldout product":soldout_product,"Location of product":location_of_product,"Rating of product":rating_of_product}
df = pd.DataFrame(my_dic)
df.to_csv("data.csv", index=False)  
