import requests, random, re, time
from lxml import etree


def spyder():
    mask = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"]
    url = "https://web.okjike.com/u/wenhao1996"
    headers = {'User-agent': random.choice(mask)}

    Html = requests.get(url,headers=headers).text
    eHTML = etree.HTML(Html)
    WebUrl = eHTML.xpath('/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/div/article/div[2]/div[2]/div/div/a')
    for index in range(len(WebUrl)):
        Url = WebUrl[index].attrib['href']      # 获取今日新闻链接
    Html = requests.get(Url,headers=headers).text
    eHTML = etree.HTML(Html)
    Time = eHTML.xpath('/html/head/title/text()')
    Time = Time[0]
    WebUrl = eHTML.xpath('.//li[@class="item"]/a')
    mUrl = []
    for index in range(len(WebUrl)):
        Url = WebUrl[index].attrib['href']      # 获取详细新闻链接
        Url = re.sub('https://', '', Url)
        mUrl.append(Url)
    # mNum = eHTML.xpath('.//span[@class="num"]/text()')
    mText = eHTML.xpath('.//span[@class="text"]/text()')
    NewsString = Time + '世界上发生了什么：\n'
    for i in range(len(mUrl)):
        text = str(i+1) + '. ' + mText[i] + '\n' + mUrl[i] + '\n'
        NewsString += text
    NewsString += '信息来源即刻资讯台：https://web.okjike.com/u/wenhao1996\n'
    return NewsString


def weather():
    WeatherString = '\n' + '济南每日天气预报：\n'
    weather = requests.get('https://devapi.qweather.com/v7/weather/now?location=101120101&key=0ff640e9311c4b92b733e2d8c12765c6')  # 济南实时天气
    weather = weather.json()['now'] # 天气信息
    wTime = weather['obsTime']
    wTime = re.sub('T', ' ', wTime)
    wTime = '更新时间：' + re.sub('\+08:00', '', wTime) + '\n'  # 观测时间
    WeatherString += wTime
    wTemp = '气温：' + weather['temp'] + '℃' + '\t'  # 温度
    wFeelsLike = '体感温度：' + weather['feelsLike'] + '℃' + '\n'  # 体感温度
    wText = '天气：' + weather['text'] + '\n'  # 天气文字描述
    wWindDir = '风向：' + weather['windDir'] + '\t'  # 风向
    wWindScale = '风力等级：' + weather['windScale'] + '\n'  # 风力等级
    wVis = '能见度：' + weather['vis'] + '\n'   # 能见度
    wString = [wTemp, wFeelsLike, wText, wWindDir, wWindDir, wWindScale, wVis]
    for key in wString:
        WeatherString += key

    text = requests.get('https://devapi.qweather.com/v7/indices/1d?type=1,3,7,8,9&location=101120101&key=0ff640e9311c4b92b733e2d8c12765c6')
    text = text.json()
    daily = text['daily']
    for i in range(len(daily)):
        WeatherString += daily[i]['name'] + '：' + daily[i]['category'] + '\n' + daily[i]['text'] + '\n'
    return WeatherString


def post(String):
    PostUrl = 'https://push.xuthus.cc/group/69497f37b8bc93f90facedb92841f4bf?sendList=585097341,698150236'
    requests.post(PostUrl, data=String.encode())


if __name__ == '__main__':
    jkNws = spyder()
    Weather = weather()
    String = jkNws+Weather
    post(String)
    time.sleep(120)
    requests.post('https://push.xuthus.cc/group/69497f37b8bc93f90facedb92841f4bf?sendList=823625227', data=jkNws.encode())
    print('OK!')
