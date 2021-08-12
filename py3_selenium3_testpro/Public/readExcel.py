# coding:utf-8

from Public import getPathInfo
import xlrd, os

class readExcel(object):
    def __init__(self, xlsx_name):
        path = getPathInfo.get_Path()                               # 获得上级目录路径
        self.xlsPath = os.path.join(path, 'TestData', xlsx_name)    # 获取用例文件路径
        self.file = xlrd.open_workbook(self.xlsPath)                # 打开用例Excel

    def get_sheetnames(self):
        '''
        返回所有sheet名称
        :return:
        '''
        return self.file.sheet_names()

    def get_xlsx(self, sheet):
        '''
        获取Excel中测试用例相关信息
        :param sheet:
        :return:
        '''
        list = []
        sheet = self.file.sheet_by_name(sheet)      # 获得指定sheet数据
        row_valuel = sheet.row_values(0)            # 获得第1行的标题
        nrows = sheet.nrows                         # 获得当前sheet行数
        ncols = sheet.ncols                         # 获得当前sheet列数
        for i in range(1, nrows):                   # 从第2行遍历当前sheet
            row = sheet.row_values(i)               # 获取行数据
            dict = {}
            for j in range(0, ncols):
                if row_valuel[j] == 'NO.' or row_valuel[j] == 'code':
                    dict[row_valuel[j]] = int(row[j])   # NO和code值取int
                else:
                    dict[row_valuel[j]] = row[j]    # 从第一列开始，将每一列的数据与第1行的数据组成一个键值对，形成字典
            list.append(dict)
        return list

if __name__ == '__main__':
    x = readExcel('UI_TestCase.xlsx')
    print(x.get_sheetnames())
    print(x.get_xlsx('login'))


















