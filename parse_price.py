# -*- coding: utf-8 -*-
"""
Created on Tue May  7 04:24:30 2019

@author: magilo
"""
from bs4 import BeautifulSoup
import requests

def curr_only(rawdata):
    return float(''.join(c for c in rawdata if c.isdigit() or c =="."))

def hm_pp(url):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    page_link = url
    page_response = requests.get(page_link, timeout=5, headers=agent)
    page_soup = BeautifulSoup(page_response.content, "html.parser")
    p_name = page_soup.find("title").text
    p2 = page_soup.find("span", {"class":"price-value"})
    sale_p = curr_only(p2.text)
    p3 = page_soup.find("div", {"class":"tealiumProductviewtag productview parbase"}).text

    if "SALES_PRICE" in p3:
        sale = True
        std_p_key = "product_original_price"
        std_p_sind = p3.find(std_p_key)
        std_p = curr_only(p3[std_p_sind:std_p_sind+34])
    else:
        sale = False
        std_p = None
    return sale_p, sale, p_name, std_p


def uniqlo_pp(url):
    page_link = url
    page_response = requests.get(page_link, timeout=5)
    page_soup = BeautifulSoup(page_response.content, "html.parser")
    
    div = page_soup.find("div", {"class": "product-price"})
    span = div.find("span", {"class": "price-sales", "itemprop": "price"})
    #span is an html object
    span2 = div.find("span", {"class": "price-standard", "itemprop": "price"})
    
    product = page_soup.find("h1")
    product_span = product.find("span", {"class": "product-name", "itemprop": "name"})
    if span2 != None:
        standard = float(span2.text)
    else:
        standard = None
    return float(span.text), span2 != None, str(product_span.text), standard


def madewell_pp(url):
    page_link = url
    page_response = requests.get(page_link, timeout=5)
    page_soup = BeautifulSoup(page_response.content, "html.parser")
    
    div_p = page_soup.find("div", {"class": "product-price"})
    sale_p = div_p.find("span", {"class": "price-sales"})
    
    sale_p = curr_only(sale_p.text)
    std_p = div_p.find("del", {"class": "price-standard"})
    
    p_name = page_soup.find("h1", {"class":"product-name", "itemprop": "name"})
    cw = page_soup.find("div", {"class":"selected-value"})
    p_name = p_name.text + " " + cw.text.strip()

    if std_p != None:
        standard = float(curr_only(std_p.text))
    else:
        standard = None
    
    return sale_p, std_p != None, p_name, standard


def allsaints_pp(url):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    page_link = url
    page_response = requests.get(page_link, timeout=15, headers=agent)
    page_soup = BeautifulSoup(page_response.content, "html.parser")

    title = page_soup.find("title").text
    p_name = title[21:]

    p_now = page_soup.find("span", {"class": "product__price-now price-now"})
    
    if p_now != None:
        sale_p = curr_only(p_now.text)
        p_was = page_soup.find("span", {"class": "product__price-was price-was"})
        std_p = curr_only(p_was.text)
        
    else:
        price_h2 = page_soup.find("h2", {"class":"product__price"})
        price_div = price_h2.find("div", {"tabindex":"0"})
        sale_p = curr_only(price_div.text)
        std_p = None
        
    return sale_p, p_now != None, p_name, std_p
    
