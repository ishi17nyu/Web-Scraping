import urllib.request
from bs4 import BeautifulSoup as soup
import datetime
import re



#Get the start and end  and file name from User
filename = input("Enter File Name \n")
start = input("Enter Start Url \n")
end = input("Enter End Url \n")

#Saving data in csv file
f = open(filename , "w")
headers = "URL, DATE Scraped, Type, Product Category, Product Name , Current Price , Old Price, Position, Product Number, Product Color, Product Description, Number of Reviews, Star Rating, Free Shipping Indicator, Number of Photos \n"
if int(start) == 1:
    f.write(headers)

#Fetching current DATE
now = datetime.datetime.now()
date = str(now.month) + "-" + str(now.day) + "-" + str(now.year)

#Open url csv file for reading urls
url_file = open('/Users/ishitaverma/Desktop/zalando/zalando/zalando_url.csv' , "r")

count = 0

for line in url_file:
    #url from file to get the data
    url = line.strip('\n')
    url_tosave = url

    count = count + 1

    #print (count)
    #print (url)

    if url.startswith('"'):
        url = url[1:len(url)]

    if count in range (1,int(start)) and int(start) != 1:
        continue
    if count == int(end):
        break

    try:
        product_page = urllib.request.urlopen(url)
        product_htmlpage_soup = soup(product_page, "html.parser")
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
    position = 1
    main_picture = 1
    old_productprice = "NA"
    type = "Product Page"

    try:
        title_div = product_body.find("div", {"id" : "z-pdp"})

        product_name_div = title_div.find("div", {"id":"z-pdp-topSection"})
        product_name = product_name_div.h1.text

        product_color_span = title_div.find("span" , {"class" : "h-text h-color-black detail title-4"})
        product_color = product_color_span.text

        product_price_div = product_body.find("div" , {"class" : "h-product-price topSection"})
        product_price = product_price_div.h4.text.replace("inclusief btw", " ")
        if product_price.startswith('Vanaf ') :
            product_price = product_price.replace("Vanaf ", " ")
        if product_price_div.findAll('span'):
            span_tag = product_price_div.findAll('span')
            if len(span_tag) > 1 :
                old_productprice = span_tag[2].text
            if old_productprice.startswith('Vanaf ') :
                old_productprice = old_productprice.replace("Vanaf ", " ")


        p_tag = product_body.find(string = re.compile("Artikelnummer")).parent.parent
        span_tags = p_tag.findAll("span")
        product_number = span_tags[1].text

        free_shiping = product_body.find(string = re.compile("Gratis verzending"))
        if free_shiping:
            free_shipping_indicator = "AVAILABLE"


        pictures_div = product_body.find("div" , {"id" : "topsection-thumbnail-scroller"})
        total_pictures_div = pictures_div.findAll("div" , {"class" : "h-container h-scroller-item h-align-left"})
        number_of_pictures =  len(total_pictures_div) + main_picture


        print(url, date, type, product_category, product_name, product_price,old_productprice, position , product_number , product_color, product_description, no_of_reviews, star_rating, free_shipping_indicator, number_of_pictures)
        try:
            f.write(url + "," + date + "," + type + "," + product_category + "," + product_name + "," + product_price.replace(",",".") + "," + old_productprice.replace(",",".") + "," + str(position) + "," + product_number + "," + product_color + "," +
            product_description.replace(",", " ") + "," + no_of_reviews + "," +
            star_rating + "," + free_shipping_indicator + "," + str(number_of_pictures) + "\n")
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
