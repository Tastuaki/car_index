import datetime
import urllib.request
from itertools import count
import re
import os

bkey={"url":'',"end_tag":'',"search_tags":[],"tag_count":0,"search_result":True,"next":False}
# tkey={"url":'',"end_tag":'show-more',"search_tags":['<a class="card-link'],"tag_count":1,"search_result":True,"next":True}


def acs(url):
    try:
        all = urllib.request.urlopen(url).readlines()
    except urllib.error.URLError:
        print("URL NOT FOUND:"+url)
        return
    for h in range(len(all)):
        all[h] = all[h].decode("utf-8")
    return all

def indata(txt):
    t = ""
    ts = []
    flag = False
    htm_en=['&rsquo;','&quot;']
    chtm_en=["'",'"']
    lhtm_en = len(htm_en)
    txt = txt.strip()
    for i in count():
        # print("|"+txt+"|")
        if txt == "":
            return txt
        elif "<" == txt[0]:
            flag = True
            if ">" in txt:
                txt = txt[txt.find(">")+1:]
            else:
                return ""
            # print(txt)
        else:
            if ">" == txt[len(txt)-1]:
                flag = True
                if txt.rfind("</") != -1:
                    txt = txt[:txt.rfind("</")]
                elif txt[len(txt)-4:len(txt)] == "<br>":
                    txt = txt[:txt.rfind("<br>")]
                # print(txt) 
            else:
                if ">" in txt:
                    flag = True
                    t,txt = txt.split("<",1)
                    txt = "<"+txt
                    ts.append(t)
                    continue
                else:
                    if len(ts) > 0:
                        ts.append(txt)
                    break
    # print(ts)
    if flag:
        if len(ts) > 1:
            txt = ""
            for t in ts:
                txt += t + "\n"
        l = 0
        while re.search('&*;',txt) is not None:
            txt = txt.replace(htm_en[l],chtm_en[l])
            l += 1
            if l == lhtm_en:
                break
    else:
        print(txt+"→")
        txt = ""
    return txt

def ittrr(key):
    sdata = []
    all = acs(key["url"])
    data = []
    for i,data in enumerate(all):
        if key["end_tag"] in data:
            return sdata
            break
        else:
            for tag in key["search_tags"]:
                if tag in data:
                    print(data)
                    if "<a" in data:
                        url = data[data.find('href="')+6:data.rfind('.')+5]
                        if "http" not in url:
                            burl = ""
                            eurl = ""
                            burl,eurl = key["url"].split(".co",1)
                            if url[0] == "/":
                                url = burl+".co"+eurl[:eurl.find("/")]+url
                            else:
                                url = burl+".co"+eurl[:eurl.find("/")+1]+url
                    if indata(data) == "":
                        j=1
                        name = ""
                        while indata(all[i+j]) != "":
                            print(all[i+j])
                            name=indata(all[i+j])
                            j += 1
                        row = url+" "+name
                        sdata.append(row)
                        print("|"+row)
                    else:
                        row = url+" "+indata(data)
                        sdata.append(row)
                        print("|"+row)
                    # if key["search_result"]:
                    #     key["search_result"] = False

def set_key(key,row):
    stag = ""
    key["url"],key["end_tag"],stag=row.split("|",2)
    while "|" in stag:
        tag = ""
        tag,stag = stag.split("|",1)
        key["search_tags"].append(tag)
    if stag != "":
        key["search_tags"].append(stag)
    return key
        

base = os.path.dirname(__file__)
files_path = base+"\\ts"
set_path = base+"\\set"
print(set_path)

with open(set_path,encoding='utf-8') as f:
    sett = f.readlines()

for i,da in enumerate(sett):
    da = da.rstrip("\n")

for setting in sett:
    key = bkey.copy()
    key = set_key(key,setting)
    print(key)
    wdata = ittrr(key)
    # print(wdata)
    with open(files_path,"+a",encoding='utf-8') as f:
        f.writelines(wdata)
# key_toys_de = bkey.copy()
# key_toys_de["url"] = ittrr(key)
# key_toys_de["search_tags"].append("product-carousel")