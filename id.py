import urllib.request
from itertools import count
import html

def indata(txt):
    t = ""
    ts = []
    # print(txt)
    txt = txt.strip()
    for i in count():
        if txt == "":
            break
        elif "<" == txt[0]:
            txt = txt[txt.find(">")+1:]
            # print(txt)
        else:
            if ">" == txt[len(txt)-1]:
                txt = txt[:txt.rfind("</")]
                # print(txt) 
            else:
                if ">" in txt:
                    t,txt = txt.split("<",1)
                    txt = "<"+txt
                    ts.append(t)
                    continue
                else:
                    if len(ts) > 0:
                        ts.append(txt)
                    break
    # print(ts)
    if len(ts) > 1:
        txt = ""
        for t in ts:
            txt += t + "\n"
    return txt

q = True
while q:
    burl="https://muuseo.com/Tastuaki33/items/"

    print("Enter number(End -1) :",end="")
    arg = input()
    
    if arg == "-1":
        break
    elif not arg.isdecimal():
        print("URL Not Found")
        continue
    else:
        burl += arg

    try:
        all = urllib.request.urlopen(burl).readlines()
    except urllib.error.URLError:
        print("\""+burl+"\""+" Not Found")
        continue
    for h in range(len(all)):
        all[h] = all[h].decode("utf-8")
        # print(all[h])

    for i in count():
        if "h1" in all[i]:
            # print("Name")
            print(indata(html.unescape(all[i])))
        if "item_description" in all[i]:
            # print("Explain")
            print(all[i+1].replace("      ","").replace("<br />","\n"))
        if "msoItemInfoLabel" in all[i]:
            for j in count(i+1):
                if "title" in all[j]:
                    print(indata(all[j+1]),end=" : ")
                elif "info" in all[j]:
                    print(indata(all[j+1]))
                    break
        if "amazon_block" in all[i]:
            break
    print("\n")