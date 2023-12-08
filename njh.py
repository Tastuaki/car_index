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

def listotx(data):
    pdata = ""
    sdata = []
    for d in data:
        # print(list(d))
        if d != "\n":
            pdata += d.replace("\t"," ") + "\t"
            # print(pdata)
        else:
            sdata.append(pdata)
            pdata = ""
    return sdata

burl="https://hotwheels.fandom.com/wiki/List_of_2021_Hot_Wheels"

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
            if "Exclusive" in s:
                edata.append(sdata[i].replace("\n\t","\t").replace("\n","|"))
                sdata.pop(i)
            sdata[i] = sdata[i].replace("\n\t","\t").replace("\n","|")
            
target = []
walmart = []
kroger = []
dollar = []
etc = []

be = "                <tr><td>"
af = "</td></tr>"
for i,s in enumerate(edata):
    # print(s.split("\t"))
    mn,no,name,seg,segno=s.split("\t",4)
    name = name[:name.rfind(" (")]
    segno = segno[:segno.rfind("/")]
    seg,exv=seg.split("|",1)
    etxt = name+"\t"
    if "Target" in exv:
        etxt = etxt.replace("\t","</td><td>")
        etxt = be+etxt+segno+af
        target.append(etxt)
    else:
        etxt += seg+"\t"+segno
        etxt = etxt.replace("\t","</td><td>")
        etxt = be+etxt+af
        if "Walmart" in exv:
            walmart.append(etxt)
        elif "Kroger" in exv:
            kroger.append(etxt)
        elif "Dollar" in exv:
            dollar.append(etxt)
        else:
            etxt = etxt[len(be):len(etxt)-(len(af))]
            etxt = etxt+"\t"+exv
            etxt = etxt.replace("\t","</td><td>")
            etxt = be+etxt+af
            etc.append(etxt)
            print(exv)

with open("ex","w+",encoding="utf-8") as f:
    f.writelines([d+"\n" for d in sdata])
    f.write("-----Exclusive------\ntarget\n")
    f.writelines([d+"\n" for d in target])
    f.write("walmart\n")
    f.writelines([d+"\n" for d in walmart])
    f.write("kroger\n")
    f.writelines([d+"\n" for d in kroger])
    f.write("Dollar General\n")
    f.writelines([d+"\n" for d in dollar])
    f.write("etc\n")
    f.writelines([d+"\n" for d in etc])