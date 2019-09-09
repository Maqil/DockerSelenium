import os
import logging
import pprint
import datetime

import mysql.connector

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

logging.getLogger().setLevel(logging.INFO)

pp = pprint.PrettyPrinter(indent=1)

data = []

BASE_URL = 'https://rnm.franceagrimer.fr/'


def goBack():
    driver.execute_script("window.history.go(-1)")


def getMarche(id, search_product):

    listmarketslabels = []
    allpriceslist = []
    prices = []

    markets = []
    labels = []
    dates = []
    currencies = []
    unities = []

    # Find the input form for product to search
    inputProduct = driver.find_element_by_id('produit')
    inputProduct.send_keys(search_product)
    inputProduct.send_keys(Keys.ENTER)

    marketslabels = driver.find_elements_by_xpath(
        "//*[@class='sta1' or @class='sta2' or @class='sta3' or @class='sta4' or @class='sta5' or @class='sta6' or @class='sta7']")

    for iter in marketslabels:
        listmarketslabels.append(iter.text)
        prixclass = iter.find_elements_by_class_name('tdcotr')

        for prix in prixclass:
            allpriceslist.append(prix.text)
        allpriceslist = ["0.0" if x == ' ' else x for x in allpriceslist]

        if (search_product == 'fève' or search_product == 'orange'):
            price = allpriceslist[::3]

        else:
            price = allpriceslist[::4]

    prices.extend(price)

    for i in range(0, len(listmarketslabels)):
        if not (search_product.upper() in listmarketslabels[i]) and (search_product.upper() + " : " not in listmarketslabels[i]):
            for j in range(i + 1, len(listmarketslabels)):

                if search_product.upper() in listmarketslabels[j] and (search_product.upper() + " : " not in listmarketslabels[j]):

                    cleanmarkets = listmarketslabels[i].split(" marché ")[0]
                    markets.append(cleanmarkets)

                    # cleanlabels = listmarketslabels[j].replace(
                    #     search_product.upper() + " ", "")
                    # labels.append(cleanlabels)

                    cleandate = listmarketslabels[i].split(
                        " du ")[1].split(" (cou")[0]

                    formateddate = datetime.datetime.strptime(
                        cleandate, '%d/%m/%y').strftime('%Y-%m-%d')
                    dates.append(formateddate)

                    for s in listmarketslabels:
                        if " le " in s:
                            cleandevise = listmarketslabels[i].split(
                                " : ")[1].split(" le ")[0]
                    currencies.append(cleandevise)

                    for x in listmarketslabels:
                        if " le " in x:
                            cleanunities = listmarketslabels[i].split(" le ")[
                                1]

                    unities.append(cleanunities)

                else:
                    i = j + 1
                    break

        elif search_product.upper() in listmarketslabels[i] and (search_product.upper() + " : " in listmarketslabels[i]):
            for j in range(i + 1, len(listmarketslabels)):
                if search_product.upper() in listmarketslabels[j] and (search_product.upper() + " : " not in listmarketslabels[j]):

                    cleanmarkets = listmarketslabels[i].split(" marché ")[0]
                    markets.append(cleanmarkets)

                    # cleanlabels = listmarketslabels[j].replace(
                    #     search_product.upper() + " ", "")
                    # labels.append(cleanlabels)

                    cleandate = listmarketslabels[i].split(
                        " du ")[1].split(" (cou")[0]

                    formateddate = datetime.datetime.strptime(
                        cleandate, '%d/%m/%y').strftime('%Y-%m-%d')
                    dates.append(formateddate)

                    for s in listmarketslabels:
                        if " le " in s:
                            cleandevise = listmarketslabels[i].split(
                                " : ")[1].split(" le ")[0]
                    currencies.append(cleandevise)

                    for x in listmarketslabels:
                        if " le " in x:
                            cleanunities = listmarketslabels[i].split(
                                " le ")[1].split(search_product.upper())[0]

                    unities.append(cleanunities)

                else:
                    i = j + 1
                    break

    labelslist = []

    labelsclass = driver.find_elements_by_class_name('tdcotl')
    for lbls in labelsclass:
        labelslist.append(lbls.text)
        labels = [x.replace(search_product.upper() + " ", "")
                  for x in labelslist]

    logging.info(search_product.upper())

    logging.info(len(markets))
    logging.info(markets)
    logging.info(len(labels))
    logging.info(labels)
    logging.info(len(dates))
    logging.info(dates)
    logging.info(len(currencies))
    logging.info(currencies)
    logging.info(len(unities))
    logging.info(unities)
    logging.info(len(prices))
    logging.info(prices)

    # for marketelem in zip(markets, labels, unities, currencies, dates, prices):
    #     data.extend(marketelem)
    #     cursor.execute(
    #         """INSERT INTO PRODUIT (NOM_MARCHE,ID_CULTURE, LIBELLE,DESCRIPTION_UNITE, DESCRIPTION_DEVISE, DATE,PRIX) VALUES (%s,
    #         """ + str(id) + """,%s,%s,%s,%s,%s)""", marketelem)

    # connection.commit()

# try:
#     connection = mysql.connector.connect(host='localhost',
#                                          database='ATMAR',
#                                          user='root',
#                                          password='',
#                                          port=3306)
#     cursor = connection.cursor()

    # cursor.execute('delete from PRODUIT')
    # cursor.execute('ALTER TABLE PRODUIT AUTO_INCREMENT = 1')


display = Display(visible=0, size=(800, 600))
display.start()
logging.info('Initialized virtual display..')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': os.getcwd(),
    'download.prompt_for_download': False,
})
logging.info('Prepared chrome options..')

driver = webdriver.Chrome(chrome_options=chrome_options)
logging.info('Initialized chrome browser..')

driver.get(BASE_URL)
logging.info('Accessed %s ..', BASE_URL)
logging.info('Page title: %s', driver.title)

# getMarche(1, "tomate")
# goBack()
# getMarche(2, "pomme de terre")
# goBack()
# getMarche(3, "oignon")
# goBack()
getMarche(4, "fève")
# goBack()
# getMarche(5, "poivron")
# goBack()
# getMarche(6, "pastèque")
# goBack()
# getMarche(7, "melon")
# goBack()
# getMarche(8, "orange")
# goBack()
# getMarche(9, "fraise")
# goBack()
# getMarche(10, "framboise")

# getMarche(1, "tomate", cursor)
# goBack()
# getMarche(2, "pomme de terre", cursor)
# goBack()
# getMarche(3, "oignon", cursor)
# goBack()
# getMarche(4, "fève", cursor)
# goBack()
# getMarche(5, "poivron", cursor)
# goBack()
# getMarche(6, "pastèque", cursor)
# goBack()
# getMarche(7, "melon", cursor)
# goBack()
# getMarche(8, "orange", cursor)
# goBack()
# getMarche(9, "fraise", cursor)
# goBack()
# getMarche(10, "framboise", cursor)


# except mysql.connector.Error as error:
#     print("Failed to insert record ERROR : {}".format(error))

# finally:
#     if (connection.is_connected()):
#         connection.close()
#         print("MySQL connection is successful")

# Quit Chrome browser
# driver.close()
