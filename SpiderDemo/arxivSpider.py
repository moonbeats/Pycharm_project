# -*- coding:utf-8 -*-
import re  # 正则表达式，进行文字匹配
import requests
import urllib.error  # 指定url，获取网页数据
import urllib.request
import xlwt  # 进行excel操作
from bs4 import BeautifulSoup  # 网页解析，获取数据


def main():
    baseurl = "https://arxiv.org/search/?query=intelligent+reflecting+surface+mmWave&searchtype=all&source=header"
    html = askURL(baseurl)
    fileurllist, filenamelist = getfileURL(html)
    downLoadPDFfile(fileurllist, filenamelist)
    print("Mission Finished!")

# 1 得到指定URL的网页内容
def askURL(url):
    # 用户代理伪装爬虫
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    print("successfully ask target url!")
    return html
# 2 解析网页得到 fileurl下载池
findURLlink = re.compile(r'<a href="(.*?)">')  #匹配文章链接
findPaperTitle = re.compile(r'<p class="title is-5 mathjax">(.*?)</p>', re.S) #匹配文章标题

def getfileURL(html):
    fileurllist = []
    filenamelist = []
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.find_all('li', class_="arxiv-result"):
        item = str(item)
        link = re.findall(findURLlink, item)[0]
        link = re.sub('abs', 'pdf', link)
        fileurllist.append(link)

        name = re.findall(findPaperTitle, item)[0]
        name = re.sub('<span (.*?)>', '', name)
        name = re.sub('</span>', '', name)
        name = re.sub(':', ' ', name)
        name = re.sub(r'\n', '', name)
        name = re.sub(r'\s+', ' ', name)

        filenamelist.append(name)

    print(fileurllist)
    print(filenamelist)
    if(len(filenamelist) != len(fileurllist)):
        print("Unequal length, matching error！")
    return fileurllist, filenamelist




#3 下载文件pdf
def downLoadPDFfile(fileurllist,filenamelist):

    for i in range(0, len(fileurllist)):
        fileurl = fileurllist[i]
        filename = filenamelist[i]
        path = "./mmWaveIRS/arxiv%d_%s.pdf"%(i+1, filename)
        r = requests.get(fileurl, stream=True)
        with open(path, "wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)


        print("downloading NO %d paper....." %(i+1))


if __name__ == "__main__":
    main()
