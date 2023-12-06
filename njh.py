import urllib.request
from itertools import count

def indata(txt):
    t = ""
    ts = []
    txt = txt.replace("\n","")
    # print(txt)
    for i in count():
        if "<" == txt[0]:
            txt = txt[txt.find(">")+1:]
            # print(txt)
        else:
            if ">" == txt[len(txt)-1]:
                txt = txt[:txt.rfind("</")]
                # print(txt) 
            else:
                if "</" in txt:
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

def listotx(data):
    pdata = ""
    sdata = []
    for d in data:
        if d != "\n":
            pdata += d.replace("\t"," ") + "\t"
            # print(pdata)
        else:
            sdata.append(pdata)
            pdata = ""
    return sdata

burl="https://hotwheels.fandom.com/wiki/List_of_2022_Hot_Wheels"

try:
    all = urllib.request.urlopen(burl).readlines()
except urllib.error.URLError:
    print("\""+burl+"\""+" Not Found")
for h in range(len(all)):
    all[h] = all[h].decode("utf-8")
    # print(all[h])

data = []
edata = []
d = ""
ed = False
for i in count():
    if "sortable" in all[i]:
        for j in count(i+1):
            if "<tr>\n" == all[j]:
                for k in count(j+1):
                    if "</td>" in all[k]:
                        pass
                    elif "/images/" not in all[k]:
                        data.append(indata(all[k]))
                    if "</tr>" in all[k]:
                        data.append("\n")
                        break
            elif "</table>" in all[j]:
                e = True
                break
        if e:
            break

sdata = listotx(data)

edata = []
for i,s in enumerate(sdata):
    if "\n" in s:
        sdata[i] = s.replace("\n ("," (")
        if "\n" in sdata[i]:
            sdata[i] = sdata[i].replace("\n\t","\t").replace("\n","-")
            if "Exclusive" in s:
                edata.append(sdata[i])

with open("ex","w+",encoding="utf-8") as f:
    f.writelines([d+"\n" for d in sdata])
    f.write("-----Exclusive------\n")
    f.writelines([d+"\n" for d in edata])