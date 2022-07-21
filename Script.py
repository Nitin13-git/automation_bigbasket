from statistics import quantiles
from py import process
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
import shutil
import time
import os
import json
import re
import pre_process
def start_driver(headless=True):
    if not headless:
        return webdriver.Firefox()
    chrome_options = webdriver.FirefoxOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    return webdriver.Firefox()




def get_product_data(product, raw_data_file):
    Brand = product.find("div", {"qa": "product_name"}).find("h6").text
    tmp1 = product.find("div", {"qa": "product_name"}).find("a").text
    Product=pre_process.comparing_ingredient_cleaning_dict(tmp1)
    Quantity = product.find("span", {"data-bind": "label"}).text
    discounted_pr= product.find("span", {"class": "discnt-price"}).text
    try:
        discounted_p=str(discounted_pr).split()[1]
    except:
        discounted_p=str(discounted_pr).split()[2]
    discounted_price,Quantity_new=pre_process.converstion(Quantity,discounted_p)
    actual_pr= product.find("span", {"class": "mp-price ng-scope"}).text
    actual_p=str(actual_pr).split()[1]
    try:
        actual_price,Quantity=pre_process.converstion(Quantity,actual_p)
    except:
        actual_price=None
        Quantity=1

    with open(raw_data_file, "a") as f:
        data = json.dumps({
            'Brand': Brand,
            'Product': Product,
            'Quantity': Quantity,
            'discounted_price': discounted_price,
            'actual_price':actual_price,


          
        })
        f.write(data + "\n")

 


def dump_json(raw_data_file, out_data_file):
    with open(raw_data_file) as f:
        data = f.read().strip().split("\n")
    js_data = list(map(lambda x: json.loads(x), data))

    with open(out_data_file, "w") as f:
        json.dump(js_data, f, indent=2)


if __name__ == "__main__":
    driver = start_driver()

    DEBUG = True
    OUTPUT_DIR = "Output"
    out_data_file = os.path.join(OUTPUT_DIR, "data.json")
    delay = 8

    with open('links.txt', 'r') as f:
        url_list = f.read().split("\n")

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    raw_data_file = os.path.join(OUTPUT_DIR, "raw_data.txt")
    with open(raw_data_file, "w") as f:
        pass

    for url in url_list:
        driver.get(url)
        print("Starting Download from: {}".format(url))

        time.sleep(delay)
        while True:
            try:
                driver.find_element_by_xpath("//button[@ng-click='vm.pagginator.showmorepage()']").click()
                time.sleep(2)
                # if DEBUG:
                #     print("Clicked Successfully")
            except Exception as e:
                # if DEBUG:
                #     print(e)
                break
        html = driver.execute_script("return document.documentElement.outerHTML")
        soup = bs(html, 'html.parser')
        products = soup.findAll("div", {"qa": "product"})

        rel_url = re.sub(r"/?.*", "", url)
        rel_url = rel_url.lstrip('https://www.bigbasket.com/pc/')

        ds_img = os.path.join(OUTPUT_DIR, 'images', 'large')
        dl_img = os.path.join(OUTPUT_DIR, 'images', 'small')

        if not os.path.exists(ds_img):
            os.makedirs(ds_img)
        if not os.path.exists(dl_img):
            os.makedirs(dl_img)

        for product in products:
            get_product_data(product, raw_data_file)

        print("Downloaded all data from: ".format(url))

    print("Download finished from all the links.")
    dump_json(raw_data_file, out_data_file)
    print("JSON file saved as {}".format(raw_data_file))

    driver.quit()
