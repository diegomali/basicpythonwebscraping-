# -*- coding: utf-8 -*-
import requests
import json
import bs4
from time import sleep
#Mudar
totalReg = None
dataPerPage = None
nroPages = None

file = open('reviews.csv', 'w')
file.write('USER;Verified')

def getPayload(page= 1):
    return { 'methods': [{"method":"reviews","params":{ "page": page }}], 'app_key': 'UVSfkRAXBjVv6PR6gPV0h2MmjWTysVdhGe3bHyjo' }

def getReviews(page= 1):
    global nroPages, totalReg, dataPerPage, nroPages
    headers = {'Content-Type': 'application/json'}
    response = requests.post('https://w2.yotpo.com/batch', data= json.dumps(getPayload(page)), headers=headers)
    responseData = json.loads(response.text)[0]
    soup = bs4.BeautifulSoup(responseData['result'], 'html.parser')
    if  nroPages == None:
        nodeInfoReviews = soup.select('div.yotpo-pager')[0]
        totalReg = int(nodeInfoReviews.attrs.get('data-total'))
        dataPerPage = int(nodeInfoReviews.attrs.get('data-per-page'))
        nroPages = totalReg // dataPerPage if  totalReg % dataPerPage == 0 else (totalReg // dataPerPage) + 1
        
    for review in soup.select('div.yotpo-review.yotpo-regular-box'):
        if('yotpo-template' in review['class']): continue
        reviewData = (review.select('label.yotpo-user-name')[0].text, 
                      'Y' if review.select('span.y-label.yotpo-user-title')[0].text == 'Verified Buyer' else 'N')
        file.write('%s;%s \n' % reviewData)
        
getReviews()
file.close()
