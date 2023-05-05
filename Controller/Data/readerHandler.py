import sys
import time
from datetime import datetime
import xlwt
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from PyQt5.QtWidgets import QMessageBox
from View.DPRAView import Ui_MainWindow
import pymongo
import copy
import datetime




globalTimeList:list = []
globalAllInfoList:list = []

class window(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchButton.clicked.connect(self.searchButtonOnClicked)
        self.startDateEdit.setDate(datetime.datetime.strptime('2023/04/14',"%Y/%m/%d"))
        self.endDateEdit.setDate(datetime.datetime.strptime('2023/04/20',"%Y/%m/%d"))

    def searchButtonOnClicked(self):
        print(self.startDateEdit.text().split('/'))
        print(self.startDateEdit.text().split('/')[1]+'月'+self.startDateEdit.text().split('/')[2]+'日')
        begin_date = datetime.datetime.strptime(self.startDateEdit.text(), "%Y/%m/%d")
        end_date = datetime.datetime.strptime(self.endDateEdit.text(), "%Y/%m/%d")
        if begin_date <= end_date:
            begin_date += datetime.timedelta(days=1)
            end_date += datetime.timedelta(days=1)
            begin_date_str = begin_date.strftime("%Y/%m/%d")
            end_date_str = end_date.strftime("%Y/%m/%d")
        else:
            print('数据不合法！！！！')
        searchProjectInfoWithDateAndDrillNum(begin_date_str,end_date_str,self.drillNumLineEdit.text())

    def setSearchButtonEnable(self):
        self.searchButton.setEnabled(True)

    def savedInMongoDB(self):
        global globalAllInfoList
        global globalCollectionName
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client.drillProject
        if len(globalCollectionName) > 0:
            collectionName = globalCollectionName[0]
            collection = db[collectionName]
            rowCount = self.dataTableWidget.rowCount()
            # columnCount = self.dataTableWidget.columnCount()
            i = 0
            while i < rowCount:
                # j = 0
                # while j < columnCount:
                #     # drillProjectItem = ['company':]
                #     j = j + 1
                keysList = ['projectDate',
                            'company',
                            'projectName',
                            'drillId',
                            'currentDeep',
                            'lastDayDeep',
                            'drillTools',
                            '6:00-10:00',
                            '10:00-14:00',
                            '14:00-18:00',
                            '18:00-22:00',
                            '22:00-2:00',
                            '22:00-2:00',
                            'tips',
                            'allInfo']
                print(globalAllInfoList[i])
                projectItem = []
                for infoList in globalAllInfoList[i]:
                    infoListStr = ''.join(infoList)
                    projectItem.append(infoListStr)
                    print(projectItem)
                drillProjectItem = dict(zip(keysList, projectItem))
                print(drillProjectItem)
                result = collection.update_one({"drillId":drillProjectItem["drillId"]},{"$set":drillProjectItem},upsert=True)
                print(result)
                i = i + 1
            QMessageBox.information(MainWindow, '提示：', '成功写入数据库！！！')
        else:
            QMessageBox.information(MainWindow, '警告！！！', '数据源选择有误，无法写入数据库！！！')

# 获取每列所占用的最大列宽
def get_max_col(max_list):
    line_list = []
    # i表示行，j代表列
    for j in range(len(max_list[0])):
        line_num = []
        for i in range(len(max_list)):
            line_num.append(max_list[i][j])  # 将每列的宽度存入line_num
        line_list.append(max(line_num))  # 将每列最大宽度存入line_list
    return line_list

def write_excel(data,drillNum,startDateStr,endDateStr):
    row_num = 0  # 记录写入行数
    col_list = []  # 记录每行宽度
    # 个人信息：姓名，性别，年龄，手机号，固定电话，邮箱
    # 创建一个Workbook对象
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    # 创建一个sheet对象
    sheet = book.add_sheet(drillNum, cell_overwrite_ok=True)
    col_num = [0 for x in range(0, 14)]
    # 写入数据
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            sheet.write(i, j, data[i][j])
            col_num[j] = len(data[i][j].encode('gb18030')) # 计算每列值的大小
        col_list.append(copy.copy(col_num))  # 记录一行每列写入的长度
        row_num += 1
    # 获取每列最大宽度
    col_max_num = get_max_col(col_list)
    # 设置自适应列宽
    for i in range(0, len(col_max_num)):
        # 256*字符数得到excel列宽,为了不显得特别紧凑添加两个字符宽度
        sheet.col(i).width = 256 * (col_max_num[i] + 2)
    startDate = datetime.datetime.strptime(startDateStr, "%Y/%m/%d")
    endDate = datetime.datetime.strptime(endDateStr, "%Y/%m/%d")
    startDate -= datetime.timedelta(days=1)
    endDate -= datetime.timedelta(days=1)
    begin_date_str = startDate.strftime("%Y-%m-%d")
    end_date_str = endDate.strftime("%Y-%m-%d")


    # 保存excel文件
    book.save('C:\\Users\\18637\\Desktop\\%s(%s至%s).xlsx'%(drillNum,begin_date_str,end_date_str))


def getEveryDay(startDateStr,endDateStr):
    date_list = []
    begin_date = datetime.datetime.strptime(startDateStr, "%Y/%m/%d")
    end_date = datetime.datetime.strptime(endDateStr, "%Y/%m/%d")
    while begin_date <= end_date:
        begin_date_str = begin_date.strftime("%Y/%m/%d")
        date_list.append(begin_date_str)
        begin_date += datetime.timedelta(days=1)

    return date_list

def searchProjectInfoWithDateAndDrillNum(startDateStr,endDateStr,drillNum):
    getEveryDay(startDateStr,endDateStr)
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.yesterday
    #日期	井深	日进尺	生产时间	钻井效率


    MutiRowList = [['日期',
                    '井深',
                    '日进尺',
                    '生产时间',
                    '钻井效率',
                    '钻具组合',
                    '备注',
                    '6:00-10:00',
                    '10:00-14:00',
                    '14:00-18:00',
                    '18:00-22:00',
                    '22:00-2:00',
                    '2:00-6:00',
                    'allInfo']]

    for dateCollection in getEveryDay(startDateStr,endDateStr):
        singleRowList = []

        myCol = db[dateCollection]
        results = myCol.find({'drillId': drillNum})
        print(results)
        #日期	井深	每日进尺	生产时间	钻效	孔径	备注

        keysList = ['projectDate',
                    'currentDeep',
                    'lastDayDeep',
                    'workingHour',
                    'workingAging',
                    'drillTools',
                    'tips',
                    '6:00-10:00',
                    '10:00-14:00',
                    '14:00-18:00',
                    '18:00-22:00',
                    '22:00-2:00',
                    '2:00-6:00',
                    'allInfo']
        for r in results:
            print(r)
            for k in keysList:
                singleRowList.append(r[k])
        MutiRowList.append(singleRowList)

    write_excel(MutiRowList,drillNum,startDateStr,endDateStr)

if __name__ == '__main__':
    #loadDataFromExcel('1')
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = window()  # 创建窗体对象
    MainWindow.show()  # 显示窗体

    sys.exit(app.exec_())  # 程序关闭时退出进程

qmut_1 = QMutex() # 创建线程锁
qmut_2 = QMutex()
# 继承QThread
class Thread_1(QThread):  # 线程1
    def __init__(self):
        super().__init__()

    def run(self):
        qmut_1.lock() # 加锁
        values = [1, 2, 3, 4, 5]
        for i in values:
            #print(i)
            time.sleep(0.5)  # 休眠
        qmut_1.unlock() # 解锁


class Thread_2(QThread):  # 线程2
    _signal =pyqtSignal()
    def __init__(self):
        super().__init__()

    def run(self):
        # qmut_2.lock()  # 加锁
        values = ["a", "b", "c", "d", "e"]
        for i in values:
           # print(i)
            time.sleep(0.5)
        # qmut_2.unlock()  # 解锁
        self._signal.emit()
