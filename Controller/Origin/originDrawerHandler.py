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
    if len(dataSourceArray)>0 and dataSourceArray != None:
        for subSheetData in dataSourceArray:
            date = subSheetData[0]
            deep = subSheetData[1]
            perDeep = subSheetData[2]
            pureDrillingTime = subSheetData[3]
            aging = subSheetData[4]
            drillUtils = subSheetData[5]
            perDayDeepTipsText = subSheetData[6]
            workingHoursTipsText = subSheetData[7]
            drillNum = subSheetData[8]
            # drillInfo = ['特凿井分公司4202钻机海石湾瓦斯井']
            wks = op.new_sheet('w',lname = drillNum)
            deepTextList = []
            perDayDeepTipsTextList = []
            workingHoursTipsTextList = []
            dateTextList = []
            i = 0
            while i < len(date):
                if str(drillUtils[i]) == 'nan':
                    deepTextList.append((str)(deep[i]))
                else:
                    if '\n' in drillUtils[i]:
                        str1 = drillUtils[i][0:drillUtils[i].find('\n')]
                        str2 = drillUtils[i][drillUtils[i].find('\n')+1:-1]+drillUtils[i][-1]
                        print(str1)
                        print(str2)
                        deepTextList.append('\c2(\p80(' + str1 + '))' + '\n\c2(\p80(' + str2 + '))\n' + (str)(deep[i]))
                    else:
                        deepTextList.append('\c2(\p80(' + drillUtils[i] + '))\n' + (str)(deep[i]))

                if str(perDayDeepTipsText[i]) == 'nan':
                    perDayDeepTipsTextList.append((str)(perDeep[i]))
                else:
                    if '\n' in perDayDeepTipsText[i]:
                        str1 = perDayDeepTipsText[i][0:perDayDeepTipsText[i].find('\n')]
                        str2 = perDayDeepTipsText[i][perDayDeepTipsText[i].find('\n')+1:-1]+perDayDeepTipsText[i][-1]
                        perDayDeepTipsTextList.append('\c2(\p80(' + str1 + '))'+'\c2(\p80(' + str2 + '))\n' + (str)(perDeep[i]))
                    else:
                        perDayDeepTipsTextList.append('\c2(\p80(' + perDayDeepTipsText[i] + '))\n' + (str)(perDeep[i]))
                if str(workingHoursTipsText[i]) == 'nan':
                    workingHoursTipsTextList.append((str)(pureDrillingTime[i]))
                else:
                    if '\n' in workingHoursTipsText[i]:
                        str1 = workingHoursTipsText[i][0:workingHoursTipsText[i].find('\n')]
                        str2 = workingHoursTipsText[i][workingHoursTipsText[i].find('\n') + 1:-1]+workingHoursTipsText[i][-1]
                        workingHoursTipsTextList.append(
                            '\c2(\p80(' + str1 + '))' + '\c2(\p80(' + str2 + '))\n' + (str)(pureDrillingTime[i]))
                    else:
                        workingHoursTipsTextList.append('\c2(\p80(' + workingHoursTipsText[i] + '))\n' + (str)(pureDrillingTime[i]))
                dateTextList.append(i + 1)
                i += 1
            if len(date) > 7:
                wks.from_list(0,dateTextList,'日期')
                wks.from_list(11, date, '日期',axis='L')
            else:
                wks.from_list(0, date, '日期',axis='X')
            wks.from_list(1, deep, '井深', 'm')
            wks.from_list(2, perDeep, '日进尺', 'm')
            wks.from_list(3, pureDrillingTime, '生产时间', 'h')
            wks.from_list(4, aging, '钻井效率', 'm/h')
            wks.from_list(5, deepTextList, '井深标签B(Y)', axis='L')
            wks.from_list(6, perDayDeepTipsTextList, '日进尺标签C(Y)', axis='L')
            wks.from_list(7, workingHoursTipsTextList, '生产时间标签D(Y)', axis='L')
            wks.from_list(8, aging, '钻井效率标签E(Y)', axis='L')
            wks.from_list(9, drillUtils, '钻具', axis='L')
            wks.from_list(10, getDrillBaseInfo(drillNum), '钻机信息', axis='L')


            # Add data plots onto the graph
            if len(date) > 7:
                gp = op.new_graph(template='drillAginMonth', lname=drillNum)
            else:
                gp = op.new_graph(template='drillAgingOTPU', lname=drillNum)
            # Loop over layers and worksheets to add individual curve.
            for i, gl in enumerate(gp):
                dp = gl.add_plot(wks, 1 + i, 0)
                if (gl.label('titleText')) != None:
                    label = gl.label('titleText')
                    label.text = str(label.text).replace('drillNum',drillNum)

                # print(i)
                if i == 0:
                    if max(deep) > 0:
                        maxNumPlus1Str = str(max(deep))
                        if '.' in str(max(deep)):
                            maxNumPlus1Str = maxNumPlus1Str[0:maxNumPlus1Str.find('.')]
                        if min(deep) <= 10:
                            if 0 < max(deep) - min(deep) <= 50:
                                gl.set_ylim(0, float(maxNumPlus1Str)+10)
                                gl.set_ylim(step=10)
                            elif 50 < max(deep) - min(deep) <= 100:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 10)
                                gl.set_ylim(step=20)
                            elif 100 < max(deep) - min(deep) <= 500:
                                gl.set_ylim(0, float(maxNumPlus1Str)+20)
                                gl.set_ylim(step=50)
                            elif 300 < max(deep) - min(deep) <= 1000:
                                gl.set_ylim(0, float(maxNumPlus1Str)+50)
                                gl.set_ylim(step=100)
                            elif 1000 < max(deep) - min(deep) <= 10000:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 100)
                                gl.set_ylim(step=200)
                            else:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 100)
                                gl.set_ylim(step=20)
                        else:
                            if 0 < max(deep) - min(deep) <= 50:
                                gl.set_ylim(min(deep)-10, float(maxNumPlus1Str) + 10)
                                gl.set_ylim(step=10)
                            elif 50 < max(deep) - min(deep) <= 100:
                                gl.set_ylim(min(deep)-10, float(maxNumPlus1Str) + 10)
                                gl.set_ylim(step=20)
                            elif 100 < max(deep) - min(deep) <= 500:
                                gl.set_ylim(min(deep)-20, float(maxNumPlus1Str) + 20)
                                gl.set_ylim(step=50)
                            elif 300 < max(deep) - min(deep) <= 1000:
                                gl.set_ylim(min(deep)-20, float(maxNumPlus1Str) + 50)
                                gl.set_ylim(step=100)
                            elif 1000 < max(deep) - min(deep) <= 10000:
                                gl.set_ylim(min(deep)-10, float(maxNumPlus1Str) + 100)
                                gl.set_ylim(step=200)
                            else:
                                gl.set_ylim(min(deep) - 10, float(maxNumPlus1Str) + 100)
                                gl.set_ylim(step=20)

                    # dp.set_cmd('-a 1 815 test')

                    # dp.symbol_size=y4_text
                    # dp.symbol_sizefactor = 10
                    # gl.creat_label('123123')
                    # op.execute("label -a 2 840 \p400(xdfgsdf)")
                    # dp.set_cmd('label -a 2 840 \p400(%s)'%'cvbcv')
                    # op.attach()
                elif i == 1:
                    if max(perDeep) > 0:
                        maxNumPlus1Str = str(max(perDeep) + 1)
                        if ('.' in maxNumPlus1Str) :
                            maxNumPlus1Str = maxNumPlus1Str[0:maxNumPlus1Str.find('.')]
                        # gl.set_ylim(0, float(maxNumPlus1Str))
                        if min(perDeep) <= 10:
                            if 0 < max(perDeep) - min(perDeep) <= 1:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 0.5)
                            elif 1 < max(perDeep) - min(perDeep) <= 2:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 0.5)
                            elif 2 < max(perDeep) - min(perDeep) <= 5:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 1)
                            elif 5 < max(perDeep) - min(perDeep) <= 10:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 1)
                            elif 10 < max(perDeep) - min(perDeep) <= 20:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 2)
                            elif 20 < max(perDeep) - min(perDeep) <= 50:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 5)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 5)
                            elif 50 < max(perDeep) - min(perDeep) <= 100:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 10)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 10)
                            elif 100 < max(perDeep) - min(perDeep) <= 1000:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 10)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 20)
                            else:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 1)
                        else:
                            if 0 < max(perDeep) - min(perDeep) <= 1:
                                gl.set_ylim(min(perDeep) - 1, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 0.5)
                            elif 1 < max(perDeep) - min(perDeep) <= 2:
                                gl.set_ylim(min(perDeep) - 1, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 0.5)
                            elif 2 < max(perDeep) - min(perDeep) <= 5:
                                gl.set_ylim(min(perDeep) - 1, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 0.5)
                            elif 10 < max(perDeep) - min(perDeep) <= 20:
                                gl.set_ylim(min(perDeep) - 1, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 0.5)
                            elif 20 < max(perDeep) - min(perDeep) <= 50:
                                gl.set_ylim(min(perDeep) - 1, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step= (float(maxNumPlus1Str)//4) if (float(maxNumPlus1Str)//4) > 0 else 0.5)
                            elif 50 < max(perDeep) - min(perDeep) <= 100:
                                gl.set_ylim(min(perDeep) - 5, float(maxNumPlus1Str) + 5)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.5)
                            elif 100 < max(perDeep) - min(perDeep) <= 500:
                                gl.set_ylim(min(perDeep) - 10, float(maxNumPlus1Str) + 10)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.5)
                            elif 500 < max(perDeep) - min(perDeep) <= 1000:
                                gl.set_ylim(min(perDeep) - 20, float(maxNumPlus1Str) + 20)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.5)
                            else:
                                gl.set_ylim(min(perDeep) - 1, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.5)
                    # gl.set_ylim(step=int(maxNumPlus1Str) / 5)
                elif i == 2:
                    gl.set_ylim(0, 24)
                    gl.set_ylim(step=4)
                elif i == 3:
                    if max(aging) > 0:
                        maxNumPlus1Str = str(max(aging)+1)
                        if ('.' in maxNumPlus1Str):
                            maxNumPlus1Str = maxNumPlus1Str[0:maxNumPlus1Str.find('.')]
                        if min(aging) <= 1:
                            if 0 < max(aging) - min(aging) <= 0.1:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 0.1)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.1)
                            elif 0.1 < max(aging) - min(aging) <= 0.2:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 0.1)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.1)
                            elif 0.2 < max(aging) - min(aging) <= 0.5:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 0.1)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.1)
                            elif 0.5 < max(aging) - min(aging) <= 1:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 0.1)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.2)
                            elif 1 < max(aging) - min(aging) <= 2:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 0.2)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.5)
                            elif 2 < max(aging) - min(aging) <= 5:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 0.2)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.5)
                            elif 5 < max(aging) - min(aging) <= 10:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 0.5)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 1)
                            elif 10 < max(aging) - min(aging) <= 20:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 2)
                            elif 20 < max(aging) - min(aging) <= 50:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 5)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 5)
                            elif 50 < max(aging) - min(aging) <= 100:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 10)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 10)
                            elif 100 < max(aging) - min(aging) <= 1000:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 10)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 20)
                            else:
                                gl.set_ylim(0, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 1)
                        else:
                            if 0 < max(aging) - min(aging) <= 0.1:
                                gl.set_ylim(min(aging) - 0.1, float(maxNumPlus1Str) + 0.1)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.1)
                            elif 0.1 < max(aging) - min(aging) <= 0.2:
                                gl.set_ylim(min(aging) - 0.1, float(maxNumPlus1Str) + 0.1)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.1)
                            elif 0.2 < max(aging) - min(aging) <= 0.5:
                                gl.set_ylim(min(aging) - 0.1, float(maxNumPlus1Str) + 0.1)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.1)
                            elif 0.5 < max(aging) - min(aging) <= 1:
                                gl.set_ylim(min(aging) - 0.1, float(maxNumPlus1Str) + 0.1)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.2)
                            elif 1 < max(aging) - min(aging) <= 2:
                                gl.set_ylim(min(aging) - 0.2, float(maxNumPlus1Str) + 0.2)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.2)
                            elif 2 < max(aging) - min(aging) <= 5:
                                gl.set_ylim(min(aging) - 0.5, float(maxNumPlus1Str) + 0.5)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 0.5)
                            elif 5 < max(aging) - min(aging) <= 10:
                                gl.set_ylim(min(aging) - 1, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 1)
                            elif 10 < max(aging) - min(aging) <= 20:
                                gl.set_ylim(min(aging) - 2, float(maxNumPlus1Str) + 2)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 2)
                            elif 20 < max(aging) - min(aging) <= 50:
                                gl.set_ylim(min(aging) - 5, float(maxNumPlus1Str) + 5)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 5)
                            elif 50 < max(aging) - min(aging) <= 100:
                                gl.set_ylim(min(aging) - 10, float(maxNumPlus1Str) + 10)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 10)
                            elif 100 < max(aging) - min(aging) <= 500:
                                gl.set_ylim(min(aging) - 20, float(maxNumPlus1Str) + 20)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 20)
                            elif 500 < max(aging) - min(aging) <= 1000:
                                gl.set_ylim(min(aging) - 50, float(maxNumPlus1Str) + 50)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 50)
                            else:
                                gl.set_ylim(min(perDeep) - 1, float(maxNumPlus1Str) + 1)
                                gl.set_ylim(step=(float(maxNumPlus1Str) // 4) if (float(maxNumPlus1Str) // 4) > 0 else 1)
                        # gl.set_ylim(0,float(maxNumPlus1Str))
                    # gl.set_ylim(step=int(maxNumPlus1Str) / 5)
                else:
                    print('Error')
                gl.set_xlim(0.5, len(date)+0.5)
                gl.set_xlim(step=1)
                # gl.set

                # gl.
                # gl.set_xlim = (0.5,7.5,1)
                #
                # gl.ylim = (0, 200, 50)


def getDrillBaseInfo(drillNum: str):
    drillNumDict = {'4102-1': '矿产资源勘查分公司4102(TSJ-3000)钻机洛宁地热井钻效图',
                    '4106': '矿产资源勘查分公司4106(XY-8DB)钻机新乡能源三盘区断层勘查孔钻效图',
                    '4109': '矿产资源勘查分公司4109(XY-6B)钻机赵固二矿进风井井检孔钻效图',
                    '4205': '能源勘查分公司4205(TSJ-3000)平煤瓦斯抽采项目钻效图',
                    '4208': '能源勘查分公司4208(ZJ40)钻机中海油项目钻效图',
                    '4209': '能源勘查分公司4209(CMD100)钻机美中项目钻效图',
                    '4210': '能源勘查分公司4210(CMD100)钻机美中项目钻效图',
                    '4202': '特凿井分公司4202(TSJ-3000)钻机海石湾瓦斯井钻效图',
                    '4203': '特凿井分公司4203(TSJ-3000)钻机九里山瓦斯井钻效图',
                    '4207': '特凿井分公司4207(TSJ-3000)钻机平煤瓦斯抽采项目钻效图'}
    return drillNumDict[drillNum]

def loadDataFromExcel(fileNames: str):
    global globalAllInfoList
    path_openfile_name = fileNames
    print(path_openfile_name.title())
    dataSourceList = []
    df = pd.read_excel(path_openfile_name, sheet_name=None)
    if len(list(df)) > 0:
        # drillNum = list(df)[0]
        for subSheet in list(df):
            if path_openfile_name != '':
                input_table = pd.read_excel(path_openfile_name,sheet_name=subSheet)
                dataList = np.array(input_table.iloc[0:, 0:])
                dateList = []
                deepList = []
                perDayDeepList = []
                workingHourList = []
                workingAgingList = []
                drillToolsList = []
                perDayDeepTipsList = []
                workingHourTipsList = []

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
                            perDayDeepTipsList.append(i[6])
                            workingHourTipsList.append(i[7])
                ndList1 = [dateList.copy(),
                           deepList.copy(),
                           perDayDeepList.copy(),
                           workingHourList.copy(),
                           workingAgingList.copy(),
                           drillToolsList.copy(),
                           perDayDeepTipsList.copy(),
                           workingHourTipsList.copy(),
                           subSheet]
                ndArray = np.array(ndList1, dtype='object')
                # print(ndArray)
                dataSourceList.append(ndArray)
        return dataSourceList
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
