import os
import hashlib
import time
import json
import re
import http.client
import configparser
import oss2

def uploadOss(key,filename):
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
    result = oss2.resumable_upload(bucket, key, filename, progress_callback= percentage)
    # if result == 200:
    #     print('上传成功')
    # else:
    #     print('上传失败')

def percentage(consumed_bytes,total_bytes):
    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())+'  '+f'\r{consumed_bytes / total_bytes:.2%}',end = '')

def write_config(filename, encodeing):
    with open(filename, 'w', encoding=encodeing) as f:
        config.write(f)

def calculate_file_md5(file_path):
    with open(file_path, 'rb') as file:
        md5_obj = hashlib.md5()
        while True:
            data = file.read(4096)  # 每次读取4096字节
            if not data:
                break
            md5_obj.update(data)
 
    md5_value = md5_obj.hexdigest()
    return md5_value

def upload():
    # 定义文件夹路径
    # folder_path = 'D:\\tool\\firmware\\V18\\ota'
    # 获取文件夹下所有文件和文件夹的名字
    filenames = os.listdir(folder_path)
    conn = http.client.HTTPConnection("39.108.235.188", 8094)

    headers = {
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Host': '39.108.235.188:8094',
    'Connection': 'keep-alive'
    }
    files = [f for f in filenames if os.path.isfile(os.path.join(folder_path, f))]
    
    # 打印所有文件
    for file in files:
        if (re.findall('.bin',file) and re.findall('OTA',file)) or re.findall('Sound',file):
            file_path = os.path.join(folder_path, file)
            file_size = os.path.getsize(file_path)
            md5 = calculate_file_md5(file_path=folder_path+'\\'+file)
            url = file.replace('$','%24')
            # print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())+'  '+file)
            if len(url.split('%24')) > 1:
                module = url.split('%24')[1].split('_')[0]
                version = url.split('_')[len(url.split('_'))-1].split('.bin')[0]+'_'+str(int(time.time()))
            elif re.findall('Sound',url):
                module = 8
                version = url.split('_')[len(url.split('_'))-1].split('.bin')[0]+'_'+str(int(time.time()))
            elif re.findall('OEM',url) or re.findall('_4_',url):
                module = 4
                version = url.split('OTA_')[len(url.split('OTA_'))-1].split('.bin')[0]+'_'+str(int(time.time()))
            
            url = url.replace('%24','_')
            # print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())+'  '+url,module,version)
            if md5 != config.get('md5',module) :
                print('OSS上传固件')
                uploadOss(config.get('cfg','upload_path')+url,config.get('cfg','folder_path')+'\\'+file)
                #获取目录文件版本并修改配置文件对应固件版本
                if config.has_option('fileVer', module):
                    config.set('fileVer', str(module), str(version))
                    write_config(cfg_path,encodeing='UTF-8')
            elif md5 == config.get('md5',module):
                print('md5一致，不上传OSS')
                
            
            payload = json.dumps({
            "moduleCode": module,
            "fileName": url,
            "fileUrl": fileUrl+config.get('cfg','upload_path')+url,
            "fileVer": version,
            "fileLen": file_size,
            "fileDesc": file,
            "pidList": "001,002",
            "fileMd5": md5,
            "createUser": config.get('cfg','user'),
            "uploadIp": "127.0.0.1",
            "uploadPersion": config.get('cfg','user'),
            "customerApp": 1
            })
                #修改配置文件对应moduleCode firmwareId
            if md5 != config.get('md5',module) :
                print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())+'  '+payload)
                conn.request("POST", "/ota/firmware/uploadFirmware", payload, headers)
                
                res = conn.getresponse()
                data = res.read()
                print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())+'  fileName = '+url+'  '+version +' = '+ data.decode("utf-8")+'   fileUrl= '+fileUrl+config.get('cfg','upload_path')+url)
                if config.has_option('firmwareId', module):
                    config.set('firmwareId', str(module), str(data.decode("utf-8")))
                    config.set('md5',str(module),md5)
                    config.set('fileUrl',str(module),fileUrl+config.get('cfg','upload_path')+url)
                    write_config(cfg_path,encodeing='UTF-8')
            time.sleep(1)
            
def checkFile():
    filenames = os.listdir(folder_path)
    files = [f for f in filenames if os.path.isfile(os.path.join(folder_path, f))]
    # 打印所有文件
    for file in files:
        if (re.findall('.bin',file) and re.findall('OTA',file)) or re.findall('Sound',file):
            file_path = os.path.join(folder_path, file)
            file_size = os.path.getsize(file_path)
            md5 = calculate_file_md5(file_path=folder_path+'\\'+file)
            url = file.replace('$','%24')
            # print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())+'  '+file)
            if len(url.split('%24')) > 1:
                module = url.split('%24')[1].split('_')[0]
                version = url.split('_')[len(url.split('_'))-1].split('.bin')[0]
            elif re.findall('Sound',url):
                module = 8
                version = url.split('_')[len(url.split('_'))-1].split('.bin')[0]
            elif re.findall('OEM',url) or re.findall('_4_',url):
                module = 4
                version = url.split('OTA_')[len(url.split('OTA_'))-1].split('.bin')[0]
            url = url.replace('%24','_')
            # if md5 != config.get('md5',module):
            #     print('md5不一致')
            # elif md5 == config.get('md5',module):
            #     # print('md5一致')
            print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())+'  '+url,module,version,md5)

def create():
    otaModuleList = []
    currentModelList = []
    updateModule = config.get('cfg','moduleCode').replace('[','').replace(']','')
    #根据updateModule判断需要升级的模组
    if updateModule == 'all':
        module = config.items('firmwareId')
        for i in range (len(module)):
            
            otaModuleList.append({
             "moduleCode": config.items('fileVer')[i][0],
             "moduleName": config.items('moduleName')[i][1],
             "firmwareId": config.items('firmwareId')[i][1],
             "fileVer": config.items('fileVer')[i][1]
            })
            currentModelList.append({"moduleCode": config.items('fileVer')[i][0], "version": "V1.44.004"})
            print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())+'   '+config.items('moduleName')[i][1]+' = '+config.items('fileUrl')[i][1])

            
    elif updateModule != 'all':
        updateModuleList = updateModule.split(',')
        for i in range(len(updateModuleList)):
            #判断是否有对应modulecode
            if config.has_option('fileVer', updateModuleList[i]):
                otaModuleList.append({
                    "moduleCode": updateModuleList[i],
                    "moduleName": config.get('moduleName',updateModuleList[i]),
                    "firmwareId": config.get('firmwareId',updateModuleList[i]),
                    "fileVer": config.get('fileVer',updateModuleList[i])
                    })
                print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())+'   '+config.get('moduleName',updateModuleList[i])+' = '+config.get('fileUrl',updateModuleList[i]))
                currentModelList.append({"moduleCode": updateModuleList[i], "version": "V1.44.004"})

            else:
                print('非法moduleCode')
                exit()
    conn = http.client.HTTPConnection("39.108.235.188", 8094)
    # print(currentModelList)
    # print(otaModuleList)
    headers = {
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Host': '39.108.235.188:8094',
    'Connection': 'keep-alive'
    }

    payload = json.dumps({
    "taskName": config.get('cfg','taskName'),
    "upgradeType": int(config.get('cfg','upgradeType')),
    "retry": int(config.get('cfg','retry')),
    "timeout": int(config.get('cfg','timeout')),
    "createUser": config.get('cfg','user'),
    "otaModuleList": otaModuleList,
    "deviceList": [{"esn": config.get('cfg','esn'),"currentModelList": currentModelList}],
    "retryInterval": int(config.get('cfg','retryInterval')),
    "customerApp": 1,
    "productType": 1
})
    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())+'  '+payload)
    conn.request("POST", "/ota/taskConfig/addTask", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())+'  '+data.decode("utf-8"))

if __name__ == '__main__':
    cfg_path = 'D:\\code\\ota.conf'
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(cfg_path,encoding='utf-8')
    folder_path = config.get('cfg','folder_path')
    fileUrl = config.get('cfg','fileUrl')
    access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', config.get('cfg','access_key_id'))
    access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', config.get('cfg','access_key_secret'))
    bucket_name = os.getenv('OSS_TEST_BUCKET', config.get('cfg','bucket_name'))
    endpoint = os.getenv('OSS_TEST_ENDPOINT', config.get('cfg','endpoint'))
    num = input('检查升级文件信息：1\n上传固件：2\n创建升级任务：3\n')
    # while True:
    if num == '1':
        checkFile()
    elif num == '2':
        upload()
    elif num == '3':
        create()
    
