# coding:utf-8

import os

def get_Path():
    '''
    :return: 返回上级目录的绝对路径
    '''
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def join_cwd(path):
    '''
    和上级目录拼接路径
    :param path:
    :return:
    '''
    return os.path.join(get_Path(), path)

if __name__ == '__main__':
    print(join_cwd('Logs'))





