## Insight project

WineTales
"WineTales" is a wine recommendation system where you enter a wine product to find three similar products.

The system consists of three parts, which are data scraping tool for extracting product information from the web using Python¡¯s Beautifulsoup package, front-end component built using Python¡¯s Flask and HTML where the user can interact with the website to receive the recommendations (www.winetales.live:5000), and the recommendation engine that processes the input in the background using various Python packages including Pandas, Gensim, and NLTK to output the recommended products.
Folders
/Data
Data folder contains relevant data used for the recommendation engine. Data formats are in CSV, Excel, and pickle. The folder divides into three subdirectories, which are raw, cleaned, and for_models. As the names suggest, raw contains unprocessed data, cleaned contain cleaned data, and for_model contains final data set that were used to train the models. 
Two types of data were used. The first type is scraped data on the red wine category from the LCBO website. The second type is massive wine data from the Kaggle (https://www.kaggle.com/zynicide/wine-reviews). 
Some of the data that are too large were excluded. Namely, wine data available in Kaggle was not included. 

/script
Script contains Python files that were used to create the web scraping tools and recommendation engine of the system. There are three subdirectories for each component of the system. 
scrape folder contains LCBO_scrape_tools.py and lcbo_navigate_scrape_main.py. The first file contains functions based on Beautifulsoup that extracts information from a LCBO wine product webpage. The second file helps to navigate the website and contains functions that exports the scraped data to CSV files. 
rw_process folder contains Python files that were used to process the raw data that was scraped.

NLP folder contains Python scripts that processed the Kaggle wine and LCBO wine data to train a doc2vec model.

Recomm folder contains the scripts that were used as the engine behind the web app

/WineTales_app
Contains Python script based on Flask as well as HTML, css, js files used to generate the WineTales web app.

/notebooks
This folder contains any Jupyter notebook files that were used present the development progress of the project
