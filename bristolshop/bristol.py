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
url_file = open('/Users/ishitaverma/Desktop/zalando/bristolshop/bristolshop.csv' , "r")
count = 0

for line in url_file:
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
    type = "List Page"

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_html = urllib.request.urlopen(req).read()
        htmlpage_soup = soup(page_html, "html.parser")
        html_body = htmlpage_soup.body

        divs = html_body.find("ul" , {"id" : "products-list"})

        div_products = divs.findAll("li")

        product_category_div = html_body.find("div" , {"class" : "breadcrumbs"})
        p_c_li = product_category_div.findAll("li")
        product_category = p_c_li[len(p_c_li) - 1].text

    except AttributeError:
            continue
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

    for i in div_products:

        try:
            product_a = i.a['href']

            req_product = urllib.request.Request(product_a, headers={'User-Agent': 'Mozilla/5.0'})
            product_html = urllib.request.urlopen(req_product).read()

            product_htmlpage_soup = soup(product_html, "html.parser")
            product_body = product_htmlpage_soup.body

            product_header_div = product_body.find("div" , {"class" : "product-name"})
            product_name = product_header_div.h1.text

            price_div = product_body.find("div" , {"class" : "price-box "})

            if price_div.find("p" , {"class" : "old-price"}):
                old_productprice = price_div.find("p" , {"class" : "old-price"}).find("span" , {"class" : "price"}).text.replace("\n" , " ")
                print (old_productprice)

            if price_div.find("p" , {"class" : "special-price"}):
                product_price = price_div.find("p" , {"class" : "special-price"}).find("span" , {"class" : "price"}).text.replace("\n" , " ")

            if price_div.find("span" , {"class" : "regular-price"}):
                product_price = price_div.find("span" , {"class" : "regular-price"}).find("span" , {"class" : "price"}).text.replace("\n" , " ")
                old_productprice = "NA"

            if product_body.find(string = re.compile("Artikelnummer")).parent.parent:
                article_tag = product_body.find(string = re.compile("Artikelnummer")).parent.parent
                product_number = article_tag.find("span" , {"class" : "data"}).text

            if product_body.find(string = re.compile("Kleur")).parent.parent:
                color_tag = product_body.find(string = re.compile("Kleur")).parent.parent
                product_color = color_tag.find("span" , {"class" : "data"}).text

            try:
                f.write(url + "," + date + "," + type + "," + product_category + "," + product_name.strip('\n') + "," + product_price.replace(",",".") + "," + old_productprice.replace(",",".") + "," + str(position) + "," + product_number.strip('\n') + "," +  product_color.replace(",",".") + "," +
                product_description.replace(",", " ") + "," + no_of_reviews + "," +
                star_rating + "," + free_shipping_indicator + "," + str(main_picture) + "\n")
            except ValueError:
                continue

            position = position + 1
            if position == 11:
                break

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
