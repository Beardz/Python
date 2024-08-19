import serial
import time
import logging
import re
import datetime
import traceback

class match_log():
    def __init__(self) -> None:
        self.logger = logging.getLogger(currentTime +'.log')
        Terminalformat = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        format = logging.Formatter('%(asctime)s - %(message)s')
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(Terminalformat)
        path = 'com ' + com.removeprefix('com') + '\\'
        th = logging.FileHandler(filename='D:\\code\\logs\\'+path+com+'_'+currentTime+ '.log',encoding='utf-8')
        th.setFormatter(format)
        # self.logger.addHandler(sh)
        self.logger.addHandler(th)


    def match_log(self,kind,com):

        if kind == 'master':
            ser = serial.Serial(com,'921600',timeout=0.05)
        elif kind == 'camera':
            ser = serial.Serial(com,'1500000',timeout=0.05)
        elif kind == 'opener':
            ser = serial.Serial(com,'921600',timeout=0.05)
        elif kind == 'ble':
            ser = serial.Serial(com,'921600',timeout=0.05)
        t = time.time()
        while True:
            read = ser.readlines()
            rsp = '\n'.join([
            # str(item).replace(r"\r", "").replace(r"\n'", "").replace(r"b'", "").replace(r"\x1b", "").replace("[0m", "").replace("[0;36m", "").replace("[36;22m","").replace("[33;22m","").replace("[1;32m","").replace("[m","").replace("[1;35m","").replace("[0;35m","").replace("[1;33m","") for item in read])
            str(item).replace(r"\r", "").replace(r"\n'", "").replace(r"\t","") for item in read])
            # str(item).replace(r"\n'", "") for item in read])
            st = re.sub(r'\[\d{1,2}\;\d{1,2}m|\[\wm|\[m|\\x1b|b\'|\', b\'',"",rsp)
            # if time.time() - t > 10:
            #     t = time.time()
            #     ser.write(str('killall ipc\n').encode('utf-8'))
            if rsp != '':
                self.logger.info(st)
            if kind == 'master':
                if re.findall('door opener mode is : 1',st):
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + "Hand Open Door")
                    self.logger.info(u"手动开门")
                if re.findall('door opener mode is : 0',st):
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + "Auto Open Door")
                    self.logger.info(u"自动开门")
                if re.findall(lockfunction,st):
                    val = re.search(r'(?<=ParamModify index:05, value:)\d{1,2}',st).group(0)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + val)
                    if val == '00':
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"Auto Unlock")
                        self.logger.info(u"Auto Unlock")
                    elif val == '01':
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"Hand Unlock")
                        self.logger.info(u"Hand Unlock")
                if re.findall(doubleCheck,st):
                    val = re.search(r'(?<=ParamModify index:08, value:)\d{1,2}',st).group(0)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + val)
                    if val == '00':
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"Close Doublecheck")
                        self.logger.info(u"Close Doublecheck")
                    elif val == '01':
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"Open Doublecheck")
                        self.logger.info(u"Open Doublecheck")
                if re.findall(faceRecognize,st):
                    val = re.search(r'(?<=ParamModify index:0F, value:)\d{1,2}',st).group(0)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + val)
                    if val == '00':
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"Close FaceRecognize")
                        self.logger.info(u"Close FaceRecognize")
                    elif val == '01':
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"Open FaceRecognize")
                        self.logger.info(u"Open FaceRecognize")
                if re.findall(saftyfunction,st):
                    val = re.search(r'(?<=ParamModify index:06, value:)\d{1,2}',st).group(0)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + val)
                    if val == '00':
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"Close Defense")
                        self.logger.info(u"Close Defense")
                    elif val == '01':
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"Open Defense")
                        self.logger.info(u"Open Defense")
                if re.findall(sensiticity,st):
                    val = re.search(r'(?<=ParamModify index:44, value:)\d{1,2}',st).group(0)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + val)
                    if val == '00':
                        self.logger.info(u"Close Sensiticity")
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"Close Sensiticity")
                    elif val == '01':
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"High Sensiticity")
                        self.logger.info(u"High Sensiticity")
                    elif val == '02':
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"Low Sensiticity")
                        self.logger.info(u"Low Sensiticity")
                if re.findall(faceAlarm,st):
                    val = re.search(r'(?<=ParamModify index:45, value:)\d{1,2}',st).group(0)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + val)
                    if val == '00':
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"High invade")
                        self.logger.info(u"High invade")
                    elif val == '01':
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"Mid invade")
                        self.logger.info(u"Mid invade")
                    elif val == '02':
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + u"Low invade")
                        self.logger.info(u"Low invade")
                if re.findall(out_time_unlock,st):
                    val = int(re.search(r'(?<=ParamModify index:52, value:)\w{1,2}',st).group(0),16)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + str(val))
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + "out_time_unlock:%s"%val)
                    self.logger.info(u"out_time_unlock:%s"%val)
                if re.findall(indoorVolume,st):
                    val = int(re.search(r'(?<=ParamModify index:03, value:)\w{1,2}',st).group(0),16)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + str(val))
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + "indoorVolume:%s"%val)
                    self.logger.info(u"indoorVolume:%s"%val)
                if re.findall(outdoorVolume,st):
                    val = int(re.search(r'(?<=ParamModify index:02, value:)\w{1,2}',st).group(0),16)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + str(val))
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + "outdoorVolume:%s"%val)
                    self.logger.info(u"outdoorVolume:%s"%val)

            if kind == 'opener':
                if re.findall('DoorOpener message publish state2 :4',st):
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '自动模式')
                    self.logger.info(u"自动模式")
                if re.findall('DoorOpener message publish state2 :5',st):
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '手动模式')
                    self.logger.info(u"手动模式")
                if re.findall('SetupParam type = 11, SetupParam = 1',st):
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '右开')
                    self.logger.info(u"右开")
                if re.findall('SetupParam type = 11, SetupParam = 0',st):
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '左开')
                    self.logger.info(u"左开")   
                if re.findall(r'SetupParam type = 12, SetupParam = \d{1,2}',st):
                    Param = re.search(r'SetupParam = \d{1,2}',st).group(0).split().pop()
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '开门类型:%s'%Param)
                    if Param == '0' :
                        self.logger.info(u"单门:"+Param)
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '单门')
                    elif Param == '1' :
                        self.logger.info(u"双门主动:"+Param)
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '双门主动')
                    elif Param == '2' :
                        self.logger.info(u"双门从动:"+Param)         
                        print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '双门从动')
                if re.findall(r'SetupParam type = 1, SetupParam = \d{1,2}',st):
                    Param = re.search(r'SetupParam = \d{1,2}',st).group(0).split().pop()
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '开门速度:%s'%Param)
                    self.logger.info(u"开门速度"+Param)   
                if re.findall(r'SetupParam type = 2, SetupParam = \d{1,2}',st):
                    Param = re.search(r'SetupParam = \d{1,2}',st).group(0).split().pop()
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '关门速度:%s'%Param)
                    self.logger.info(u"关门速度"+Param)   
                if re.findall(r'SetupParam type = 3, SetupParam = \d{1,2}',st):
                    Param = re.search(r'SetupParam = \d{1,2}',st).group(0).split().pop()
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '开门缓行角度:%s'%Param)
                    self.logger.info(u"开门缓行角度"+Param)   
                if re.findall(r'SetupParam type = 4, SetupParam = \d{1,2}',st):
                    Param = re.search(r'SetupParam = \d{1,2}',st).group(0).split().pop()
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '关门缓行角度:%s'%Param)
                    self.logger.info(u"关门缓行角度"+Param)   
                if re.findall(r'SetupParam type = 5, SetupParam = \d{1,2}',st):
                    Param = re.search(r'SetupParam = \d{1,2}',st).group(0).split().pop()
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '保持开门时间:%s'%Param)
                    self.logger.info(u"保持开门时间"+Param)   
                if re.findall(r'SetupParam type = 6, SetupParam = \d{1,2}',st):
                    Param = re.search(r'SetupParam = \d{1,2}',st).group(0).split().pop()
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '推即开触发角度:%s'%Param)
                    self.logger.info(u"推即开触发角度"+Param)   
                if re.findall(r'SetupParam type = 7, SetupParam = \d{1,2}',st):
                    Param = re.search(r'SetupParam = \d{1,2}',st).group(0).split().pop()
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '开门安全光线检测范围:%s'%Param)
                    self.logger.info(u"开门安全光线检测范围"+Param)   
                if re.findall(r'SetupParam type = 8, SetupParam = \d{1,2}',st):
                    Param = re.search(r'SetupParam = \d{1,2}',st).group(0).split().pop()
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '关门安全光线检测范围:%s'%Param)
                    self.logger.info(u"关门安全光线检测范围"+Param)   
                if re.findall(r'SetupParam type = 9, SetupParam = \d{1,2}',st):
                    Param = re.search(r'SetupParam = \d{1,2}',st).group(0).split().pop()
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '慢速扭矩:%s'%Param)
                    self.logger.info(u"慢速扭矩"+Param)   
                if re.findall(r'SetupParam type = 10, SetupParam = \d{1,2}',st):
                    Param = re.search(r'SetupParam = \d{1,2}',st).group(0).split().pop()
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '关门紧闭力:%s'%Param)
                    self.logger.info(u"关门紧闭力"+Param)   

            if kind == 'camera':
                if re.findall('GetMqttInfo Failed',st):
                    self.logger.error(u"GetMqttInfo Failed")
                if re.findall('GetMqttInfo Success',st):
                    self.logger.debug(u"GetMqttInfo Success")
                if re.findall(nigteVersion,st):
                    val = re.search(r'(?<=SetCamera\)nightVision:)\d',st).group(0)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + 'nightVision:'+val)
                    if val == '0':
                        print('始终关闭')
                        self.logger.info(u"始终关闭")
                    elif val == '1':
                        print('自动切换')
                        self.logger.info(u"自动切换")
                    elif val == '2':
                        print('始终开启')
                        self.logger.info(u"始终开启")
                if re.findall(outsideCatEyeVoice,st):
                    val = re.search(r'(?<=SetCamera\)outsideCatEyeVoice:)\d{1,3}',st).group(0)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + 'outsideCatEyeVoice:'+val)
                    self.logger.info(u""+val+"")
                if re.findall(recordDuration,st):
                    val = re.search(r'(?<=SetCamera\)recordDuration:)\d{1,2}',st).group(0)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + 'recordDuration:'+val)
                    self.logger.info(u""+val+"")
                if re.findall(stayDuration,st):
                    val = re.search(r'(?<=[pcLockStr:{"func":"setLock","msgId":\d{1,3},"params":{"stayDuration":])"stayDuration":\d{1,2}',st).group(0)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + val)
                    self.logger.info(u""+val+"")
                if re.findall(recordInterval,st):
                    val = re.search(r'(?<=[pcLockStr:{"func":"setLock","msgId":\d{1,3},"params":{"recordInterval":])"recordInterval":\d{1,3}',st).group(0)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + val)
                    self.logger.info(u""+val+"")
                if re.findall(sentsitiveDetection,st):
                    val = re.search(r'(?<=[pcLockStr:{"func":"setLock","msgId":\d{1,3},"params":{"sentsitiveDetection":])"sentsitiveDetection":\d',st).group(0)
                    print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + val)
                    self.logger.info(u""+val+"")
                


    def write_log(self, write_info="", logname="", write_way='a+', log_print=False, time_mark=True):
        try:
            with open(logname, write_way) as fl:
            # with open(log_path + "\\" + logname, write_way) as fl:
                if time_mark:  # 日志中记录时间
                    Current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # fl.write("[------------" + Current_time + "------------]"+ "\n" + (str(write_info) + "\n").replace("\r", ""))
                    fl.write((str(write_info) + "\n").replace("\r", ""))
                else:
                    fl.write(str(write_info))
            if log_print:  # 日志打印在控制台
                print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + str(write_info).strip())
            return True
        except:
            return False

if __name__ == '__main__':
    currentTime = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
    lockfunction = r'ParamModify index:05, value:\d{1,2}'
    doubleCheck = r'ParamModify index:08, value:\d{1,2}'
    faceRecognize = r'ParamModify index:0F, value:\d{1,2}'
    saftyfunction = r'ParamModify index:06, value:\d{1,2}'
    sensiticity = r'ParamModify index:44, value:\d{1,2}'
    faceAlarm = r'ParamModify index:45, value:\d{1,2}'
    out_time_unlock = r'ParamModify index:52, value:\w{1,2}'
    indoorVolume = r'ParamModify index:03, value:\w{1,2}'
    outdoorVolume = r'ParamModify index:02, value:\w{1,2}'
    nigteVersion = r'SetCamera\)nightVision:'
    recordDuration = r'SetCamera\)recordDuration:'
    outsideCatEyeVoice = r'SetCamera\)outsideCatEyeVoice:'
    stayDuration = r'{"func":"setLock","msgId":\d{1,3},"params":{"stayDuration":\d{1,2}'
    recordInterval = r'{"func":"setLock","msgId":\d{1,3},"params":{"recordInterval":\d{1,2}'
    sentsitiveDetection = r'{"func":"setLock","msgId":\d{1,3},"params":{"sentsitiveDetection":\d'
    com = 'com3'
    kind = 'master'
    com = 'com5'
    kind = 'opener'
    # com = 'com6'
    # kind = 'camera'
    r = match_log()
    while True:
        try:
            r.match_log(kind,com)
        except:
            print(time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()) + '  ' + '\n'+traceback.format_exc())
            pass