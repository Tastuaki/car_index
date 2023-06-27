import urllib.request
import requests
import sys
import os
from itertools import count

def listrfind(list,target):
    for i in range(len(list)-1,-1,-1):
        if target in list[i]:
            return i

def itemname(url):
    itemdata = []
    text = ""
    try:
        itemdata = urllib.request.urlopen(url).readlines()
        len_item = len(itemdata)
    except:
        print("\""+url+"\""+" Not Found")
        return ""
    for k in range(len_item):
        itemdata[k] = itemdata[k].decode("utf-8")
        # print(itemdata[k],end="")
        if "title_block" in itemdata[k]:
            itemdata[k+1] = itemdata[k+1].decode("utf-8")
            exb = itemdata[k+1].rfind("(")
            if exb != -1:
                return itemdata[k+1][exb+1:itemdata[k+1].rfind(")")]
            else:
                text = itemdata[k+1][itemdata[k+1].find(">")+1:itemdata[k+1].rfind("<")]
                return text[text.find("　")+1:]
    return ""

burl=""
if len(sys.argv) <= 1:
    print("URLがありません")
    exit()
else:
    burl = "https://muuseo.com/Tastuaki33/diaries/"+sys.argv[1]

body = []
exp = False
gen = False
tan = ""
exbegin = 0
brand = ["トミカ","ホットウィール","マジョレット","チョロＱ","ディーラー","京商","コーヒーのおまけ","マッチボックス","ウェリー","RMZ","マイスト","グリーンライト"]
brandsum=len(brand)
# try:
#     os.mkdir("exchanged")
# except FileExistsError:
#     pass
# finally:
try:
    all = urllib.request.urlopen(burl).readlines()
except urllib.error.URLError:
    print("\""+burl+"\""+"Not Found")
    exit()
for h in range(len(all)):
    all[h] = all[h].decode("utf-8")
for i in count():
    if "article_title" in all[i]:
        title = all[i+1][all[i+1].find(">")+1:all[i+1].rfind("<")]
        titletext='            <h1 class="header_txt" id="main_title">'+title+'</h1>\n        </header>\n        <div id="main">\n'
        if "/" in title:
            title = title.replace("/","_")
    elif "lab_article_body" in all[i]:
        body_begin = i
        for j in count(i):
            if "</div>" in all[j]:
                body_end = j
                break
        break
for k in range(body_begin+1,body_end):
    bodybase = all[k]
    bodyline = all[k][all[k].find(">")+1:all[k].rfind("<")]
    if gen:
        gen = False
        body.append(tan)
        tan = ""
    if "</a>" in bodyline:
        bodyline = bodyline[bodyline.find(">")+1:bodyline.rfind("<")]
        url = all[k][all[k].find("href=")+6:all[k].find("rel")-2]

        if bodyline != url:
            bodyline = '<a class="car_link" href="'+url+'">'+bodyline+'</a><br>'
        elif "item" not in url:
            bodyline = '<a class="car_link" href=""></a><br>'
        else:
            bodyline = '<a class="car_link" href="'+url+'">'+itemname(url)+'</a><br>'
    elif exp:
        exp = False
        if "。" in bodyline:
            tan = bodyline
            bodyline = '<p class="car_explain">'
            gen = True
        # else:
        #     gen = bodyline
        #     # bodyline = '<p class="car_explain">\n'
        #     # body.append(bodyline)
        #     bodyline = gen
        #     # print(bodyline,end="|\n")
    elif "<blockquote>" in bodybase:
        if "代" in bodyline:
            bodyline = '<b>'+bodyline+'</b>'
        else:
            bodyline = '<h3 class="header_txt" id="car_name_">'+bodyline+"</h3>"
            exp = 1
    elif "<br>" in bodyline:
        bodyline = "</p>"
    else:
        for i in range(brandsum):
            if brand[i] in bodyline:
                bodyline = '<p class="brand">'+bodyline+'</p>'
                break
    body.append(bodyline)
    if "<b>" in bodyline:
        endbody = len(body)-1
        newbody = body[endbody]
        if "car_explain" not in newbody:
            body[endbody] = '<p class="car_explain">'
            body.append(newbody)
    elif "</p>" == bodyline:
        endbody = len(body)
        exbegin = listrfind(body,"car_explain")
        for j in range(exbegin+1,endbody-1):
            body[j] = "    "+body[j]+"<br>"
with open(title+".html",'w+',encoding='utf-8') as ex:
    ex.write('<!DOCTYPE html>\n<html lang="ja" id="main_html">\n    <head>\n        <link rel="shortcut icon" href="https://raw.githubusercontent.com/Tastuaki/car_index/main/favicon.ico" type="image/vnd.microsoft.icon">\n        <link rel="stylesheet" href="https://tastuaki.github.io/car_index/car_index.css">\n    </head>\n    <body>\n        <header>\n'+titletext)
    for i in range(len(body)):
        writeline = body[i].replace("	","")
        if writeline != "":
            ex.write("            "+writeline+"\n")
    ex.write('        </div>\n        <footer>\n            <a class="footer_link" href="https://tastuaki.github.io/car_index/index.html">ホーム</a>　\n            <a class="footer_link" href="https://tastuaki.github.io/car_index/brand/new.html">新製品カレンダー</a>\n            </footer>\n  </body>\n</html>\n')
print("exchange "+ burl+":"+title)