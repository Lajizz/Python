from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import sqlite3

#正则表达式
findlink = re.compile(r'<a href="(.*?)">')
findimg = re.compile(r'src="(.*?)"')
findtitle = re.compile(r'class="title">(.*?)</span>')
findactor = re.compile(r'<p class="">(.*?)</p>',re.S)
findscore = re.compile(r'property="v:average">(.*?)</span>')
findpeople = re.compile(r'<span>(.*?)人评价</span>')
findsentence = re.compile(r'<span class="inq">(.*?)</span>',re.S)
def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 爬取网页
    datalist = getData(baseurl)
    # 解析数据
    # 保存数据
    path ="./豆瓣电影Top250.xls"
    saveData(datalist,path)


#某一网页内容
def askUrl(url):
    head = {}
    # 浏览器类型
    head["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def getData(baseurl):
    datalist = []

    for i in range(0,10):
        url = baseurl + str(i*25)
        html = askUrl(url)
        soup = BeautifulSoup(html, "html.parser")

        for item in soup.find_all('div', class_='item'):
            data = []
            item = str(item)
            link = re.findall(findlink, item)[0]
            data.append(link)
            img = re.findall(findimg, item)[0]
            data.append(img)
            title = re.findall(findtitle, item)[0]
            data.append(title)
            if len(re.findall(findtitle, item)) == 2:
                othertitle = re.findall(findtitle, item)[1]
            else:
                othertitle = ""
            data.append(othertitle)
            actor = re.findall(findactor, item)[0]
            actor = re.sub(r"<br(\s+)?>(\s+)?"," ",actor)
            actor = re.sub(r'/'," ",actor)
            data.append(actor.strip())
            score = re.findall(findscore, item)[0]
            data.append(score)
            people = re.findall(findpeople, item)[0]
            data.append(people)
            sentence = re.findall(findsentence, item)
            if len(sentence) != 0:
                sentence = re.findall(findsentence, item)[0]
                sentence = sentence.replace("。", "")
                sentence = sentence.replace(" ", "")
            else:
                sentence = ""
            data.append((sentence))
            datalist.append(data)
    return datalist


def saveData(datalist,path):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet("Good movies",cell_overwrite_ok=True)
    col =("电影链接", "图片", "中文名", "外国名", "详情", "评分", "人数", "简介")
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        print("第%d条" %(i+1))
        data = datalist[i]
        print(data)
        for j in range(0, 8):
            sheet.write(i+1, j, data[j])
    book.save("250movies.xls")

    print("finished...")

if __name__ == '__main__':
    main()

