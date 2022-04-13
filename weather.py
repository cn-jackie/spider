import requests
from lxml import etree
import pandas as pd

# 张嘉琦
# 学号：2019213161
# 班号：2019213105
# Web搜索技术
# 其中为-的数据为正常情况，目标网页中该部分的意思为：该时间段已经过去，不再展示预报信息

# url = 'http://www.weather.com.cn/textFC/hb.shtml'  # 483*2条数据
# url = 'http://www.weather.com.cn/textFC/db.shtml'  # 252*2条数据
# url = 'http://www.weather.com.cn/textFC/hd.shtml'  # 665*2条数据
# url = 'http://www.weather.com.cn/textFC/hz.shtml'  # 343*2条数据
# url = 'http://www.weather.com.cn/textFC/hn.shtml'  # 392*2条数据
# url = 'http://www.weather.com.cn/textFC/xb.shtml'  # 420*2条数据
# url = 'http://www.weather.com.cn/textFC/xn.shtml'  # 644*2条数据
# url = 'http://www.weather.com.cn/textFC/gat.shtml'  # 34*2条数据
urlList = ['http://www.weather.com.cn/textFC/hb.shtml', 'http://www.weather.com.cn/textFC/db.shtml',
           'http://www.weather.com.cn/textFC/hd.shtml', 'http://www.weather.com.cn/textFC/hz.shtml',
           'http://www.weather.com.cn/textFC/hn.shtml', 'http://www.weather.com.cn/textFC/xb.shtml',
           'http://www.weather.com.cn/textFC/xn.shtml', 'http://www.weather.com.cn/textFC/gat.shtml']

nameList = ['华北', '东北', '华东', '华中', '华南', '西北', '西南', '港澳台']


def printTest(listofvalue):
    print(len(listofvalue))
    print(listofvalue)


if __name__ == '__main__':
    rowCounter = 0
    for url in urlList:
        with requests.get(url) as res:
            content = res.content
            html = etree.HTML(content)

            dayContentList = []
            nightContentList = []

            location = html.xpath('//td[@width="83"]/a[@target="_blank"]/text()')
            dayContentList.append(location)
            nightContentList.append(location)

            weatherCondition = html.xpath('//td[@width="89"]/text()')
            # dayWeatherCondition = weatherCondition[:len(weatherCondition) // 2]
            # nightWeatherCondition = weatherCondition[len(weatherCondition) // 2:]
            dayContentList.append(weatherCondition)
            # dayContentList.append(dayWeatherCondition)
            # dayContentList.append(nightWeatherCondition)

            # windDirection = html.xpath('//td[@width="162"]/span/text()')
            # dayContentList.append(windDirection)

            dayWindPower = html.xpath('//td[@width="162"]/span[@class="conMidtabright"]/text()')
            dayContentList.append(dayWindPower)

            nightWindPower = html.xpath('//td[@width="162"]/span[@class="conMidtabright"]/text()')
            nightContentList.append(nightWindPower)

            highestTemperature = html.xpath('//td[@width="92"]/text()')
            dayContentList.append(highestTemperature)

            lowestTemperature = html.xpath('//td[@width="86"]/text()')
            nightContentList.append(lowestTemperature)

            try:
                while 1:
                    highestTemperature.remove('最高气温')
                    lowestTemperature.remove('最低气温')
                    weatherCondition.remove('天气现象')
            except:
                pass

            for item in dayContentList:
                printTest(item)

            dayDF = pd.DataFrame(
                {'地点': location, '最高温度': highestTemperature, '风力': dayWindPower})
            nightDF = pd.DataFrame(
                {'地点': location, '最低温度': lowestTemperature, '风力': nightWindPower})
            rowCounter += dayDF.shape[0]
            rowCounter += nightDF.shape[0]
            # print(dayDF)

            dayListDF = []
            nightListDF = []
            num = int(len(location) / 7)
            for i in range(0, 7):
                dayListDF.append(dayDF.iloc[i * num: num * (1 + i), :])
                nightListDF.append(nightDF.iloc[i * num: num * (1 + i), :])
                # print()
                # print()
                # print(str(i) + ' days after:')
                # print(dayListDF[i])
                # print(nightListDF[i])
                dayFileName = nameList[urlList.index(url)] + '地区' + str(i) + '日后白天天气情况.csv'
                nightFileName = nameList[urlList.index(url)] + '地区' + str(i) + '日后夜间天气情况.csv'
                dayListDF[i].to_csv(dayFileName, encoding="utf_8_sig")
                nightListDF[i].to_csv(nightFileName, encoding="utf_8_sig")

    print()
    print('一共包含数据' + str(rowCounter) + '条')
