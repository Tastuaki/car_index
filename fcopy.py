import os
import glob

def mfile(fname,e=False):
    try:
        os.mkdir(fname)
        if e:
            print("make "+fname)
        return True
    except FileExistsError:
        if e:
            print("\nError! \""+fname+"\" is already exist")
            # print("\nPress any key...",end="")
            # input()
            # exit()
            return False
        return True

base = ""
while base == "":
    print("input folder name: ",end="")
    base = input()

if ":" not in base:
    base = os.path.dirname(__file__)+"\\"+base

if not os.path.exists(base):
    print("folder not found")
    print("\nFinish! Press any Key...",end="")
    input()
    exit()

tree = glob.glob('**/', recursive=True,root_dir=base)

num = 2
bbase,bfolder = base.rsplit("\\",1)
bbase += "\\"
nes = True
while nes:
    defname = bfolder + "_" + str(num)
    if not os.path.exists(bbase+defname):
        nes = False
    num += 1

nes = True
while nes:
    print("copy folder name (default:"+defname+"): ",end="")
    rn = input()

    if rn != "":
        cfolname = rn
        if not os.path.exists(bbase+cfolname):
            nes = False
        else:
            print("\""+cfolname+"\" is already exist\n")
            continue
    else:
        cfolname = defname
        nes = False

cfolname += "\\"

bbase += cfolname
mfile(bbase)
for tif in tree:
    # print(bbase+tif)
    mfile(bbase+tif)

print("copy folder: "+bfolder+" → "+cfolname.rstrip("\\"))
print("\nFinish! Press any Key...",end="")
input()