import requests
import re
import json 
import time

f = open("gamelist.txt","r")
contents = f.read().split('\n')

outfile = open("outfile.csv", "a")
print("Got {} games".format(len(contents)))
i = 1

for line in contents:
    print("Getting game [{}/{}]".format(i,len(contents)))
    request = requests.get("https://store.steampowered.com/app/{}".format(line))


    while 1:
        storerequest= requests.get("https://store.steampowered.com/api/appdetails?appids={}".format(line))
        if storerequest.status_code == 200:
            break
        print("Got a {} waiting".format(storerequest.status_code))
        time.sleep(60)

    storejson = json.loads(storerequest.text)

    m = re.findall('<a[^>]*class=\\\"app_tag\\\"[^>]*>([^<]*)</a>', request.text) # yoinked from https://github.com/rallion/depressurizer/blob/master/Depressurizer/GameDB.cs
    taglist = ""
    for x in m:
        taglist = taglist + x.strip() + ", "
    
    if "data" in storejson[line]:
        if "name" in storejson[line]["data"]:
            outfile.write(storejson[line]["data"]["name"]+";"+line+";"+taglist.strip().replace("\t","")+"\n")

    i += 1
    

f.close
outfile.close
