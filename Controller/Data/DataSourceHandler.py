import pandas as pd
import numpy as np
# import re
# import datetime

def loadDataFromExcel(fileNames: str):
    global globalAllInfoList
    path_openfile_name = fileNames

    if path_openfile_name != '':
        input_table = pd.read_excel(path_openfile_name)
        dataList = np.array(input_table.iloc[0:, 0:])
        dateList = []
        deepList = []
        perDayDeepList = []
        workingHourList = []
        workingAgingList = []
        drillToolsList = []
        tipsList = []

        if 0 < len(dataList):
            for i in dataList:
                # 索引出每个不为空的第一行即为新的项目数据行
                if str(i[0]) != 'nan':
                    # datePatternName = re.compile(r'[0-9]+月+[0-9]+日')
                    # drillToolsPattern = re.compile(r'Φ[A-Za-z0-9]+.[A-Za-z0-9]+.*PDC|'
                    #                                r'φ[A-Za-z0-9]+.[A-Za-z0-9]+.*PDC|'
                    #                                r'Ф[A-Za-z0-9]+.[A-Za-z0-9]+.*PDC|')
                    # # 171.5mm潜孔锤头
                    #
                    # if datePatternName.search(fileNames):
                    #     currentDate = datetime.datetime.strptime(datePatternName.search(fileNames).group(), "%m月%d日")
                    #     yesterday = currentDate - datetime.timedelta(days=1)
                    #     dateStr = yesterday.strftime("%#m月%#d日")
                    #     dateList.append(dateStr)
                    dateList.append(i[0])
                    deepList.append(i[1])
                    perDayDeepList.append(i[2])
                    workingHourList.append(i[3])
                    workingAgingList.append(i[4])
                    drillToolsList.append(i[5])
                    tipsList.append(i[6])
fileName = r'C:\Users\18637\Desktop\钻效分析图\钻效分析数据源\特凿\0420\xlsx\4202(2023-4-15至2023-4-21).xlsx'
loadDataFromExcel(fileName)