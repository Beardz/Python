from factory_config_线上 import *
import requests
import json

n_data = json.dumps(data)
headers = {"Content-Type":"application/json; charset=utf-8",'User_Agent':'PostmanRuntime/7.26.2','Connection':'keep-alive'}

def add_version():
    #线上
    rps = requests.put(url='http://device-test.dding.net:3001/factoryTest/gatewayless/versionRestriction', data=n_data,headers=headers)
    print(rps.text)
    result = json.loads(rps.text)
    if result['ErrMsg'] == 'success':
        c_data = str(data).replace(",", ",\n")
        print('增加版本限制：%s\n  成功'%c_data)
        print("-----------------增加分割线------------------")
    else:
        print('增加版本限制失败：%s'% result['ErrMsg'])

def delete_version():
    #线上
    rps = requests.delete(url='http://device-test.dding.net:3001/factoryTest/gatewayless/versionRestriction',data=n_data,headers=headers)
    print(rps.text)
    result = json.loads(rps.text)
    if result['ErrMsg'] == 'success':
        c_data = str(data).replace(",", ",\n")
        print('删除版本限制：\n %s 成功' % c_data)
        print("-----------------删除分割线------------------")
    else:
        print('删除版本限制失败：%s'% result['ErrMsg'])

def check_version():
    #线上
    url = 'http://device-test.dding.net:3001/factoryTest/gatewayless/versionRestriction?model=%s'%model
    rep= requests.get(url)
    dict1=json.loads(rep.text)
    n_dict = dict1['list']
    print('目前共有%s种厂测组合版本存在：'%len(n_dict))
    a=0
    for i in n_dict:
        a=a+1
        print("-----------------版本分割线------------------")
        print("第%s种产测版本如下："%a)
        print(str(i).replace(",", ",\n"))



if __name__ == '__main__':
    num = input('增加版本组合请输入：1\n删除版本组合请输入：2\n查询版本组合请输入：3\n')
    if num == '1':
        add_version()
        check_version()
    elif num == '2':
        delete_version()
        check_version()
    elif num =='3':
        check_version()
    else:
        print('参数有误！')
