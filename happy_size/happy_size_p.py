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
url_file = open('/Users/ishitaverma/Desktop/zalando/happy_size/happy_size.csv' , "r")
count = 0

for line in url_file:
    #url from file to get the data
    url = line.strip('\n')
    Url_tosave = url

    count = count + 1
    print(url)
    if url.startswith('"'):
        url = url[1:len(url)]

    if count in range (1,int(start)) and start != 1:
        continue
    if count == int(end):
        break

    try:
        req_product = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        product_html = urllib.request.urlopen(req_product).read()

        product_htmlpage_soup = soup(product_html, "html.parser")
        product_body = product_htmlpage_soup.body

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
    old_productprice = "NA"
    position = 1
    type = "Product Page"


    try:
        product_category_div = product_body.find("div" , {"class" : "breadcrumbsContent"})
        product_category = product_category_div.find("span" , {"class" : "breadcrumbsEntry last"}).text

        product_div = product_body.find("div" , {"class" : "productDescriptionTitle"})
        product_name = product_div.h1.text


        if product_body.find("div" , {"class" : "price"}):
            if product_body.find("div" , {"class" : "price"}).find("span" , {"class" : "price"}):
                product_price = product_body.find("div" , {"class" : "price"}).find("span" , {"class" : "price"}).find("meta")['content']

            if product_body.find("div" , {"class" : "price"}).find("span" , {"class" : "price reduced"}):
                product_price = product_body.find("div" , {"class" : "price"}).find("span" , {"class" : "price reduced"}).find("meta")['content']

            if product_body.find("div" , {"class" : "price"}).find("span" , {"class" : "price crossedOut"}):
                old_productprice_van = product_body.find("div" , {"class" : "price"}).find("span" , {"class" : "price crossedOut"}).text.replace("van" , " ")
                old_productprice = old_productprice_van.replace("\r\n\t\t\t\t\t\t" , " ").replace("\r\n\t\t\t\t\t\t", " ").replace("\n" , " ")

        if product_body.find("span" , {"class" : "orderNumber"}):
            product_number = product_body.find("span" , {"class" : "orderNumber"}).text.replace("\r\n\t\t\t" , " ")

        if product_body.find("div" , {"class" : "selectedColor"}):
            product_color = product_body.find("div" , {"class" : "selectedColor"}).find("span" , {"class" : "selectedAttribute"}).text.replace("\r\n\t\t\t\t\t\n" , " ")

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
