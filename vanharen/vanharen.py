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
url_file = open('/Users/ishitaverma/Desktop/zalando/vanharen/vanharen_url.csv' , "r")
count = 0

for line in url_file:
    #url from file to get the data
    url = line.strip('\n')
    Url_tosave = url
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

    try:
        #opening up the connection
        uClient = urllib.request.urlopen(url)

        #grabbing the page
        page_html = uClient.read()

        #Closing the connection
        uClient.close()

        #html parsing of above grabbed using BeautifulSoup
        htmlpage_soup = soup(page_html, "html.parser")

        # Get the product category
        product_category = htmlpage_soup.head.title.text


        #Grab each product
        html_body = htmlpage_soup.body

        product_container_div = html_body.find("div", {"id" : "product-list"})
        product_list = product_container_div.findAll("div" , {"class" : "product-row"})

        length = len (product_list)

        if length > 1:
            type = "List Page"
        else:
            type = "Product Page"

        #Product category
        product_category_main_div = html_body.find("div" , {"class" : "product-sorting is-product-toolbar"})
        product_category_ul = product_category_main_div.find("ul" , {"class" : "selected-filters"})
        product_category_li = product_category_ul.findAll("li")

        for i in product_category_li:
            if i.has_attr('class'):
                if i['class'] == 'hidden':
                    continue
            else:
                if i.find("a"):
                    product_category_a = i.find("a").text
                    p_c_split = product_category_a.split(" ")
                    p_c_length = len(p_c_split)
                    if p_c_length > 1 :
                        product_category = product_category_a.split(" ")[1].replace('\n',"")
                        break
                    else:
                        product_category = "NA"
                else:
                    continue

        for i in product_list:
            try:
                product_a = i.a['href']
                try:
                    p_url =  'https://www.vanharen.nl' + product_a
                    #print(p_url)
                    req = urllib.request.Request(p_url, headers={'User-Agent': 'Mozilla/5.0'})
                    page_html = urllib.request.urlopen(req).read()
                except urllib.error.HTTPError:
                    continue
                except ValueError:
                    continue
                except http.client.IncompleteRead:
                    continue



                product_htmlpage_soup = soup(page_html, "html.parser")
                product_body = product_htmlpage_soup.body

                product_name_header = product_body.find("section" , {"class" : "details image-zoom-container"})
                product_name_section = product_name_header.find("section" , {"class" : "features"})
                product_name = product_name_section.find("h1").find("span").text.replace('\n',"")

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

                #print(Url_tosave, date, type, product_category, product_name, product_price,old_productprice, position , product_number , product_color, product_description, no_of_reviews, star_rating, free_shipping_indicator, main_picture)
                try:
                    f.write(Url_tosave + "," + date + "," + type + "," + product_category + "," + product_name + "," + product_price.replace(",",".") + "," + old_productprice.replace(",",".") + "," + str(position) + "," + product_number + "," + product_color + "," +
                    product_description.replace(",", " ") + "," + no_of_reviews + "," +
                    star_rating + "," + free_shipping_indicator + "," + str(main_picture) + "\n")
                except ValueError:
                    continue
                position = position + 1
                if position == 11:
                    break
            except ValueError:
                continue
            except http.client.IncompleteRead:
                continue
            except urllib.error.HTTPError:
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
