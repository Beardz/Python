import csv
import uiautomator2 as u2
import time, datetime
import serial
import threading
import re
import logging
import traceback
import subprocess
import configparser


class WIFIChange():

    def __init__(self):
        global t,refresh,refresh_overtime,success,wifi_index,fileName,connect,connect_flag,plu,kind,wifi_index,flag,WIFI_IP_List,WIFI_List,WIFI_PWD
        t = 0
        refresh = 0
        refresh_overtime = False
        fileName = '-switch_wifi-'
        success = 0
        wifi_index = 0
        connect_flag = 0
        connect = 0
        config = configparser.ConfigParser()
        config.read('D:\code\python\smartdoor\wifi.conf',encoding='utf-8')
        plu = config.get('plu','name')
        kind = config.get('plu','door')
        wifi = config.options('wifi')
        WIFI_List = []
        WIFI_IP_List = []
        WIFI_PWD = []
        for i in range(len(wifi)):
            WIFI_List.append(wifi[i])
            WIFI_IP_List.append(config.get('ip',wifi[i]))
            WIFI_PWD.append(config.get('wifi',wifi[i]))
        flag = WIFI_List[0]
        self.logger = logging.getLogger(currentTime+ fileName +'.log')
        Terminalformat = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        format = logging.Formatter('%(asctime)s - %(message)s')
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(Terminalformat)
        th = logging.FileHandler(filename=currentTime+ '.log',encoding='utf-8')
        th.setFormatter(format)
        self.logger.addHandler(sh)
        # self.logger.addHandler(th)
        time.sleep(3)
        subprocess.run('python -m uiautomator2 init')
        self.d = u2.connect()

        with open(currentTime + '.csv', 'a', newline='',encoding='UTF-8') as f:
            row = ['时间','结果', '成功率','成功次数','总次数']
            file = csv.writer(f)
            file.writerow(row)

    def restartAPP(self):
        # 杀掉正在运行的程序
        self.d.app_stop("com.xiaomi.smarthome")
        # 启动目标程序
        self.d.app_start("com.xiaomi.smarthome",use_monkey=True)

    def screenShot(self, reason=''):
        now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        image = self.d.screenshot()
        image.save(reason + now + ".jpg")

    def TryIn(self):
        # 插件位置
        a = self.d(text=plu)
        if a.exists(timeout=3):
            a.click()
        else:
            for i in range(5):
                self.d.swipe_ext("up", scale=0.6)
                if not a.exists(timeout=3):
                    continue
                else:
                    a.click()
                    break

        if self.d(text='稍后再说').exists(timeout=10):
            self.d(text='稍后再说').click()

    def settingIn(self):
        time.sleep(1)
        if self.d(description='消息中心').exists:
            self.d(text=plu).click()
            if self.d(text='稍后再说').exists(timeout=5):
                self.d(text='稍后再说').click()
        # self.d.click(0.5, 0.06)
        self.d(description="更多设置").click()
        time.sleep(1)
        if kind == 'P50':
            s = self.d(text='设备信息')
            if s.exists(timeout=5):
                s.click()
                time.sleep(1)
                if self.d(text="Wi-Fi").exists(timeout=2):
                    self.d(text='Wi-Fi').click()
        elif kind == 'U' or kind == 'P1' or kind == 'Y':
            if self.d(text="网络设置").exists(timeout=2):
                    self.d(text='网络设置').click()

    def switchWIFI(self):
        global flag,t,connect_flag,connect,wifi_index,WIFI_List,success,refresh_overtime,WIFI_PWD
        if kind == 'P50':
            if self.d(text="Wi-Fi").exists(timeout=2):  
                self.d(text='Wi-Fi').click()
            if self.d(text='已连接').exists(timeout=15):
                if not self.d(text='更换Wi-Fi').exists:
                    self.d.swipe_ext("up", scale=0.6)
                self.d(text='更换Wi-Fi').click()
            else:
                pass
        elif kind == 'U' or kind == 'P1'or kind == 'Y' :
            if  self.d(text='更换Wi-Fi').exists:   
                self.d(text='更换Wi-Fi').click()
        t1 = threading.Thread(target=self.getBluetooth)
        t1.start()
        if self.d(text='选择Wi-Fi',index=0).exists(timeout=45):
            self.d(text='选择Wi-Fi',index=0).click()
            time.sleep(3)
            self.click_WiFi(flag)
            # self.refreshWIFI(flag)
            if refresh_overtime == True:
                self.logger.warning(u'刷新未找到WiFi，杀掉app')
                self.errorReTry()
                refresh_overtime = False
            elif self.d(text = WIFI_List[wifi_index]).exists(timeout=2) :
                if self.d(text='请输入密码').exists(timeout=2):
                    self.d(className='android.widget.RelativeLayout',index = 2).click()
                    time.sleep(1)
                    # self.d.send_keys(text=WIFI_PWD[wifi_index],clear=True)
                    self.d(focused=True).set_text(WIFI_PWD[wifi_index])
                    time.sleep(1)
                    self.d(description='完成').click()
                if self.d(text='下一步').exists(timeout=1):
                    self.d(text='下一步').click()
                    begTime = time.time()
                    # self.match_log()
                    while True:
                        endTime = time.time()
                        if self.d(text='设备添加成功').exists or connect != 0:
                            t+=1
                            success+=1
                            endTime = time.time()
                            linkTime = endTime - begTime
                            percent = round(success*100/t,2)
                            self.logger.info(u'WiFi更换成功')
                            self.write_csv(kind1=flag+'更换成功',time1=str(percent)+'%',s=success,t=t)
                            time.sleep(3)
                            break
                        elif self.d(text='设备连接网络超时 查看原因').exists:
                            t+=1
                            self.logger.warning(u'设备连接网络超时')
                            percent = round(success*100/t,2)
                            self.write_csv(kind1=flag+'设备连接网络超时',time1=str(percent)+'%',s=success,t=t)
                            self.d(className='android.widget.ImageView',index=0).click()
                            break
                        elif endTime - begTime > 45:
                            t+=1
                            self.logger.warning(u'WiFi更换失败')
                            percent = round(success*100/t,2)
                            self.write_csv(kind1=flag+'更换失败',time1=str(percent)+'%',s=success,t=t)
                            self.d(className='android.widget.ImageView', index=0).click()
                            break
                        else:
                            pass
                else:
                    self.logger.error(u'未知原因')
                    self.screenShot(reason='未知原因')
                    self.errorReTry()
            else:
                self.logger.error(u'未知原因')
                self.screenShot(reason='未知原因')
                self.errorReTry()
        else:
            if self.d(text='更换Wi-Fi').exists and connect_flag == 1:
                self.logger.error(u'未知原因')
                pass
            elif self.d(text='更换Wi-Fi').exists and connect_flag == 0:
                self.logger.error(u'蓝牙连接失败')
                self.errorReTry()
            else:
                self.logger.error(u'未知原因')
                self.screenShot(reason='未知原因')
                self.errorReTry()
        wifi_index+=1
        if wifi_index >= len(WIFI_List):
            wifi_index = 0
        flag=WIFI_List[wifi_index]

    def click_WiFi(self,flag):
        global refresh,wifi_index,WIFI_List,refresh_overtime
        a = self.d(text=WIFI_List[0])
        b = self.d(text=WIFI_List[1])
        c = self.d(text='yunlu-guest')
        d = self.d(text=WIFI_List[wifi_index])
        if self.d(text='选择Wi-Fi',index=0).exists(timeout=2):
            self.d(text='选择Wi-Fi',index=0).click()
        if a.exists or b.exists or c.exists or d.exists:
            if not d.exists:
                self.logger.warning(u'未找到WiFi')
                # t += 1
                self.d.swipe(0.483,0.607,0.446, 0.875)
                refresh += 1
                time.sleep(6)
                # self.click_WiFi(flag)
                if refresh == 3:
                    refresh_overtime = True
                    refresh = 0
                else:
                    self.click_WiFi(flag)
            else:
                refresh_overtime = False
                refresh = 0
                d.click()
                if self.d(text="路由器名称包含非英文字符").exists:
                    # self.logger.warning(u'路由器名称包含非英文字符')
                    self.d(text='确定').click()
        else:
            self.logger.error(u'未知位置/未找到WiFi')
            self.screenShot(reason='未找到WiFi')

    def write_csv(self, kind1, time1='',s='',t=''):
        global fileName
        with open(currentTime + '.csv', 'a', newline='',encoding='UTF-8') as f:
            row = [time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()), kind1, time1,s,t]
            file = csv.writer(f)
            file.writerow(row)

    def errorReTry(self):
        try:
            self.restartAPP()
            self.TryIn()
            self.settingIn()
        except:
            self.logger.error('\n'+traceback.format_exc())

    def getBluetooth(self):
        global connect_flag
        if self.d(text='同步数据中，请稍后再试(10003)').exists(timeout=45):
            time.sleep(2)
            self.d(text='更换Wi-Fi').click()
        else:
            connect_flag = 1

    def write_log(self, write_info="", logname="", write_way='a+', log_print=False, time_mark=True):
            try:
                with open(logname, write_way) as fl:
                # with open(log_path + "\\" + logname, write_way) as fl:
                    if time_mark:  # 日志中记录时间
                        Current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        # fl.write("[--------------------------" + Current_time + "--------------------------]"+ "\n" + (str(write_info) + "\n").replace("\r", ""))
                        fl.write((str(write_info) + "\n").replace("\r", ""))
                    else:
                        fl.write(str(write_info))
                if log_print:  # 日志打印在控制台
                    print(str(write_info).strip())
                return True
            except:
                return False

    def match_log(self):
        global com,flag,connect,WIFI_List,wifi_index
        btime = time.time()
        if com !='':
            ser = serial.Serial(com,'115200',timeout=0.00001)
        while True:
            etime = time.time()
            if etime - btime >= 60:
                self.logger.error(u'wifi连接失败')
                break
            else:
                read = ser.readlines()
                rsp = '\n'.join([str(item).replace(r"\r", "").replace(r"\n'", "").replace(r"b'", "").replace(r"\x1b", "").replace("[0m", "").replace("[33m", "") for item in read])
                if rsp != '':
                    self.write_log(write_info=rsp,logname=com+'_'+currentTime+'.log')
                if rsp != '':
                    if kind == 'P50':
                        success_flag = re.findall("My Lan IP : "+WIFI_IP_List[wifi_index],rsp)
                        wifi_a = re.findall("My Lan IP : "+WIFI_IP_List[0],rsp)
                        wifi_b = re.findall("My Lan IP : "+WIFI_IP_List[1],rsp)
                        wifi_c = re.findall("My Lan IP : "+WIFI_IP_List[2],rsp)
                    if kind == 'P1' or kind == 'Y' or kind == 'U':
                        success_flag = re.findall("prepare online event information ip="+WIFI_IP_List[wifi_index],rsp)
                        wifi_a = re.findall("online event information ip="+WIFI_IP_List[0],rsp)
                        wifi_b = re.findall("online event information ip="+WIFI_IP_List[1],rsp)
                        wifi_c = re.findall("online event information ip="+WIFI_IP_List[2],rsp)
                    if success_flag:
                        self.logger.info(WIFI_List[wifi_index]+u'连接成功')
                        break
                    elif wifi_a and wifi_index!=0 :
                        self.logger.warning(WIFI_List[wifi_index]+u'连接失败，'+u'连回'+WIFI_List[0])
                        break
                    elif wifi_b and wifi_index!=1 :
                        self.logger.warning(WIFI_List[wifi_index]+u'连接失败，'+u'连回'+WIFI_List[1])
                        break
                    elif wifi_c and wifi_index!=2 :
                        self.logger.warning(WIFI_List[wifi_index]+u'连接失败，'+u'连回'+WIFI_List[2])
                        break
                    
        ser.close()


if __name__ == '__main__':
    currentTime = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
    com = 'com16'
    r = WIFIChange()
    while True:
        try:
            r.switchWIFI()
        except:
            r.logger.error('\n'+traceback.format_exc())
            r.screenShot()
            pass

