import originpro as op
import os
import datetime#用于获取当前系统时间

file_dir = r'C:\\Users\\18637\\Desktop\\'
newFilePath = ''
if os.path.lexists(file_dir) == False:#判断系统是否存在该指定路径，若不存在则创建该路径与子文件夹
    os.makedirs(file_dir)  # 创建该指定路径
    #有时需要给子文件夹加后缀来做区分，系统时间是一个不错的选择
    A_curr_time = datetime.datetime.now()
    A_time_str = datetime.datetime.strftime( A_curr_time, '%Y_%m_%d_%H_%M_%S' )
    newFilePath = file_dir+ '钻效分析图'+ "\\" + A_time_str
    os.makedirs(newFilePath)#创建子文件夹
if os.path.lexists(file_dir) == True:#若存在该指定路径则创建子文件夹
    A_curr_time = datetime.datetime.now()
    A_time_str = datetime.datetime.strftime( A_curr_time, '%Y_%m_%d_%H_%M_%S' )
    newFilePath = file_dir + '钻效分析图' + "\\" + A_time_str
    os.makedirs(newFilePath)#创建子文件夹

op.attach()
print(op.graph_list())
for graph in op.graph_list():
    graph.save_fig(path=newFilePath + '\\%s.png'%(graph.lname),width=4200,ratio=300)
    print(graph.lname)
