import os ,Image
j = 1
dir="./font/"
for f in os.listdir(dir):
    if f.endswith(".jpg"):
        img = Image.open(dir+f)
        img.crop((7, 5, 15, 16)).save("backup/%d.jpg" % j)
        j += 1
        img.crop((16, 5, 24, 16)).save("backup/%d.jpg" % j)
        j += 1
        img.crop((25, 5, 33, 16)).save("backup/%d.jpg" % j)
        j += 1
        img.crop((34, 5, 43, 16)).save("backup/%d.jpg" % j)
        j += 1
