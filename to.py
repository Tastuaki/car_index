import datetime
import urllib.request
from itertools import count

def indata(txt):
    t = ""
    ts = []
    txt = txt.strip()
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

def tomi_data(all):
    ser = []
    car = []
    nscar = []
    j = -1
    for i,data in enumerate(all):
        if "footMain01" in data:
            break
        elif "titles" in data:
            ser.append(indata(data).replace("シリーズ",""))
            j += 1
            car.append("")
            nscar.append("")
        elif "CarName" in data:
            if car[j] != "":
                car[j] += "/"
            if "<br>" in data:
                car[j] += indata(data.replace("<br>",""))+" "+indata(all[i+1])
            else:
                car[j] += indata(data)
        elif "mark-irekae" in data:
            if nscar[j] != "":
                nscar[j] += "/"
            nscar[j] += indata(data)
    return ser,car,nscar

burl="https://www.takaratomy.co.jp/products/tomica/new/"

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9), 'JST'))
day = now.strftime("%y%m")
hday = int(day)

for i in count(hday):
    try:
        all = urllib.request.urlopen(burl+str(i)+".htm").readlines()
    except urllib.error.URLError:
        i -= 1
        now = urllib.request.urlopen(burl+str(i-2)+".htm").readlines()
        oneaf = urllib.request.urlopen(burl+str(i-1)+".htm").readlines()
        break

for h in range(len(all)):
    all[h] = all[h].decode("utf-8")
for h in range(len(now)):
    now[h] = now[h].decode("utf-8")
for h in range(len(oneaf)):
    oneaf[h] = oneaf[h].decode("utf-8")

# with open("test.html","w+",encoding="UTF-8") as f:
#     f.writelines(all)

# print(all)
# exit()

aser = []
acar = []
anscar = []
aser,acar,anscar=tomi_data(all)
nser = []
ncar = []
nnscar = []
nser,ncar,nnscar=tomi_data(now)
oser = []
ocar = []
onscar = []
oser,ocar,onscar=tomi_data(oneaf)
print(i)
print(aser)
print(acar)
print(anscar)
print(i-1)
print(nser)
print(ncar)
print(nnscar)
print(i-2)
print(oser)
print(ocar)
print(onscar)
    # print(data)