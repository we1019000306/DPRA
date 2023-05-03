'''
This sample shows how to use from_file function to import text data to worksheet
'''
import originpro as op
import pandas as pd
import numpy as np
import os

globalFilesPathList:list = []

def drawPicture(fileName: str):
    op.set_show()
    dataSourceArray = loadDataFromExcel(fileName)

    date = dataSourceArray[0]
    deep = dataSourceArray[1]
    perDeep = dataSourceArray[2]
    pureDrillingTime = dataSourceArray[3]
    aging = dataSourceArray[4]
    drillUtils = dataSourceArray[5]
    tipsText = dataSourceArray[6]
    drillNum = dataSourceArray[7]

    # drillInfo = ['特凿井分公司4202钻机海石湾瓦斯井']

    wks = op.new_sheet('w')
    deepTextList = []
    pureDrillingTimeTextList = []
    i = 0
    while i < 7:
        if str(drillUtils[i]) == 'nan':
            deepTextList.append((str)(deep[i]))
        else:
            deepTextList.append('\c2(\p80(' + drillUtils[i] + '))\n' + (str)(deep[i]))

        if str(tipsText[i]) == 'nan':
            pureDrillingTimeTextList.append((str)(pureDrillingTime[i]))
        else:
            pureDrillingTimeTextList.append('\c2(\p80(' + tipsText[i] + '))\n' + (str)(pureDrillingTime[i]))
        i += 1
    wks.from_list(0, date, '日期')
    wks.from_list(1, deep, '井深', 'm')
    wks.from_list(2, perDeep, '日进尺', 'm')
    wks.from_list(3, pureDrillingTime, '生产时间', 'h')
    wks.from_list(4, aging, '钻井效率', 'm/h')
    wks.from_list(5, deepTextList, '井深标签B(Y)', axis='L')
    wks.from_list(6, perDeep, '日进尺标签C(Y)', axis='L')
    wks.from_list(7, pureDrillingTimeTextList, '生产时间标签D(Y)', axis='L')
    wks.from_list(8, aging, '钻井效率标签E(Y)', axis='L')
    wks.from_list(9, tipsText, '钻具', axis='L')
    wks.from_list(10, getDrillBaseInfo(drillNum), '钻机信息', axis='L')

    # Add data plots onto the graph
    gp = op.new_graph(template='drillAgingOTPU')  # load Vertical 2 Panel graph template

    # Loop over layers and worksheets to add individual curve.
    for i, gl in enumerate(gp):
        dp = gl.add_plot(wks, 1 + i, 0)

        # print(i)
        if i == 0:
            # maxNumPlus1Str = str(max(deep) + 50)
            # maxNumPlus1Str = maxNumPlus1Str[0:maxNumPlus1Str.find('.')]
            # gl.set_ylim(0, float(maxNumPlus1Str))
            # gl.set_ylim(step=int(maxNumPlus1Str) / 5)
            gl.set_ylim(begin=min(deep) - 10,end=max(deep) + 10)
            # dp.set_cmd('-a 1 815 test')

            # dp.symbol_size=y4_text
            # dp.symbol_sizefactor = 10
            # gl.creat_label('123123')
            # op.execute("label -a 2 840 \p400(xdfgsdf)")
            # dp.set_cmd('label -a 2 840 \p400(%s)'%'cvbcv')
            # op.attach()
        elif i == 1:
            maxNumPlus1Str = str(max(perDeep) + 1)
            maxNumPlus1Str = maxNumPlus1Str[0:maxNumPlus1Str.find('.')]
            gl.set_ylim(0, float(maxNumPlus1Str))
            # gl.set_ylim(step=int(maxNumPlus1Str) / 5)
        elif i == 2:
            gl.set_ylim(0, 24)
            gl.set_ylim(step=4)
        elif i == 3:
            maxNumPlus1Str = str(max(aging)+1)
            maxNumPlus1Str = maxNumPlus1Str[0:maxNumPlus1Str.find('.')]
            gl.set_ylim(0,float(maxNumPlus1Str))
            # gl.set_ylim(step=int(maxNumPlus1Str) / 5)
        else:
            print('Error')
        gl.set_xlim(0.5, 7.5)
        gl.set_xlim(step=1)
        # gl.set_xlim = (0.5,7.5,1)
        #
        # gl.ylim = (0, 200, 50)


def getDrillBaseInfo(drillNum: str):
    drillNumDict = {'4102-1': '矿产资源勘查分公司4102(TSJ-3000)钻机洛宁地热井钻效图',
                    '4106': '矿产资源勘查分公司4106(XY-8DB)钻机新乡能源三盘去断层勘查孔钻效图',
                    '4109': '矿产资源勘查分公司4109(XY-6B)钻机赵固二矿进风井井检孔钻效图',
                    '4205': '4205',
                    '4208': '能源勘查分公司4208(ZJ40)钻机中海油项目--钻效图',
                    '4209': '能源勘查分公司4209(CMD100)钻机美中项目钻效图',
                    '4210': '能源勘查分公司4210(CMD100)钻机美中项目钻效图',
                    '4202': '特凿井分公司4202(TSJ-3000)钻机海石湾瓦斯井钻效图',
                    '4203': '特凿井分公司4203(TSJ-3000)钻机九里山瓦斯井钻效图',
                    '4207': '特凿井分公司4207(TSJ-3000)钻机平煤八矿瓦斯井钻效图'}
    return drillNumDict[drillNum]

def loadDataFromExcel(fileNames: str):
    global globalAllInfoList
    path_openfile_name = fileNames
    print(path_openfile_name.title())
    df = pd.read_excel(path_openfile_name, sheet_name=None)
    if len(list(df)) > 0:
        drillNum = list(df)[0]
    else:
        drillNum = ''
    print(drillNum)
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
        ndList1 = [dateList.copy(),
                   deepList.copy(),
                   perDayDeepList.copy(),
                   workingHourList.copy(),
                   workingAgingList.copy(),
                   drillToolsList.copy(),
                   tipsList.copy(),
                   drillNum]
        ndArray = np.array(ndList1, dtype='object')
        # print(ndArray)

        return ndArray

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


pathName = 'C:\\Users\\18637\\Desktop\\钻效分析图\\钻效分析数据源\\currentData'
scannerAllFolder(pathName)
if len(globalFilesPathList) > 0:
    for i in globalFilesPathList:
        #print(i)
        drawPicture(i)
    print('全部数据导入成功！！！！')



# gl.label('Legend')
# Customize legend
# lgnd = gp[1].label('Legend')
# lgnd.text = '\l(1) %(1, @ws)\n\l(2) %(2, @ws)\n\l(3) %(3, @ws)'
# lgnd.set_int('left', 4900)
# lgnd.set_int('top', 100)

# gp[0].label('Legend').remove()

# f = op.path('e')+r'User Files\4202.csv'
# print(f)
# #assume active worksheet
# wks = op.find_sheet()
#
# #By default, CSV connector is used
# wks.from_file(f)
#
# print(wks.shape)
import os
# x_vals = [1,2,3,4,5,6,7,8,9,10]
# y_vals = [23,45,78,133,178,199,234,278,341,400]
# y1_vals = [5,5,5,6,5,6,7,8,6,16]
#
# wks = op.new_sheet('w')
#
# wks.from_list(0, x_vals, 'X Values')
# wks.from_list(1, y_vals, 'Y Values')
# wks.from_list(2, y1_vals, 'Y1 Values')
# gp = op.new_graph()
# gl = gp[0]
# gl.add_plot(wks, 2, 0)
# gl.add_plot(wks,1,0)
# gl.rescale()
# # gl.group()
# fpath = op.path('u') + 'simple.png'
# gp.save_fig(fpath)
# print(f'{gl} is exported as {fpath}')
# op.exit()

# for wks, fn in zip(wb, ['S15-125-03.dat', 'S21-235-07.dat', 'S32-014-04.dat']):
#     wks.from_file(os.path.join(op.path('e'), 'Samples', 'Import and Export', fn))
