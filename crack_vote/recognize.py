#!/usr/bin/env python
import os, Image

def binary(f):
    print f
    img = Image.open(f)
    img = img.convert("RGBA")
    pixdata = img.load()
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][1] < 136:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)
    return img
def division(img):
    nume = 1
    font=[]
    temp = img.crop((7, 5, 15, 16))
    temp.save("./temp/%d.jpg" % nume)
    font.append(temp)
    nume = nume + 1
    temp = img.crop((16, 5, 24, 16))
    temp.save("./temp/%d.jpg" % nume)
    font.append(temp)
    nume = nume + 1
    temp = img.crop((25, 5, 33, 16))
    temp.save("./temp/%d.jpg" % nume)
    font.append(temp)
    nume = nume + 1
    temp = img.crop((34, 5, 43, 16))
    temp.save("./temp/%d.jpg" % nume)
    font.append(temp)
    return font

def recognize(img):
    fontmap = []
    dir = "./fonts/"
    for f in os.listdir(dir):
        im = Image.open(dir+f)
        fontmap.append((int(os.path.splitext(f)[0]), im))
    #print(fontmap)
    result = ""
    thresh = 32
    font = division(img)
    for i in font:
        target = i
        points = []
        for mod in fontmap:
            diffs = 0
            for yi in range(11):
                for xi in range(8):
                    A = target.getpixel((xi, yi))
                    B = mod[1].getpixel((xi, yi))
                    if abs(A[0] - B[0]) > thresh:
                        diffs += 1
                    else:
                        if abs(A[1] - B[1]) > thresh:
                            diffs += 1
                        else:
                            if abs(A[2] - B[2]) > thresh:
                                diffs += 1

            #print diffs, mod[0]
            points.append((diffs, mod[0]))
        points.sort()
        C = []
        cnt = 0
        ret = 0
        for k in points:
            if k[0] == points[0][0]:
                C.append(k[1])
        print C
        for k in C:
            if C.count(k) > cnt:
                cnt = C.count(k)
                ret = k
        result += str(ret)
    return result

if __name__ == '__main__':
    print recognize(binary("test.jpg"))
