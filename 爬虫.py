# coding=utf-8
#https://movie.douban.com/top250
#此程序需安装re bs4 urllib xlwt sqlite3 sys 数据库 若没有请自行安装。


import sys
from bs4 import BeautifulSoup    #网页解析
import re     #正则表达
import urllib.error,urllib.request   #制定url
import xlwt    #excel操作
import sqlite3 #sqlite数据库操作

def main():
    baseurl = "https://movie.douban.com/top250?start="
    #获取网页
    datalist = getdata(baseurl)
    savepath = ".\\豆瓣电影top250.xls"
    # 保存数据
    savedata(datalist,savepath)
    #askurl("https://movie.douban.com/top250?start=")

#规则
findlink = re.compile(r'<a href="(.*?)">')#生成正则表达式对象
findimgsrc = re.compile(r'<img.*src="(.*?)"',re.S)
findname = re.compile(r'<span class="title">(.*)</span>')
findrating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findjudge = re.compile(r'<span>(\d*)人评价</span>')
findinq = re.compile(r'<span class="inq">(.*)</span>')
findbd = re.compile(r'<p class="">(.*?)</p>',re.S)




# 爬取
def getdata(baseurl):
    datalist = []
    for i in range(0,10):
        url = baseurl + str(i*25)  #调用获取信息页面10次
        html = askurl(url)     #保存获取的网页源码
        #解析
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all("div",class_="item"):   #查找符合要求的字符串
        #print(item)
            data = []
            item = str(item)
            link = re.findall(findlink,item)[0]  #通过正则表达查找
            data.append(link)
            imgsrc = re.findall(findimgsrc,item)[0]
            data.append(imgsrc)
            titles = re.findall(findname, item)
            if(len(titles)==2):
                ctitles = titles[0]
                data.append(ctitles)
                otitles = titles[1].replace("/","")
                data.append(otitles)
            else:
                data.append(titles[0])
                data.append(' ') #没有就留空
            rating = re.findall(findrating, item)[0]
            data.append(rating)
            judge = re.findall(findjudge,item)[0]
            data.append(judge)
            inq = re.findall(findinq,item)
            if len(inq)!=0:
                inq = inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")
            bd = re.findall(findbd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)
            bd = re.sub('/'," ",bd)
            data.append(bd.strip())
            datalist.append(data) # 分析
    return datalist
# 得到一个url网页信息
def askurl(url):
    head = {        #模拟浏览器头部信息
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/100.0.4896.127Safari/537.36Edg/100.0.1185.50"
    }
# 用户代理告诉网页什么类型的机器，告诉浏览器接受文件水平
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        responce = urllib.request.urlopen(request)
        html = responce.read().decode("utf-8")
    except urllib.error.URLError as e :
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html

# 保存数据
def savedata(datalist,savepath):
     book = xlwt.Workbook(encoding="utf-8",style_compression=0)
     sheet = book.add_sheet("豆瓣电影top250",cell_overwrite_ok=True)
     col = ("电影详情链接","图片链接","中文名","外国名","评分","评价数","概况","相关信息")
     for i in range(0, 8):
        sheet.write(0, i, col[i])
     for i in range(0, 250):
         print("第%d条" % (i + 1))
         data_2 = datalist [i]
         for j in range(0, 8):
             sheet.write(i + 1, j, data_2[j])
     book.save(savepath)

if __name__ == "__main__":  #当程序执行时
    main()                       #调用函数
    print("爬取完毕")
