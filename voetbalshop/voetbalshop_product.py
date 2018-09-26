import urllib.request
from bs4 import BeautifulSoup as soup
import datetime
import re


#Saving data in csv file
filename = input("Enter File Name \n")
start = input("Enter Start Url \n")
end = input("Enter End Url \n")

f = open(filename , "w")
headers = "URL, DATE Scraped, Type, Product Category, Product Name , Current Price , Old Price, Position, Product Number, Product Color, Product Description, Number of Reviews, Star Rating, Free Shipping Indicator, Number of Photos \n"
if int(start) == 1:
    f.write(headers)

#Fetching current DATE
now = datetime.datetime.now()
date = str(now.month) + "-" + str(now.day) + "-" + str(now.year)

#Open url csv file for reading urls
url_file = open('/Users/ishitaverma/Desktop/zalando/voetbalshop/voetbalshop.csv' , "r")
count = 0

for line in url_file:
    #url from file to get the data
    url = line.strip('\n')
    count = count + 1

    if url.startswith('"'):
         url = url[1:len(url)]

    print(url)
    print(count)

    if count in range (1,int(start)) and int(start) != 1:
        continue
    if count == int(end):
        break

    #Creating Variables
    product_category = "NA"
    product_name = "NA"
    product_price = "NA"
    product_code = "NA"
    product_color = "NA"
    product_number = "NA"
    product_description = "NA"
    no_of_reviews  = "NA"
    star_rating = "NA"
    free_shipping_indicator = "NA"
    main_picture = 1
    position = 1
    type = "Product Page"
    old_productprice = "NA"

    try:
        req_product = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        product_html = urllib.request.urlopen(req_product).read()
        product_htmlpage_soup = soup(product_html, "html.parser")
        product_body = product_htmlpage_soup.body

        # product_cat_li = product_body.find("ul" , {"typeof" : "BreadcrumbList"}).findAll("li")
        # product_category = product_cat_li[len(product_cat_li) - 1].find("span").text

    except ValueError:
        continue
    except NameError:
        continue
    except urllib.error.HTTPError:
        continue
    except urllib.error.URLError:
        continue
    except http.client.IncompleteRead:
        continue

    try:
        product_name  = product_body.find("h1" , {"itemprop" : "name"}).text

        product_number = product_body.find("span" , {"itemprop" : "mpn"}).text

        if product_body.find("p" , {"class" : "price"}):
            product_price = product_body.find("p" , {"class" : "price"}).text

        if product_body.find("p" , {"class" : "price old-price"}):
            old_productprice = product_body.find("p" , {"class" : "price old-price"}).text

        if product_body.find("p" , {"class" : "price special-price"}):
            product_price = product_body.find("p" , {"class" : "price special-price"}).text

        try:
            f.write(url + "," + date + "," + type + "," + product_category + "," + product_name.strip('\n') + "," + product_price.replace(",",".") + "," + old_productprice.replace(",",".") + "," + str(position) + "," + product_number.strip('\n') + "," +  product_color.replace(",",".") + "," +
            product_description.replace(",", " ") + "," + no_of_reviews + "," +
            star_rating + "," + free_shipping_indicator + "," + str(main_picture) + "\n")
        except ValueError:
            continue




    except AttributeError:
            continue
    except ValueError:
        continue
    except urllib.error.HTTPError:
        continue
    except socket.gaierror:
        continue
    except urllib.error.URLError:
        continue
    except NameError:
        continue
    except http.client.IncompleteRead:
        continue

f.close()
