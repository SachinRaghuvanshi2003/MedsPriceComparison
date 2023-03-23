from bs4 import BeautifulSoup
from flask import Flask,render_template,redirect,request
import jinja2
names=[]
import requests
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
def tata1mg(name):
    try:
        global tata1mg
        name1 = name.replace(" ","+")

        tata1mg=f'https://www.1mg.com/search/all?name="{name1}"'
        res = requests.get(f'https://www.1mg.com/search/all?name="{name1}"',headers=headers)


        soup = BeautifulSoup(res.text,'html.parser')
        
        if(soup.select('div[class*="style__product-description__"]')):
                tata1mg_name = soup.select('div[class*="style__product-description__"]')[0].getText().strip().upper()
                if name1.upper() in tata1mg_name.upper():
                        tata1mg_price = soup.select('div[class*="style__price-tag__"]')[0].getText().strip()
                        tata1mg_name = soup.select('div[class*="style__product-description__"]')[0].getText().strip()
      
                else:
                        tata1mg_price='0'
            
        names.append(tata1mg_name)
            
        return tata1mg_price 
    except:
        tata1mg_price= '0'
    return tata1mg_price

def amazon(name):
    try:
        global amazon
        name1 = name.replace(" ","-")
        name2 = name.replace(" ","+")
        amazon=f'https://www.amazon.in/{name1}/s?k={name2}'
        res = requests.get(f'https://www.amazon.in/{name1}/s?k={name2}',headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        amazon_page_length = int(len(amazon_page))
        for i in range(0,amazon_page_length):
            name = name.upper()
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
            if name in amazon_name:
                amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip()
                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
                break
            else:
                i+=1
                i=int(i)
                if i==amazon_page_length:
                    amazon_price = '0'
                    break
        names.append(amazon_name)
                    
        return amazon_price
     
    except:
        amazon_price = '0'
    return amazon_price

def convert(a):
    b=a.replace(" ",'')
    c=b.replace("INR",'')
    d=c.replace(",",'')
    f=d.replace("₹",'')
    g=int(float(f))
    return g

app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def search():
        if(request.method=='GET'): 
              return render_template('search.html')
        else:
            statement=""
            statement1=""
            name=request.form.get('meds')
            tata1mg_price=tata1mg(name)
            amazon_price=amazon(name)
            if tata1mg_price=='0':
                    statement="tata1mg: No product found!"
                    tata1mg_price = int(tata1mg_price)
            else:
                    statement="tata1mg Price:"
                    tata1mg_price=convert(tata1mg_price)
            if amazon_price=='0':
                     statement1="Amazon: No product found!"
                     amazon_price = int(amazon_price)
            else:
                    statement1="Amazon price:"
                    amazon_price=convert(amazon_price)
            lst = [tata1mg_price,amazon_price]
#print(lst)
            lst2=[]
            for j in range(0,len(lst)):
                    if lst[j]>0:
                        lst2.append(lst[j])
            if len(lst2)==0:
                      final_statment="No relative product find in all websites...."
            else:
                       final_statment=min(lst2)
            price = {
                'amazon':f'{amazon}',
                'tata1mg':f'{tata1mg}',
            }
            if(min(lst2)==tata1mg_price):
                  minid=price['tata1mg']
            else:
                  minid=price['amazon']
                 
            return render_template('main.html',statement=statement,tata1mgprice=tata1mg_price,statement1=statement1,amazonprice=amazon_price,finalstatement=final_statment,tataid=price['tata1mg'],amazonid=price['amazon'],minid=minid,tataname=names[0],amazonname=names[1])
