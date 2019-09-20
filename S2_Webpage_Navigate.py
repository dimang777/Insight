# Import libraries
import pandas as pd
from S1_DataScraping import scrape_page_raw, scrape_product, format_data_df



def get_product_listing_html(url_page):
    html_page = scrape_page_raw(url_page)
    product_listing_container_html = html_page.find(class_ = 'product_listing_container') # Isolate section that contains a list of products
    product_listing_html = product_listing_container_html.findAll(class_ = 'product_name') # Isolate each product information

    return product_listing_html

max_items = 5520 # should be in multiples of 12 - max is 5520

page_idx = 0
while page_idx <= max_items:
    print(page_idx)
    url_page = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/wine-14/wine-14/red-wine-14001?pageView=grid&orderBy=1&fromPage=catalogEntryList&beginIndex='+ str(page_idx)

    product_listing_html = get_product_listing_html(url_page)
    
    for product_idx in range(len(product_listing_html)):
        product_page_link = product_listing_html[product_idx].find('a', href=True)['href']
        
        values = scrape_product(product_page_link, page_idx)
    
        data = format_data_df(values)
        if page_idx == 0 and product_idx == 0:
            rw = pd.DataFrame(data)
        else:
            rw = pd.concat([rw, pd.DataFrame(data)])
        
        page_idx = page_idx + 1


rw.to_csv('rw.csv', index=False)


