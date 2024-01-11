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

burl="https://www.takaratomy.co.jp/products/tomica/new/"

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9), 'JST'))
day = now.strftime("%y%m")
hday = int(day)

for i in count(hday):
    try:
        all = urllib.request.urlopen(burl+str(i)+".htm").readlines()
    except urllib.error.URLError:
        break

for h in range(len(all)):
    all[h] = all[h].decode("utf-8")

# with open("test.html","w+",encoding="UTF-8") as f:
#     f.writelines(all)

# print(all)
# exit()
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
print(ser)
print(car)
print(nscar)
    # print(data)