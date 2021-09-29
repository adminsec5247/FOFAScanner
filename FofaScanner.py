"""
Author:adminsec
Date:2021-9-29
Last Edit:2021-9-29
Version:v1.0
"""

import requests
import base64
import json
import datetime
import os
import argparse

description = "Please use a valid parameter"
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-size', type=int, help="每次查询返回记录数，默认为100条", dest="SIZE", default=100)
parser.add_argument('-page', type=int, help="翻页数，默认为第一页", dest="PAGE", default=1)
args = parser.parse_args()

FOFA_Email = '1903268948@qq.com'  # FOFA注册邮箱
FOFA_Key = '792d5699e1dbdcd32059a79e08a67640'  # FOFA API_Key
Size = args.SIZE  # FOFA官方为100条(每次查询返回记录数，默认为100条，最大可设置为10000条)
Page = args.PAGE  # FOFA官方为第一页(翻页数，默认为第一页)

params = {
    'email': FOFA_Email,
    'key': FOFA_Key,
    'size': Size,
    'page': Page
}

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61'
}


def get_qbase64():
    Keywords = input("请输入FOFA语法：")
    while Keywords == '':  # 若未输入语法，继续提示输入
        Keywords = input("请输入FOFA语法：")
    Keywords_coded = str(base64.b64encode(Keywords.encode("utf-8")), 'utf-8')  # 将语法进行Base64编码
    return Keywords_coded


def check_account():  # 检查账号和API_Key是否匹配
    url = 'https://fofa.so/api/v1/search/all'
    print("正在检查账号······")
    result = requests.get(url=url, params=params, headers=header).text
    if '401' in result:
        print("FOFA_Email或者FOFA_Key不正确!!请检查")
        exit()
    else:
        return True


def get_result():
    check_account()
    Search_Words = get_qbase64()
    url = 'https://fofa.so/api/v1/search/all?qbase64=' + Search_Words
    response = requests.get(url=url, params=params, headers=header)
    if '820000' in response.text:
        print("查询语法错误!!")
        exit()
    elif 'Server Error' in response.text:
        print("服务器异常!!")
        exit()
    elif 'not enough' in response.text:
        print("F币不足!!请到官网进行充值")
        exit()
    elif 'too large' in response.text:
        print("结果窗口过大!!")
        exit()
    else:
        result_list = response.json()['results']
        result_num = str(response.json()['size'])
        choice = input("当前结果共有" + result_num + "个,是否将" + str(Size * Page) + "个结果下载至本地?(y/n)")
        if choice == 'n' or choice == 'N' or choice == 'no' or choice == 'No':
            exit()
        else:
            if not os.path.exists('/results'):  # 检查results文件夹是否存在，不存在则创建
                os.mkdir('/results')
            file_name = "./results/" + str(datetime.datetime.now().month) + "-" + str(
                datetime.datetime.now().day) + ".txt"
            with open(file_name, 'w', encoding='utf-8') as f:
                for result in result_list:
                    if 'http://' not in result[0] and 'https://' not in result[0]:
                        target_url = "http://" + result[0] + "/"
                        f.write(target_url)
                        f.write('\n')
                    else:
                        target_url = result[0] + "/"
                        f.write(target_url)
                        f.write('\n')
                print('查询结果已保存至:' + file_name)


if __name__ == '__main__':
    get_result()
