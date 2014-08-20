#!/usr/bin/env python
import os, Image
import urllib2, cookielib
from random import randint
from time import sleep
import socket
from httplib import BadStatusLine
def binary(f):
    #print f
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
    #this is important!!!
    temp = img.crop((7, 5, 15, 16))
    #temp.save("./temp/%d.jpg" % nume)
    font.append(temp)
    nume = nume + 1
    temp = img.crop((16, 5, 24, 16))
    #temp.save("./temp/%d.jpg" % nume)
    font.append(temp)
    nume = nume + 1
    temp = img.crop((25, 5, 33, 16))
    #temp.save("./temp/%d.jpg" % nume)
    font.append(temp)
    nume = nume + 1
    temp = img.crop((34, 5, 43, 16))
    #temp.save("./temp/%d.jpg" % nume)
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

def do_vote():
    #random sleep make sense
    sleep(randint(10, 15))
    vote_url = "your site url"
    code_img = "your code url"
    submit_url_pre = "your site url"
    submit_url_post = "your site url"
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    #bad 
    proxys = ['122.96.59.99:81', 
    '114.112.69.21:81',
    '202.108.50.75:80',
    '122.96.59.106:81',
    '116.228.55.217:8000',
    '111.161.126.84:80']
    Rproxy = randint(0, len(proxys) - 1)
    print proxys[Rproxy]
    #use proxy to make it more safe(from being awared.)
    proxy = urllib2.ProxyHandler({'http': proxys[Rproxy]})
    opener = urllib2.build_opener(proxy, handler)
    
    #fake user agent
    UAs = [
    r"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13", 
    r"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14", 
    r"Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8",
    r"Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/85.8",
    r"Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"]
    Rua = randint(0, len(UAs) - 1)
    print UAs[Rua]
    opener.addheaders = [('User-agent', UAs[Rua])]
    urllib2.install_opener(opener)
    try: 
        urllib2.urlopen(vote_url)
    except urllib2.HTTPError, e:
        print e.code
        return 0
    except urllib2.URLError, e:
        print e.args
        return 0
    except BadStatusLine, e:
        print "BadStatusLine"
        return 0
    except socket.error, e:
        print "socket.error"
        return 0
    print cookie

    try:
        res = urllib2.urlopen(code_img)
        img = open("test.jpg", "wb")
        img.write(res.read())
        img.close()
    except urllib2.HTTPError, e:
        print e.code
        return 0
    except urllib2.URLError, e:
        print e.args
        return 0
    except BadStatusLine, e:
        print "BadStatusLine"
        return 0
    except socket.error, e:
        print "socket.error"
        return 0
    
    code = recognize(binary("test.jpg"))
    print code
    submit_url = submit_url_pre + code + submit_url_post

    try:
        response = urllib2.urlopen(submit_url)
        print response.geturl(), response.info()
    except urllib2.HTTPError, e:
        print e.code
        return 0
    except urllib2.URLError, e:
        print e.args
        return 0
    except BadStatusLine, e:
        print "BadStatusLine"
        return 0
    except socket.error, e:
        print "socket.error"
        return 0

if __name__ == '__main__':
    T = 10000
    while T > 0:
        print T
        do_vote()
        T = T - 1
        print ""
