from bs4 import BeautifulSoup
from flask import Flask,render_template,redirect
import jinja2

import requests
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
def tata1mg(name):
    try:
        global tata1mg
        name1 = name.replace(" ","+")

        tata1mg=f'https://www.1mg.com/search/all?name="{name1}"'
        res = requests.get(f'https://www.1mg.com/search/all?name="{name1}"',headers=headers)


        print("\nSearching in 1mg....")
        soup = BeautifulSoup(res.text,'html.parser')
        
        if(soup.select('div[class*="style__product-description__"]')):
                tata1mg_name = soup.select('div[class*="style__product-description__"]')[0].getText().strip().upper()
                if name1.upper() in tata1mg_name.upper():
                        tata1mg_price = soup.select('div[class*="style__price-tag__"]')[0].getText().strip()
                        tata1mg_name = soup.select('div[class*="style__product-description__"]')[0].getText().strip()
                        print("tata1mg:")
                        print(tata1mg_name)
                        print(tata1mg_price)
                        print("---------------------------------")
                
      
                else:
                        tata1mg_price='0'
            
            
            
        return tata1mg_price 
    except:
        print("TATA 1mg: No product found!")  
        print("---------------------------------")
        tata1mg_price= '0'
    return tata1mg_price

def amazon(name):
    try:
        global amazon
        name1 = name.replace(" ","-")
        name2 = name.replace(" ","+")
        amazon=f'https://www.amazon.in/{name1}/s?k={name2}'
        res = requests.get(f'https://www.amazon.in/{name1}/s?k={name2}',headers=headers)
        print("\nSearching in amazon...")
        soup = BeautifulSoup(res.text,'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        amazon_page_length = int(len(amazon_page))
        for i in range(0,amazon_page_length):
            name = name.upper()
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
            if name in amazon_name:
                amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip()
                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
                print("Amazon:")
                print(amazon_name)
                print("₹"+amazon_price)
                print("---------------------------------")
                break
            else:
                i+=1
                i=int(i)
                if i==amazon_page_length:
                    amazon_price = '0'
                    print("amazon : No product found!")
                    print("-----------------------------")
                    break
                    
        return amazon_price
    except:
        print("Amazon: No product found!")
        print("---------------------------------")
        amazon_price = '0'
    return amazon_price

def convert(a):
    b=a.replace(" ",'')
    c=b.replace("INR",'')
    d=c.replace(",",'')
    f=d.replace("₹",'')
    g=int(float(f))
    return g

name=input("Product Name:\n")
tata1mg_price=tata1mg(name)
amazon_price=amazon(name)


if tata1mg_price=='0':
    print("tata1mg: No product found!")
    tata1mg_price = int(tata1mg_price)
else:
    print("\ntata1mg Price:",tata1mg_price)
    tata1mg_price=convert(tata1mg_price)
if amazon_price=='0':
    print("Amazon: No product found!")
    amazon_price = int(amazon_price)
else:
    print("\nAmazon price: ₹",amazon_price)
    amazon_price=convert(amazon_price)
lst = [tata1mg_price,amazon_price]
#print(lst)
lst2=[]
for j in range(0,len(lst)):
    if lst[j]>0:
        lst2.append(lst[j])
if len(lst2)==0:
    print("No relative product find in all websites....")
else:
    min_price=min(lst2)

    print("_______________________________")
    print("\nMinimun Price: ₹",min_price)
    price = {
        f'{amazon_price}':f'{amazon}',
        f'{tata1mg_price}':f'{tata1mg}',
    }
    for key, value in price.items():
        if int(key)==min_price:
            print ('\nURL:', price[key],'\n')
   
    print("---------------------------------------------------------URLs--------------------------------------------------------------")
    print("TATA 1mg : \n",tata1mg)
    print("\nAmazon : \n",amazon)
    print("---------------------------------------------------------------------------------------------------------------------------")