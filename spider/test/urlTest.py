import urllib.request
# response = urllib.request.urlopen("http://www.baidu.com")
# print(response.read().decode('utf-8'))

#post
import urllib.parse
# data = bytes(urllib.parse.urlencode({"hello":"world"}),encoding="utf-8")
# response = urllib.request.urlopen("http://httpbin.org/post",data = data)
# print(response.read().decode("utf-8"))

# try:
#     response = urllib.request.urlopen("http://httpbin.org/get",timeout=0.01)
#     print(response.read().decode("utf-8"))
# except urllib.error.URLError as e:
#     print("time out!")

# response = urllib.request.urlopen("http://www.baidu.com")
# print(response.status)
# print(response.getheaders())
# print(response.getheader("Server"))

# url = "http://httpbin.org/post"
# headers = {
# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
# }
# data = bytes(urllib.parse.urlencode({'name':"eric"}),encoding="utf-8")
# req = urllib.request.Request(url=url,data=data,headers=headers,method="POST")
# response = urllib.request.urlopen(req)
# print(response.read().decode("utf-8"))

from bs4 import BeautifulSoup
import re
findlink = re.compile(r'<a href="(.*?)">')
findimg = re.compile(r'src="(.*?)"')
findtitle = re.compile(r'class="title">(.*?)</span>')
findactor = re.compile(r'<p class="">(.*?)</p>',re.S)
findscore = re.compile(r'property="v:average">(.*?)</span>')
findpeople = re.compile(r'<span>(.*?)人评价</span>')
findsentence = re.compile(r'<span class="inq">(.*?)</span>',re.S)
url = baseurl = "https://movie.douban.com/top250?start="
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
}
req = urllib.request.Request(url=url,headers=headers)
response = urllib.request.urlopen(req)
html = response.read().decode("utf-8")
soup = BeautifulSoup(html,"html.parser")
for item in soup.find_all('div',class_="item"):
    data=[]
    item = str(item)
    link = re.findall(findlink,item)[0]
    data.append(link)
    img = re.findall(findimg,item)[0]
    data.append(img)
    title = re.findall(findtitle,item)[0]
    data.append(title)
    if len(re.findall(findtitle,item))==2:
        othertitle = re.findall(findtitle,item)[1]
    else:
        othertitle = ""
    data.append(othertitle)
    actor = re.findall(findactor,item)[0]
    data.append(actor)
    score = re.findall(findscore,item)[0]
    data.append(score)
    people = re.findall(findpeople,item)[0]
    data.append(people)
    sentence = re.findall(findsentence,item)[0]
    sentence=sentence.replace("。","")
    sentence = sentence.replace(" ", "")
    data.append((sentence))
    print(data)
    print("====================")