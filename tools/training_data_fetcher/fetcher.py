#!/bin/python

import requests
import os
import openpyxl
from concurrent.futures import ThreadPoolExecutor

# configuration
apiurl = "https://maps.googleapis.com/maps/api/staticmap"
apikey = ""
zoomlevel = 21
imagewidth = 1000
imageheight = 1000
dataexcel = "data.xlsx"
downloadthreads = 1000
#
def fetch_img(lat, long):
    response = requests.get(
        "{url}?center={lat},{log}&zoom={zoom}&size={wid}x{hei}&maptype=satellite&key={key}".format(
            url=apiurl,
            lat=lat,
            log=long,
            zoom=zoomlevel,
            wid=imagewidth,
            hei=imageheight,
            key=apikey,
        )
    )
    if response.status_code == 200:
        return response.content
    return null

def download_img(lat,log,savepath):
    file = open(savepath,"wb")
    while(True):
        data = fetch_img(lat,log)
        if(data != null):
            file.write(data)
            file.close()
            return
        else:
            print("Download failed retrying")

os.makedirs("data",exist_ok=True)
os.makedirs("data/true",exist_ok=True)
os.makedirs("data/false",exist_ok=True)

pool = ThreadPoolExecutor(max_workers=downloadthreads)

wb = load_workbook(dataexcel,read_only = True)
sheet = wb.active

for i, row in enumerate(sheet.iter_rows(min_row=1, values_only=True), start=1):
    lat,log,imagetype = row
    pool.submit(download_img,lat,log,"data/{}/img_{}.jpg".format(imgtype,i))

pool.shutdown()