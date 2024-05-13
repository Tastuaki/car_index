import os

# base = os.getcwd()
base = os.path.dirname(__file__)
files_path = base+"\\ts"
print(files_path)

with open(files_path,encoding='utf-8') as f:
    data = f.readlines()
    # print(data)

wdata = ["\n"]
df = False
ind = 0
lda = len(data)-1
for i,da in enumerate(data):
    da = da.rstrip("\n")
    # print(da)
    if "|" in da:
        m,d = da.split("|")
        wdata.append("            <br>"+m+"月"+d+"日"+"<br>"+"\n")
    elif "http" in da:
        url,name = data[i].split(" ",1)
        wdata.append('            <a class="model_link" href="'+url+'">'+name.rstrip("\n")+"</a>"+"\n")
        if i == lda:
            break
        elif "廃盤:" in data[i+1]:
            i += 1
            wdata.append("            <br>"+data[i].rstrip("\n")+"\n")
    elif "廃盤:" not in da:
        wdata.append("            <br>"+da+"<br>"+"\n")

with open(files_path,"+a",encoding='utf-8') as f:
    f.writelines(wdata)