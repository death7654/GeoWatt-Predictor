#!/bin/python

import requests
import os
from concurrent.futures import ThreadPoolExecutor

# configuration
apiurl = "https://maps.googleapis.com/maps/api/staticmap"
apikey = ""
zoomlevel = 21
imagewidth = 1000
imageheight = 1000
dataexcel = "data.ecxl"

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

pool = ThreadPoolExecutor(max_workers=1000)
file = open(dataexcel,"r")
i = 0 
while(true):
    i = i+1
    line = file.readline()
    if(line == ""):
        break
    lat,log,imagetype = line.split(",")
    pool.submit(download_img,lat,log,"data/{}/img_{}.jpg".format(imgtype,i))

pool.shutdown()
file.close()
print(fetch_img(40,73))