import urllib.request
import sys
import os
from itertools import count

burl=""
if len(sys.argv) <= 1:
    print("URLがありません")
    exit()
else:
    burl = sys.argv[1]

body = []
exp = 0
try:
    os.mkdir("exchanged")
except FileExistsError:
    pass
finally:
        try:
            all = urllib.request.urlopen(burl).readlines()
            for h in range(len(all)):
                all[h] = all[h].decode("utf-8")
            for i in count():
                if "article_title" in all[i]:
                    title = all[i+1][all[i+1].find(">")+1:all[i+1].rfind("<")]
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
                if exp == 1:
                    exp = 0
                    bodyline = '<p class="car_explain">\n            '+ bodyline
                elif "<blockquote>" in bodybase:
                    bodyline = '<h3 class="header_txt" id="car_name_">'+bodyline+"</h3>"
                    exp = 1
                elif "</a>" in bodyline:
                    bodyline = bodyline[bodyline.find(">")+1:bodyline.rfind("<")]
                    url = all[k][all[k].find("href=")+6:all[k].find("rel")-2]
                    if bodyline != url:
                        bodyline = '<a class="car_link" href="'+url+'">'+bodyline+'</a><br>'
                    else:
                        bodyline = '<a class="car_link" href="'+url+'"></a><br>'
                elif 
                body.append(bodyline)
            with open(title+".html",'w+',encoding='utf-8') as ex:
                ex.write('<!DOCTYPE html>\n<html lang="ja" id="main_html">\n    <head>\n        <link rel="shortcut icon" href="https://raw.githubusercontent.com/Tastuaki/car_index/main/favicon.ico" type="image/vnd.microsoft.icon">\n        <link rel="stylesheet" href="https://tastuaki.github.io/car_index/car_index.css">\n    </head>\n    <body>\n        <header>\n            <h1 class="header_txt" id="main_title"></h1>\n        </header>\n        <div id="main">\n')
                for i in range(len(body)):
                    writeline = body[i].replace("	","")
                    if writeline != "":
                        ex.write("            "+writeline+"\n")
                ex.write('        </div>\n        <footer>\n            <a class="footer_link" href="https://tastuaki.github.io/car_index/index.html">ホーム</a>　\n            <a class="footer_link" href="https://tastuaki.github.io/car_index/brand/new.html">新製品カレンダー</a>\n            </footer>\n  </body>\n</html>\n')
            print("exchange "+ burl)
        except urllib.error.URLError:
            print("\""+burl+"\""+"Not Found")
            exit()