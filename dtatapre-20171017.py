# -*- coding: UTF-8 -*-
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import json
#将时间参数从list格式转为数字量
def taketime_data(timelist):
    #numbers = map(int, numbers)-python2.x
    #numbers = list(map(int, numbers))-python3.x
    #目前数据均为2017年，所以不用记录年份
    #Date_year = map(int,timelist[0])[0]*1000+ map(int,timelist[1])[0]*100+map(int,timelist[2])[0]*10+map(int,timelist[3])[0]
    Date_month =  map(int,timelist[5])[0]*10+ map(int,timelist[6])[0]
    Date_day=  map(int,timelist[8])[0]*10+ map(int,timelist[9])[0]
    Date_hour= map(float,timelist[11])[0]*10+ map(float,timelist[12])[0]
    Date_minute= map(float,timelist[14])[0]*10+ map(float,timelist[15])[0]
    #表示在2017年的具体日期，前两位表示月份后两位表示所在月份的日期
    Date_monthtime_int=Date_month*100+Date_day
    #当天的具体时间，精确到分钟
    Date_daytime_float=Date_hour+Date_minute/60
    #当天的具体时间，精确到小时
    Date_daytime_int=int(Date_hour)
    #Date_seconed=map(int,timelist[17])[0]*10+ map(int,timelist[18])[0]
    #int_time_list=[Date_year,Date_monthtime,Date_daytime_float,Date_daytime_int]
    int_time_list=[Date_monthtime_int,Date_daytime_int,Date_daytime_float]
    return int_time_list
#对每小时统计次数进行分级评价处理函数
def defineRank(conutTimes):
    #将需求热度分为5个等级，0-3为最低，大于24则为最高高需求
    if   conutTimes<=3 and conutTimes>=0:
        return 0
    elif conutTimes>3 and conutTimes<=9:
        return 1
    elif conutTimes>9 and conutTimes<=15:
        return 2
    elif conutTimes>15 and conutTimes<=24:
        return 3
    else:
        return 4
#antinghuiParkingPlace文件数据开始时间为2017年4月2日（星期日）,从json文件中提取数据
with open('E:\\deeplearnning\\ex-date\\eachshop\\antinghuiParkingPlace.json','r') as jsonF:
    data_json=json.load(jsonF)
#print "outOrderList:\n"
#取还车日期记录列表
outStartTime=[]
inStartTime=[]
#网点取车时间记录字典,从2017.4.02开始
outOrderList={}
#网点还车时间记录字典，从2017.4.02开始
inOrderList={}
for i in range(len(data_json['outOrderList'])):
    list1=taketime_data(data_json['outOrderList'][i]['outDate'])
    if list1[0] in outStartTime:
        outOrderList[list1[0]].append(list1[1])
    else:
        outStartTime.append(list1[0])
        outOrderList[list1[0]]=[list1[1]]
for i in range(len(data_json['inOrderList'])):
    list1=taketime_data(data_json['inOrderList'][i]['inDate'])
    if list1[0] in inStartTime:
        inOrderList[list1[0]].append(list1[1])
    else:
        inStartTime.append(list1[0])
        inOrderList[list1[0]]=[list1[1]]
#创建取车日期表
outOrderTimeList=sorted(outOrderList.keys())
#创建还车日期表
inOrderTimeList =sorted(inOrderList.keys())
#将一天时间按照小时来分割，从0到23
Y_dailyTime=np.arange(0,24,1)
X_outOrderTimeList=np.arange(1,len(outOrderTimeList)+1,1)
X_inOrderTimeList=np.arange(1,len(inOrderTimeList)+1,1)
#X_outOrderTimeList=np.array(outOrderTimeList)
#统计每天每小时的取车次数
outCardailyCountList=[]
for outTime in outOrderTimeList:
    countlist=[]
    for outhour in range(0,24):
        countlist.append(outOrderList[outTime].count(outhour))
    outCardailyCountList.extend(countlist)
Z_outdailyCountArray=np.array(outCardailyCountList).reshape(len(outOrderTimeList),24)
#统计每天还车每小时次数
inCardailyCountList=[]
for inTime in inOrderTimeList:
    countlist=[]
    for inhour in range(0,24):
        countlist.append(inOrderList[inTime].count(inhour))
    inCardailyCountList.extend(countlist)
Z_indailyCountArray=np.array(inCardailyCountList).reshape(len(inOrderTimeList),24)

#绘制图像
X,Y=np.meshgrid(Y_dailyTime,X_inOrderTimeList)
fig=plt.figure()
#ax=Axes3D(fig)
ax=fig.add_subplot(121,projection='3d')
ax.plot_surface(X, Y, Z_indailyCountArray, rstride=1, cstride=1, cmap='rainbow')
#绘制登高图
ax=fig.add_subplot(122,projection='3d')
ax.contourf(X, Y, Z_indailyCountArray, zdir='z', offset=-2, cmap='rainbow')
#设定坐标轴
ax.set_xlabel('dailyhour')
ax.set_ylabel('date')
ax.set_zlabel('everyhour-inCarNumber')
#通过设定角度来查看显示图，第一个值表示俯仰角度，第二值表示偏转角度
ax.view_init(20,270)
plt.show()