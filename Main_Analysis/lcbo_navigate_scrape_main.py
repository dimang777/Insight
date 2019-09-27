# Import libraries
import pandas as pd
from lcbo_scrape_tools import scrape_page_raw, scrape_product, format_data_df_v2, parse_info, read_saved_soup, format_data_df_v2



def get_product_listing_html(url_page):
    _, html_page = scrape_page_raw(url_page)
    product_listing_container_html = html_page.find(class_ = 'product_listing_container') # Isolate section that contains a list of products
    product_listing_html = product_listing_container_html.findAll(class_ = 'product_name') # Isolate each product information

    return product_listing_html


def use_web_toscrape(max_items):
    page_idx = 0
    while page_idx <= max_items:
        print(page_idx)
        url_page = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/wine-14/wine-14/red-wine-14001?pageView=grid&orderBy=1&fromPage=catalogEntryList&beginIndex='+ str(page_idx)
    
        product_listing_html = get_product_listing_html(url_page)
        with open('product_list' + str(page_idx)+'.html', "w", encoding='utf-8') as file:
            file.write(str(product_listing_html))


        for product_idx in range(len(product_listing_html)):
            product_page_link = product_listing_html[product_idx].find('a', href=True)['href']
            
            values = scrape_product(product_page_link, page_idx)
        
            data = format_data_df_v2(values)
            if page_idx == 0 and product_idx == 0:
                rw = pd.DataFrame(data)
            else:
                rw = pd.concat([rw, pd.DataFrame(data)])
            
            page_idx = page_idx + 1


    rw.to_csv('rw_web_v4.csv', index=False)

def scrape_url(max_items):
    page_idx = 0
    while page_idx <= max_items:
        print(page_idx)
        url_page = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/wine-14/wine-14/red-wine-14001?pageView=grid&orderBy=1&fromPage=catalogEntryList&beginIndex='+ str(page_idx)
    
        product_listing_html = get_product_listing_html(url_page)
        
        for product_idx in range(len(product_listing_html)):
            product_page_link = product_listing_html[product_idx].find('a', href=True)['href']

            data = {'URL':product_page_link}

            if page_idx == 0 and product_idx == 0:
                url_df = pd.DataFrame(data, index = [page_idx])
            else:
                url_df = pd.concat([url_df, pd.DataFrame(data, index = [page_idx])])
            
            page_idx = page_idx + 1

    url_df.to_csv('url_df.csv', index=False)

def use_saved_soups_toscrape(max_products):
    # This method doesn't seem to capture UTF-8 characters (i.e., ones with accents)
    # So this method can be used to just get the picture sources
    # divided into two parts to avoid losing data
    for product_idx in range(3000):
        print(product_idx)
        soup = read_saved_soup('html_source/' + str(product_idx) + '.html')
        values = parse_info(soup)
        data = format_data_df_v2(values)
        if product_idx == 0:
            rw = pd.DataFrame(data)
        else:
            rw = pd.concat([rw, pd.DataFrame(data)])

    rw.to_csv('rw_v2_include_pic_src_1_3000.csv', index=False)

    for product_idx in range(3000,max_products):
        print(product_idx)
        soup = read_saved_soup('html_source/' + str(product_idx) + '.html')
        values = parse_info(soup)
        data = format_data_df_v2(values)
        if product_idx == 3000:
            rw = pd.DataFrame(data)
        else:
            rw = pd.concat([rw, pd.DataFrame(data)])

    rw.to_csv('rw_v2_include_pic_src_3001andon.csv', index=False)

def add_url_to_df():
    # add picture source and product url to the existing df
    rw_v3_pic_and_url = pd.read_excel('RW_data_wofeaturedwines_UTF-8.xlsx')
    pic_url = pd.read_excel('rw_v2_include_pic_src.xlsx')
    url_df = pd.read_excel('url_df.xlsx')
    rw_v3_pic_and_url['URL'] = url_df['URL']
    rw_v3_pic_and_url['Pic_src'] = pic_url['Pic_src']
    rw_v3_pic_and_url.to_excel('rw_v3_pic_and_url.xlsx', index=False)

def save_to_pickle():
    rw_df_mvp_v2 = pd.read_excel('rw_df_mvp_v2.xlsx')
    rw_df_mvp_v2.to_pickle("rw_df_mvp_v2.pkl")


if __name__ == '__main__':
    max_items = 5520 # should be in multiples of 12 - max is 5520 - used to nativate pages
    max_products = 5526 # number of red wine products


    save_to_pickle()
    # use_saved_soups_toscrape(max_products)

    # use_web_toscrape(24)
    # use_web_toscrape() # First version without picture src
    # use_saved_soups_toscrape(max_products)

    # use_saved_soups_toscrape(max_products)

    # scrape_url(max_items)
    # add_url_to_df()


