import os
import shutil

base = os.path.dirname(__file__) + "\\"

# with open(base+"ti","w+",encoding="utf-8") as f:
#     data = f.readlines()

def mfile(fname,end=False):
    e = ""
    try:
        fname = base +fname
        # print(fname)
        os.mkdir(fname)
        if end:
            print("\nmake "+fname)
        return True
    except FileExistsError:
        if end:
            print("\nError! \""+fname+"\" is already exist")
        return False

# for d in data:
bname = ""
while True:
    print("input file name:",end="")
    bname = input()

    if bname == "-1":
        break

    fname = ""
    for f in bname.split("|"):
        fname += f + "\\"
        e = mfile(fname)
    
    if e:
        print("make " + fname)
        with open(base+fname+"a","w+") as f:
            f.write("")
    else:
        print("already exist "+fname)

print("\nFinish! Press any Key...",end="")
input()