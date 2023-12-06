import urllib.request
from itertools import count

def indata(txt):
    for i in range(txt.count(">")):
        if "</" in txt:
            txt = txt[txt.find(">")+1:]
            txt = txt[:txt.rfind("<")]
    return txt.replace("<br>","")

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
            print(indata(all[i]))
        if "item_description" in all[i]:
            # print("Explain")
            print(all[i+1].replace("      ","").replace("<br />",""))
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