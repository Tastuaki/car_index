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
                if txt.rfind("</") != -1:
                    txt = txt[:txt.rfind("</")]
                elif txt[len(txt)-4:len(txt)] == "<br>":
                    txt = txt[:txt.rfind("<br>")]
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
    date = []
    atxt = ""
    datetx=""
    j = -1
    fsday = False
    sday = 0
    # print(all)
    for i,data in enumerate(all):
        if "footMain01" in data:
            break
        elif "titles" in data:
            ser.append(indata(data).replace("シリーズ",""))
            j += 1
            car.append("")
            nscar.append("")
            date.append("")
        elif "CarName" in data:
            atxt = ""
            if car[j] != "":
                car[j] += "/"
            if "<br>" in data:
                x = i+1
                while "<p" not in all[x]:
                    atxt += " "+indata(all[x])
                    x += 1
                car[j] += indata(data.replace("<br>",""))+atxt
            else:
                car[j] += indata(data)
        elif "CarPrice" in data:
            datetx = indata(data[data.find("年")+1:data.find("発売予定")])
            mon,day = datetx.split("月",1)
            if fsday == False:
                bday = 1
                d = datetime.date(int(data[data.find(">")+1:data.find("年")]),int(mon),bday).weekday()
                if d != 5:
                    if d == 6:
                        bday = 7
                    else:
                        while d != 5:
                            d += 1
                            bday += 1
                sday = bday + 14
                sday = str(sday)
                fsday = True
            if day != "":
                date[j] = mon + "|" + day[:day.find("日")]
            else:
                date[j] = mon + "|" + sday
        elif "mark-irekae" in data:
            if nscar[j] != "":
                nscar[j] += "/"
            nscar[j] += indata(data)
    return ser,car,nscar,date

def yover(y):
    if (y % 100) == 0:
        y = (y-100)+12
    elif (y % 100) == 99:
        y = (y-100)+11
    return y

burl="https://www.takaratomy.co.jp/products/tomica/new/"

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9), 'JST'))
day = now.strftime("%y%m")
hday = int(day)
hday = 2501

for i in count(hday):
    try:
        all = urllib.request.urlopen(burl+str(i)+".htm").readlines()
    except urllib.error.URLError:
        i -= 1
        oneaf = urllib.request.urlopen(burl+str(yover(i-1))+".htm").readlines()
        now = urllib.request.urlopen(burl+str(yover(i-2))+".htm").readlines()
        break

for h in range(len(all)):
    all[h] = all[h].decode("utf-8")

aser = []
acar = []
anscar = []
adate = []
aser,acar,anscar,adate=tomi_data(all)
for h in range(len(now)):
    now[h] = now[h].decode("utf-8")
for h in range(len(oneaf)):
    oneaf[h] = oneaf[h].decode("utf-8")

nser = []
ncar = []
nnscar = []
ndate = []
nser,ncar,nnscar,ndate=tomi_data(now)
oser = []
ocar = []
onscar = []
odate = []
oser,ocar,onscar,odate=tomi_data(oneaf)

oadate = ""
for ix,x in enumerate(aser):
    if adate[ix] != oadate:
        print(adate[ix])
        oadate = adate[ix]
    print(x)
    print(burl+str(yover(i))+".htm")
    print(acar[ix])
    if anscar[ix] != "":
        print("廃盤:"+anscar[ix])
oodate = ""
for ix,x in enumerate(oser):
    if odate[ix] != oodate:
        print(odate[ix])
        oodate = odate[ix]
    print(x)
    print(burl+str(yover(i-1))+".htm")
    print(ocar[ix])
    if onscar[ix] != "":
        print("廃盤:"+onscar[ix])
ondate = ""
for ix,x in enumerate(nser):
    if ndate[ix] != ondate:
        print(ndate[ix])
        ondate = ndate[ix]
    print(x)
    print(burl+str(yover(i-2))+".htm")
    print(ncar[ix])
    if nnscar[ix] != "":
        print("廃盤:"+nnscar[ix])

    # print(data)