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

#url = 'https://www.peterhahn.nl/koopjes-dames-rokken'

#Fetching current DATE
now = datetime.datetime.now()
date = str(now.month) + "-" + str(now.day) + "-" + str(now.year)

#Open url csv file for reading urls
url_file = open('/Users/ishitaverma/Desktop/zalando/desigual/desigual.csv' , "r")
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
    old_productprice = "NA"
    type = "List Page"

    try:
        req_product = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        product_html = urllib.request.urlopen(req_product).read()
        product_htmlpage_soup = soup(product_html, "html.parser")
        html_body = product_htmlpage_soup.body

        if html_body.find("nav" , {"class" : "breadcrumb-navigation hidden-xs"}):
            nav = html_body.find("nav" , {"class" : "breadcrumb-navigation hidden-xs"})
            if nav.find("ol" , {"class" : "breadcrumb"}):
                lis = nav.find("ol" , {"class" : "breadcrumb"}).findAll("li")
                product_category= lis[len(lis)-1].text.replace("\n\n", " ").replace("\n\n", " ").replace("\n"," ").replace("\n", " ")
                
        product_divs = html_body.find("b2c-grid-products" , {"class" : "col"}).findAll("a" , {"class" : "product-info"})

    except AttributeError:
            continue
    except NameError:
        continue
    except ValueError:
        continue
    except urllib.error.HTTPError:
        continue
    except urllib.error.URLError:
        continue
    except http.client.IncompleteRead:
        continue


    for i in product_divs:

        try:
            if i.find("div" , {"class"  : "product-price-old"}):
                old_productprice = i.find("div" , {"class"  : "product-price-old"}).text

            if i.find("div" , {"class"  : "product-price reduced"}):
                product_price = i.find("div" , {"class"  : "product-price reduced"}).text

            if i.find("div" , {"class"  : "product-price"}):
                product_price = i.find("div" , {"class"  : "product-price"}).text

            if i.find("h3" , {"class" : "product-name"}):
                product_name = i.find("h3" , {"class" : "product-name"}).text

            if i.find("div" , {"class" : "product-sku"}):
                product_number = i.find("div" , {"class" : "product-sku"}).text.split(":")[1]

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


        try:
            f.write(url + "," + date + "," + type + "," + product_category + "," + product_name.strip('\n') + "," + product_price.replace(",",".") + "," + old_productprice.replace(",",".") + "," + str(position) + "," + product_number.strip('\n') + "," +  product_color.replace(",",".") + "," +
            product_description.replace(",", " ") + "," + no_of_reviews + "," +
            star_rating + "," + free_shipping_indicator + "," + str(main_picture) + "\n")
        except ValueError:
            continue

        #print (product_price)

        position = position + 1
        if position == 11:
            break

f.close()
