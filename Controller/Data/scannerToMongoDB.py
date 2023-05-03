import sys
import os
import time
import datetime
import pandas as pd
import numpy as np
import re
import pymongo


globalAllInfoList:list = []
globalFilesPathList:list = []
globalCollectionName:list = []

def saveDataToMongoDB():
    global globalFilesPathList
    global globalCollectionName
    globalAllInfoList.clear()
    globalCollectionName.clear()
    if len(globalFilesPathList) > 0:
        for i in globalFilesPathList:
            #print(i)
            patternName = re.compile(r'[0-9]+月+[0-9]+日')
            if patternName.search(i):
                print("2023/"+patternName.search(i).group().replace('日','').replace('月','/'))
                date1 = datetime.datetime.strptime("2023/"+patternName.search(i).group().replace('日','').replace('月','/'), "%Y/%m/%d")
                dateStr = date1.strftime("%Y/%m/%d")
                globalCollectionName.append(dateStr)
                loadDataFromExcel(i)
                savedInMongoDB(dateStr)
            else:
                print('文件命名无日期相关信息！！！！！！！')
                break
    print('全部数据导入成功！！！！')



def savedInMongoDB(dateStr):
    global globalAllInfoList
    global globalCollectionName
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.yesterday
    if len(globalCollectionName) > 0:
        collectionName = globalCollectionName[0]
        collection = db[dateStr]
        rowCount = len(globalAllInfoList)
        # columnCount = self.dataTableWidget.columnCount()
        i = 0
        while i < rowCount:
            keysList = ['projectDate',
                        'company',
                        'projectName',
                        'drillId',
                        'currentDeep',
                        'lastDayDeep',
                        'workingHour',
                        'workingAging',
                        'drillTools',
                        '6:00-10:00',
                        '10:00-14:00',
                        '14:00-18:00',
                        '18:00-22:00',
                        '22:00-2:00',
                        '2:00-6:00',
                        'tips',
                        'allInfo']
            projectItem = []
            for infoList in globalAllInfoList[i]:
                infoListStr = ''.join(infoList)
                projectItem.append(infoListStr)
                # print(projectItem)
            drillProjectItem = dict(zip(keysList, projectItem))
            print(drillProjectItem)
            result = collection.update_one({"drillId":drillProjectItem["drillId"]},{"$set":drillProjectItem},upsert=True)
            print(result)
            i = i + 1
        print('成功写入数据库！！！')
    else:
        print('数据源选择有误，无法写入数据库！！！')

def loadDataFromExcel(fileNames: str):
    global globalAllInfoList
    path_openfile_name = fileNames

    if path_openfile_name != '':
        input_table = pd.read_excel(path_openfile_name)
        dataList = np.array(input_table.iloc[3:, 0:])
        dateList = []
        companyList = []
        # print(dataList)
        drillInfoList = []
        drillProjectNameList = []
        drillNumList = []
        deepList = []
        perDayDeepList = []
        workingHourList = []
        workingAgingList = []
        drillToolsList = []
        workingStateList_01 = []
        workingStateList_02 = []
        workingStateList_03 = []
        workingStateList_04 = []
        workingStateList_05 = []
        workingStateList_06 = []
        tipsList = []
        allInfoList = []
        m = 0
        if 0 < len(dataList):
            for i in dataList:
                # 索引出每个不为空的第一行即为新的项目数据行

                if str(i[0]) != 'nan':
                    dateList.clear()
                    drillInfoList.clear()
                    companyList.clear()
                    drillProjectNameList.clear()
                    drillNumList.clear()
                    deepList.clear()
                    perDayDeepList.clear()
                    workingHourList.clear()
                    workingAgingList.clear()
                    drillToolsList.clear()
                    workingStateList_01.clear()
                    workingStateList_02.clear()
                    workingStateList_03.clear()
                    workingStateList_04.clear()
                    workingStateList_05.clear()
                    workingStateList_06.clear()
                    tipsList.clear()
                    allInfoList.clear()

                    datePatternName = re.compile(r'[0-9]+月+[0-9]+日')
                    drillToolsPattern = re.compile(r'Φ[A-Za-z0-9]+.[A-Za-z0-9]+.*PDC|'
                                                   r'φ[A-Za-z0-9]+.[A-Za-z0-9]+.*PDC|'
                                                   r'Ф[A-Za-z0-9]+.[A-Za-z0-9]+.*PDC|'
                                                   r'Φ[A-Za-z0-9]+.*PDC|'
                                                   r'φ[A-Za-z0-9]+.*PDC|'
                                                   r'Ф[A-Za-z0-9]+.*PDC|'
                                                   r'Φ[A-Za-z0-9]+[\u4e00-\u9fa5]{0,}钻头|'
                                                   r'φ[A-Za-z0-9]+[\u4e00-\u9fa5]{0,}钻头|'
                                                   r'Ф[A-Za-z0-9]+[\u4e00-\u9fa5]{0,}钻头|'
                                                   r'Φ[A-Za-z0-9]+.[A-Za-z0-9]+[\u4e00-\u9fa5]{0,}钻头|'
                                                   r'φ[A-Za-z0-9]+.[A-Za-z0-9]+[\u4e00-\u9fa5]{0,}钻头|'
                                                   r'Ф[A-Za-z0-9]+.[A-Za-z0-9]+[\u4e00-\u9fa5]{0,}钻头|'
                                                   r'Φ[A-Za-z0-9]+.*复合片|'
                                                   r'φ[A-Za-z0-9]+.*复合片|'
                                                   r'Ф[A-Za-z0-9]+.*复合片|'
                                                   r'[A-Za-z0-9]+钻头|'
                                                   r'[A-Za-z0-9]+.[A-Za-z0-9]+.*钻头|'
                                                   r'Φ[A-Za-z0-9]+.[A-Za-z0-9]+.*钻头|'
                                                   r'φ[A-Za-z0-9]+.[A-Za-z0-9]+.*钻头|'
                                                   r'Ф[A-Za-z0-9]+.[A-Za-z0-9]+.*钻头|'
                                                   r'Φ[A-Za-z0-9]+.*钻头|'
                                                   r'φ[A-Za-z0-9]+.*钻头|'
                                                   r'Ф[A-Za-z0-9]+.*钻头|'
                                                   r'Φ[A-Za-z0-9]+.*牙轮|'
                                                   r'φ[A-Za-z0-9]+.*牙轮|'
                                                   r'Ф[A-Za-z0-9]+.*牙轮|'
                                                   r'Φ[A-Za-z0-9]+.[A-Za-z0-9]+.*牙轮|'
                                                   r'φ[A-Za-z0-9]+.[A-Za-z0-9]+.*牙轮|'
                                                   r'Ф[A-Za-z0-9]+.[A-Za-z0-9]+.*牙轮')
                    # 171.5mm潜孔锤头

                    if datePatternName.search(fileNames):
                        currentDate = datetime.datetime.strptime(datePatternName.search(fileNames).group(), "%m月%d日")
                        yesterday = currentDate - datetime.timedelta(days=1)
                        dateStr = yesterday.strftime("%#m月%#d日")
                        dateList.append(dateStr)

                    companyList.append(str(i[0]))
                    drillInfoStrList = str(i[1]).split()
                    drillInfoStr = str(drillInfoStrList)
                    drillNameStr = str(i[1]).split()[0]

                    # 正则表达找出是项目名称
                    # patternName = re.compile(r'^[\u4e00-\u9fa5]+')
                    # if patternName.search(drillInfoStr):
                    #     drillNameStr = patternName.search(drillInfoStr).group()
                    # else:
                    #     drillNameStr = 'xxxx'
                    #     print('未找到项目名称！！！')
                    drillProjectNameList.append(drillNameStr)
                    print(drillNameStr)
                    # 正则表达找出是否为队属钻机
                    patternNum = re.compile(r'[-[0-9]+[\u4E00-\u9FA5A-Za-z0-9]+（.*\属）')
                    patternNum1 = re.compile(r'[-[0-9]+[\u4E00-\u9FA5A-Za-z0-9]+（.*\协）')
                    patternNum2 = re.compile(r'[-[0-9]+[\u4E00-\u9FA5A-Za-z0-9]+（.*\管）')

                    if patternNum.search(drillInfoStr):
                        drillNumStr = patternNum.search(drillInfoStr).group()
                    else:
                        if patternNum1.search(drillInfoStr):
                            drillNumStr = patternNum1.search(drillInfoStr).group()
                        else:
                            if patternNum2.search(drillInfoStr):
                                drillNumStr = patternNum2.search(drillInfoStr).group()
                            else:
                                drillNumStr = 'xxxx'
                                print('未匹配！！！！')
                    print(drillNumStr)
                    if '队管' in drillNumStr:
                        drillNumStr = drillNumStr.replace('管', '属')
                    drillNumStr = drillNumStr.replace('（','')
                    drillNumStr = drillNumStr.replace('）','')
                    drillNumStr = drillNumStr.replace('队','')
                    drillNumStr = drillNumStr.replace('属','')
                    drillNumList.append(drillNumStr)

                    deepList.append(str(input_table.iloc[m + 3, 2]))

                    # print('日进尺：' + str(input_table.iloc[m, 3]) + '(m)')
                    perDayDeepList.append(str(input_table.iloc[m + 3, 3]))
                    if checkoutDrillTools(drillToolsPattern, str(input_table.iloc[m + 3, 6])) != None:
                        drillToolsList.append(checkoutDrillTools(drillToolsPattern, str(input_table.iloc[m + 3, 6])))
                    # print('工况：' + str(input_table.iloc[m, 5]))
                    workingStateList_01.append(''.join(str(input_table.iloc[m + 3, 5]).split()))
                    if '扩孔' in workingStateList_01[0] or '钻进' in workingStateList_01[0]:
                        workingHourList.append('4')

                    # print('备注：' + str(input_table.iloc[m, 16]))
                    tipsList.append(str(input_table.iloc[m + 3, 16]))
                    allInfoList.append(str(i[1]))
                else:
                    if m % 6 == 1:
                        # workingStateList_02.append('10:00-14:00' + ''.join(str(input_table.iloc[m+3, 5]).split()))
                        workingStateList_02.append(''.join(str(input_table.iloc[m + 3, 5]).split()))
                        if '扩孔' in workingStateList_02[0] or '钻进' in workingStateList_02[0]:
                            workingHourList.append('4')
                        if checkoutDrillTools(drillToolsPattern, str(input_table.iloc[m + 3, 6])) != None:
                            drillToolsList.append(checkoutDrillTools(drillToolsPattern, str(input_table.iloc[m + 3, 6])))
                    elif m % 6 == 2:
                        # workingStateList.append('14:00-18:00' + ''.join(str(input_table.iloc[m+3, 5]).split()))
                        workingStateList_03.append(''.join(str(input_table.iloc[m + 3, 5]).split()))
                        if '扩孔' in workingStateList_03[0] or '钻进' in workingStateList_03[0]:
                            workingHourList.append('4')
                            if checkoutDrillTools(drillToolsPattern, str(input_table.iloc[m + 3, 6])) != None:
                                drillToolsList.append(checkoutDrillTools(drillToolsPattern, str(input_table.iloc[m + 3, 6])))
                    elif m % 6 == 3:
                        workingStateList_04.append(''.join(str(input_table.iloc[m + 3, 5]).split()))
                        if '扩孔' in workingStateList_04[0] or '钻进' in workingStateList_04[0]:
                            workingHourList.append('4')
                        if checkoutDrillTools(drillToolsPattern, str(input_table.iloc[m + 3, 6])) != None:
                            drillToolsList.append( checkoutDrillTools(drillToolsPattern, str(input_table.iloc[m + 3, 6])))
                        # workingStateList.append('18:00-22:00' + ''.join(str(input_table.iloc[m+3, 5]).split()))
                    elif m % 6 == 4:
                        workingStateList_05.append(''.join(str(input_table.iloc[m + 3, 5]).split()))
                        if '扩孔' in workingStateList_05[0] or '钻进' in workingStateList_05[0]:
                            workingHourList.append('4')
                        if checkoutDrillTools(drillToolsPattern, str(input_table.iloc[m + 3, 6])) != None:
                            drillToolsList.append(checkoutDrillTools(drillToolsPattern, str(input_table.iloc[m + 3, 6])))
                        # workingStateList.append('22:00-2:00' + ''.join(str(input_table.iloc[m+3, 5]).split()))
                    elif m % 6 == 5:
                        workingStateList_06.append(''.join(str(input_table.iloc[m + 3, 5]).split()))
                        if '扩孔' in workingStateList_06[0] or '钻进' in workingStateList_06[0]:
                            workingHourList.append('4')
                        if  '外协' not in drillNumStr:
                            workHour = len(workingHourList) * 4
                            workingHourList.clear()
                            workingHourList.append(str(workHour))
                            if workHour > 0:
                                workAgingStr = str(round(float(perDayDeepList[0]) / float(workHour), 2))
                            else:
                                workAgingStr = '0'
                            workingAgingList.append(workAgingStr)
                        else:
                            print('外协钻机不计算！！！')

                        # workingStateList.append('2:00-6:00' + ''.join(str(input_table.iloc[m+3, 5]).split()))
                        ndList1 = [dateList.copy(),
                                   companyList.copy(),
                                   drillProjectNameList.copy(),
                                   drillNumList.copy(),
                                   deepList.copy(),
                                   perDayDeepList.copy(),
                                   workingHourList.copy(),
                                   workingAgingList.copy(),
                                   drillToolsList.copy(),
                                   workingStateList_01.copy(),
                                   workingStateList_02.copy(),
                                   workingStateList_03.copy(),
                                   workingStateList_04.copy(),
                                   workingStateList_05.copy(),
                                   workingStateList_06.copy(),
                                   tipsList.copy(),
                                   allInfoList.copy()]
                        ndArray = np.array(ndList1, dtype='object')

                        if '外协' not in drillNumStr:
                            if checkoutDrillTools(drillToolsPattern, str(input_table.iloc[m + 3, 6])) != None:
                                drillToolsList.append(
                                    checkoutDrillTools(drillToolsPattern, str(input_table.iloc[m + 3, 6])))
                            globalAllInfoList.append(ndArray)
                        else:
                            print('数据不合法哦！！！')
                m += 1

        else:
            print('Error!')

    else:
        print('Error!')

def checkoutDrillTools(drillToolsPattern,sourceStr):
    if drillToolsPattern.search(sourceStr):
        drillToolsStr = drillToolsPattern.search(sourceStr).group()
        if drillToolsStr != '':
            if 'Ф' in drillToolsStr:
                drillToolsStr = drillToolsStr.replace('Ф', 'φ')
                if drillToolsStr.index('φ') > 0:
                    drillToolsStr = drillToolsStr[drillToolsStr.index('φ'):len(drillToolsStr)]
            elif 'φ' in drillToolsStr:
                print('φ')
            elif 'Φ' in drillToolsStr:
                drillToolsStr = drillToolsStr.replace('Φ', 'φ')
                if drillToolsStr.index('φ') > 0:
                    drillToolsStr = drillToolsStr[drillToolsStr.index('φ'):len(drillToolsStr)]
            elif 'Ф' not in drillToolsStr and 'φ' not in drillToolsStr and 'Φ' not in drillToolsStr:
                drillToolsStr = 'φ' + drillToolsStr
            else:
                print(drillToolsStr)

            return drillToolsStr
        else:
            return None
    else:
        return None
def scannerAllFolder(pathName):
    global globalFilesPathList
    if os.path.exists(pathName):
        filelist = os.listdir(pathName)
        for f in filelist:
            f = os.path.join(pathName, f)
            if os.path.isdir(f):
                scannerAllFolder(f)
            else:
                dirname = os.path.dirname(f)
                baseName = os.path.basename(f)
                if dirname.endswith(os.sep):
                    globalFilesPathList.append(dirname + baseName)
                else:
                    globalFilesPathList.append(dirname + os.sep + baseName)

if __name__ == '__main__':
    #loadDataFromExcel('1')
    pathName = 'C:\\Users\\18637\\Desktop\\生产日报\\2023'
    # pathName = 'C:\\Users\\18637\\Desktop\\test'
    scannerAllFolder(pathName)
    if len(globalFilesPathList)>0:
        for f in globalFilesPathList:
            print(f)
    else:
        print('无文件！！！')

    saveDataToMongoDB()
