# Import libraries
import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import numpy as np
from fake_useragent import UserAgent
import io
import time

def find_class(soup, class_name):
    """Finds and returns the desired class within html
    Input: Beautifulsoup object and the name of the class to find
    Output: cropped html content"""

    content = soup.find(class_ = class_name)

    return content
    
def get_info(html, category):
    # Finds and returns the desired information of the product
    # Input: html text containing the information
    # Output: information
    
    keywords = {
        'id': ['LCBO#:', 'VINTAGES#:'],
        'price': '$',
        'name': '',
        'description': '',
    }
    
    switcher = {
        'id': check_avail_keyword,
        'price': check_avail_keyword,
        'name': get_info_name,
        'description': get_info_description,
    }
    
    texts = html.findAll(text=True)
    keyword = keywords[category.lower()]
    
    for text in texts:
        if switcher[category](text, keyword):
            if category == 'id':
                flags = np.array([word in text for word in keyword])
                selected_keyword = np.array(keyword)[flags][0]
                start_idx = get_keyword_idx(text, selected_keyword)
                if selected_keyword == 'LCBO#:':
                    return ('L' + text[start_idx:].strip())
                elif selected_keyword == 'VINTAGES#:':
                    return ('V' + text[start_idx:].strip())
            elif category == 'price':
                start_idx = get_keyword_idx(text, keyword)
                return float(text[start_idx:].strip().replace(',', ''))
            elif category == 'name':
                start_idx = get_keyword_idx(text, keyword)
                # For category such as name, whitespace between words should
                # be kept
                return text[start_idx:].lstrip().rstrip()
            if category == 'description':
                start_idx = get_keyword_idx(text, keyword)
                return text[start_idx:].lstrip().rstrip() # For category such as name, whitespace between words should be kept

def get_info_name(text, keyword):
    return True

def get_details(html):
    # Finds and returns the product details
    # Input: html text containing the information
    # Output: size, alcohol, city, country, brand, sugar, sweetness, style1, style2, variety
    texts = html.findAll(text=True)
    
    keyword = 'Bottle Size:'
    size_idx = find_item_loc(keyword, texts)
    if size_idx >= 0:
        size = int(texts[size_idx].split()[0])
    else:
        size = None
    
    keyword = 'Alcohol/Vol:'
    alcohol_idx = find_item_loc(keyword, texts)
    if alcohol_idx >= 0:
        alcohol = float(texts[alcohol_idx].strip('%'))
    else:
        alcohol = None
    
    keyword = 'Made In:'
    madein_idx = find_item_loc(keyword, texts)
    if madein_idx >= 0:
        location = [x.strip() for x in texts[madein_idx].split(',')] # split by comma
        if len(location) == 2:
            [city, country] = location
        elif len(location) == 1:
            [city, country] = [None, location[0]]
    else:
        [city, country] = [None, None]
    
    keyword = 'By:'
    brand_idx = find_item_loc(keyword, texts)
    if brand_idx >= 0:
        brand = texts[brand_idx]
    else:
        brand = None
    
    keyword = 'Sugar Content:'
    sugar_idx = find_item_loc(keyword, texts)
    if sugar_idx >= 0:
        sugar = float(texts[sugar_idx].split()[0]) # Return the first number
    else:
        sugar = None
    
    keyword = 'Sweetness Descriptor:'
    sweetness_idx = find_item_loc(keyword, texts)
    if sweetness_idx >= 0:
        sweetness = texts[sweetness_idx] # Return the first number
    else:
        sweetness = None
    
    keyword = 'Style:'
    style_idx = find_item_loc(keyword, texts)
    if style_idx >= 0:
        styles = [x.strip() for x in texts[style_idx].split('&')] # split by ampersand
        if len(styles) == 2:
            [style2, style1] = styles
        elif len(styles) == 1:
            [style2, style1] = [None, styles[0]]
        else:
            raise Exception('more than two styles')
    else:
        [style2, style1] = [None, None]
      
    keyword = 'Varietal:'
    variety_idx = find_item_loc(keyword, texts)
    if variety_idx >= 0:
        variety = texts[variety_idx]
    else:
        variety = None
    
    return size, alcohol, city, country, brand, sugar, sweetness, style1, style2, variety
    
def get_featured_wines(html):
    # Finds and returns the LCBO # of the two featured wines
    # Input: html text containing the information
    # Output: LCBO# 1 and 2

    texts = html.findAll(text=True)
    
    keyword = 'LCBO#:'
    LCBO_ids = []
    for text in texts:
        if check_avail_keyword(text, keyword):
            start_idx = get_keyword_idx(text, keyword)
            LCBO_ids.append(int(text[start_idx:].strip()))
            
    if len(LCBO_ids) == 0:
        LCBO_ids = None
                
    return LCBO_ids
    
def get_recomm_foods(html):
    # Finds and returns the name of the recommended foods
    # Input: html text containing the information
    # Output: list of foods
    
    if html != None:
        texts = html.findAll(text=True)
        
        Recomm_foods = []
    
        Recomm_foods.append(texts[6].lstrip().rstrip())
        if len(texts) >= 10:
            Recomm_foods.append(texts[9].lstrip().rstrip())
            if len(texts) >= 13:
                Recomm_foods.append(texts[12].lstrip().rstrip())
    else:
        Recomm_foods = None
                
    return Recomm_foods

def check_avail_keyword(text, keyword):
    # Used by get_info to check if the text contains the keyword or not
    # Input: text and keyword
    # Output: boolean
    if len(keyword) == 1:
        return 0 <= text.find(keyword)
    elif len(keyword) == 2:
        flags = [word in text for word in keyword] # keyword = ['LCBO#:', 'VINTAGES#:']
        return any(flags)
  
def get_info_description(text, keyword):
    # Used by get_info to check if the text contains meaningful characters
    # Input: text
    # Output: boolean
    return len(text) > 5 # Basically pass new line strings and find the first actual words

def get_keyword_idx(text, keyword):
    # Find the index of the character immediately after a keyword
    # Input: String, keyword
    # Output: index
    idx = len(text) - len(text.lstrip()) + len(keyword) # Start index of whitespace after the keyword
    return idx

def find_html_sections(soup):
    # Find relevant sections for each feature extraction from the webpage html script
    # soup is mutable - i.e., passed by reference
    # Input: soup - html document of the entire webpage
    # Output: Cropped html of each section
    LCBO_html = find_class(soup, 'brand-details') # LCBO#
    price_html = find_class(soup, 'price') # price
    name_html = find_class(soup, 'current') # name
    description_html = find_class(soup, 'product_text') # description
    product_img_html = find_class(soup, 'product_main_image') # product image
    product_details_html = find_class(soup, 'product-details-list') # Bottle Size, Alcohol/Vol, Made In, Brand, Sugar Content, Sweetness Descriptor, Style, Varietal
    
    featured_wines_html = find_class(soup, 'recommendations-wrapper') # two recommended wines
    food_recomms_html = find_class(soup, 'carouselWrapper') # three recommended foods
    
    return LCBO_html, price_html, name_html, description_html, product_img_html, product_details_html, featured_wines_html, food_recomms_html
    
def find_item_loc(keyword, texts):
    # Find the index of an item in a list of texts
    # input: keyword, list of texts
    # output: the index of non-newline after the keyword
    item_idx = -1
    for idx, text in enumerate(texts):
        if item_idx < 0:
            if 0 <= text.find(keyword):
                item_idx = idx
        else:
            item_idx = item_idx + 1
            if text != '\n':
                break
                
    return item_idx

def scrape_page_raw(url):
    # Scrape the webpage and return the raw html script
    # soup is mutable - i.e., passed by reference
    # Input: url - url of the webpage to scrape
    # Output: soup - html document of the entire webpage
    # Source: https://stackoverflow.com/questions/44865673/access-denied-while-scraping
    # Source: https://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit
    # ua = UserAgent()
    # print(ua.chrome)
    # header = {'User-Agent':str(ua.chrome)}
    # print(header)
    # agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    delays = [x / 100 for x in range(100,400)]
    delay = np.random.choice(delays)
    time.sleep(delay)
    user_agent = get_random_ua()
    user_agent = user_agent[:-1]
    headers = {
        'user-agent': user_agent,
    }
    page = requests.get(url,headers=headers)

    return page.text, BS(page.text, 'html.parser')

def get_random_ua():
    # Get a random user agent
    # Input:
    # Output: random user agent str

    random_ua = ''
    ua_file = 'ua_file.txt'
    try:
        with open(ua_file) as f:
            lines = f.readlines()
        if len(lines) > 0:
            prng = np.random.RandomState()
            index = prng.permutation(len(lines) - 1)
            idx = np.asarray(index, dtype=np.integer)[0]
            random_ua = lines[int(idx)]
    except Exception as ex:
        print('Exception in random_ua')
        print(str(ex))
    finally:
        return random_ua

def format_data_df(values):
    # Given a tuple of values, format it into dict so that it can be appended to df
    # Input: tuple of values
    # Output: formatted dict
    columns = ( 'LCBO_id', 
                'Price', 
                'Name',
                'Description',
                'Size',
                'Alcohol',
                'Madein_city',
                'Madein_country',
                'Brand',
                'Sugar',
                'Sweetness',
                'Style1',
                'Style2',
                'Variety',
                'Featured_wines',
                'Recomm_foods')
    data = {}
    for i, column in enumerate(columns):
        data[column] = [values[i]]
    return data

def format_data_df_v2(values):
    # Given a tuple of values, format it into dict so that it can be appended to df
    # Input: tuple of values
    # Output: formatted dict
    columns = ( 'LCBO_id', 
                'Price', 
                'Name',
                'Description',
                'Size',
                'Alcohol',
                'Madein_city',
                'Madein_country',
                'Brand',
                'Sugar',
                'Sweetness',
                'Style1',
                'Style2',
                'Variety',
                'Featured_wines',
                'Recomm_foods',
                'URL',
                'Pic_src')
    data = {}
    for i, column in enumerate(columns):
        data[column] = [values[i]]
    return data

def scrape_product(url, index = -1):
    # Given the product url, get values for the df element
    # Input: url of the product to scrape, index of the product - used to save the html file locally
    # Output: a tuple of scraped information
    
    # Get html of the url
    html, soup = scrape_page_raw(url)

    with open(str(index)+'.html', "w", encoding='utf-8') as file:
        file.write(str(html))

    return parse_info(soup, url)


def parse_info(soup, url):
    # Given the Beautifulsoup object, get values for the df element
    # Input: Beautifulsoup object to scrape, url to save into the df
    # Output: a tuple of scraped information

    # Get relevant sections
    LCBO_html, price_html, name_html, description_html, product_img_html, product_details_html, featured_wines_html, food_recomms_html = \
    find_html_sections(soup)

    # Get_info
    LCBO_id = get_info(LCBO_html, 'id')
    price = get_info(price_html, 'price')
    name = get_info(name_html, 'name')
    description = get_info(description_html, 'description')
    size, alcohol, madein_city, madein_country, brand, sugar, sweetness, style1, style2, variety = \
        get_details(product_details_html)
    pic_src = get_pic_src(soup)
    featured_LCBO_id = get_featured_wines(featured_wines_html) # Featured wines change after each loading
    recomm_foods = get_recomm_foods(food_recomms_html) # sometimes there is no suggested foods

    return (LCBO_id, price, name, description, size, alcohol, madein_city, madein_country, brand, sugar, sweetness, style1, style2, variety, featured_LCBO_id, recomm_foods, url, pic_src)

def read_saved_soup(file_name):
    # Read the saved Breautifulsoup object
    # Input: Beautifulsoup object to scrape, url to save into the df
    # Output: a tuple of scraped information

    f = io.open(file_name, mode="r", encoding="utf-8")
    return BS(f.read())

def get_pic_src(soup):
    # Get the web source of the picture of the wine product
    # Input: Beautifulsoup object to scrape
    # Output: URL of the picture in str

    images = soup.findAll('img')
    return 'https://www.lcbo.com' + images[3]['src']

if __name__ == '__main__':
    None
    # url1 = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/red-wine-14001/folonari-valpolicella-classico-doc-828'
    # soup = scrape_page_raw(url1)
    # soup = read_saved_soup('html_source/0.html')

    # values = parse_info(soup)

    # url2 = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/yalumba-coonawarra-cabernet-sauvignon-460667?vmpContextPage=category&vmpContextItem=3074457345616679269&vmpBin=2#.XX_8bmZ7mMo'
    # values = scrape_product(url2)
    # data = format_data_df(values)
    # rw = pd.concat([rw, pd.DataFrame(data)])
    
    
    # url3 = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/red-wine-14001/domaine-breton-clos-s%C3%A9n%C3%A9chal-2015-780809#.XYJB0WZ7mMo'
    # values = scrape_product(url3)
    # data = format_data_df(values)
    # rw = pd.concat([rw, pd.DataFrame(data)])
    # rw.to_csv('rw.csv', index=False)
    
