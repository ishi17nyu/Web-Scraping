import urllib.request
from bs4 import BeautifulSoup as soup
import datetime
import re

#Saving data in csv file
filename = input("Enter File Name \n")
f = open(filename , "w")
headers = "URL, DATE Scraped, Type, Product Category, Product Name , Current Price , Old Price, Position, Product Number, Product Color, Product Description, Number of Reviews, Star Rating, Free Shipping Indicator, Number of Photos \n"
f.write(headers)

#Get the start and end from User
start = input("Enter Start Url \n")
end = input("Enter End Url \n")

#Fetching current DATE
now = datetime.datetime.now()
date = str(now.month) + "-" + str(now.day) + "-" + str(now.year)

#Open url csv file for reading urls
url_file = open('/Users/ishitaverma/Desktop/zalando/vanharen/vanharen_url.csv' , "r")
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

    try:
        product_category_div = product_body.find("div" , {"id" : "ariadne"})
        product_category_ul = product_category_div.find("ul")
        li = product_category_ul.findAll("li")
        if li[2]:
            product_category = li[2].find("a").text.replace('\n',"")
        elif li[1]:
            product_category = li[1].find("a").text.replace('\n',"")
        elif li[0]:
            product_category = li[0].find("a").text.replace('\n',"")
        else:
            product_category = 'NA'


        product_name_header = product_body.find("section" , {"class" : "details image-zoom-container"})
        product_name_section = product_name_header.find("section" , {"class" : "features"})
        product_name = product_name_section.find("h1").find("span").text.replace('\n',"")
        type = "Product Page"


        price_div = product_body.find("div" , {"class" : "priceWrapper"})
        if price_div.find("div" , {"class" : "price"}):
            price_span_div = price_div.find("div" , {"class" : "PRODUCT_GLOBAL_PRICE product-price"})
            price_span = price_span_div.find("span" , {"class" : "val"})
            product_price = price_span.text

        if price_div.find("div", {"class"  : "price reduced"}):
            price_span_div = price_div.find("div" , {"class" : "price reduced"})
            price_span = price_span_div.find("span" , {"class" : "val"})
            product_price = price_span.text

        if price_div.find("div", {"class"  : "old-price"}):
            price_span_div = price_div.find("div" , {"class" : "old-price"})
            price_span = price_span_div.find("span" , {"class" : "line-through"})
            old_productprice = price_span.text
        else:
            old_productprice = "NA"

        articlenumber_tag = product_body.find(string = re.compile("Artikelnummer:")).parent.parent
        product_number = articlenumber_tag.text.split(":")[1].replace('\n',"")

        color_tag = product_body.find(string = re.compile("Kleur:")).parent
        product_color = color_tag.text.split(":")[1].replace('\n',"")

        print(Url_tosave, date, type, product_category, product_name, product_price,old_productprice, position , product_number , product_color, product_description, no_of_reviews, star_rating, free_shipping_indicator, main_picture)
        try:
            f.write(Url_tosave + "," + date + "," + type + "," + product_category + "," + product_name + "," + product_price.replace(",",".") + "," + old_productprice.replace(",",".") + "," + str(position) + "," + product_number + "," + product_color + "," +
            product_description.replace(",", " ") + "," + no_of_reviews + "," +
            star_rating + "," + free_shipping_indicator + "," + str(main_picture) + "\n")
        except ValueError:
            continue
    except AttributeError:
        continue
    except IndexError:
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
