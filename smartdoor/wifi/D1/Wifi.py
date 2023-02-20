import csv
import uiautomator2 as u2
import time, datetime
import serial
import threading
import re
import logging
import traceback


class WIFIChange():

    def __init__(self):
        self.logger = logging.getLogger(currentTime+ fileName +'.log')
        Terminalformat = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        format = logging.Formatter('%(asctime)s - %(message)s')
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(Terminalformat)
        th = logging.FileHandler(filename=currentTime+ '.log',encoding='utf-8')
        th.setFormatter(format)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)
        time.sleep(3)
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
        self.d.click(0.5, 0.06)
        self.d(description="更多设置").click()
        time.sleep(1)
        s = self.d(text='设备信息')
        if s.exists(timeout=5):
            s.click()
            time.sleep(1)
            if self.d(text="Wi-Fi").exists(timeout=2):
                self.d(text='Wi-Fi').click()
        else:
            self.settingIn()

    def switchWIFI(self):
        global flag,t,WIFI_A,WIFI_B,connect_flag,connect,wifi_index,WIFI_List,success,flash_overtime
        if self.d(text="Wi-Fi").exists(timeout=2):  
            self.d(text='Wi-Fi').click()
        if self.d(text='已连接').exists(timeout=15):
            if not self.d(text='更换Wi-Fi').exists:
                self.d.swipe_ext("up", scale=0.6)
            self.d(text='更换Wi-Fi').click()
        else:
            pass
        t1 = threading.Thread(target=self.getBluetooth)
        t1.start()
        if self.d(text='选择Wi-Fi',index=0).exists(timeout=45):
            self.d(text='选择Wi-Fi',index=0).click()
            time.sleep(5)
            self.click_WiFi(flag)
            # self.flashWIFI(flag)
            if flash_overtime == True:
                self.logger.warning(u'刷新未找到WiFi，杀掉app')
                self.errorReTry()
                flash_overtime = False
            elif self.d(text='下一步').exists(timeout=1):
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
                self.logger.error(u'未点击下一步/未知原因')
                self.screenShot(reason='未点击下一步或未知原因')
                self.errorReTry()
        else:
            if self.d(text='更换Wi-Fi').exists and connect_flag == 1:
                self.logger.error(u'未点击更换Wi-Fi/未知原因')
                self.switchWIFI()
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
        global WIFI_A,WIFI_B,flash,wifi_index,WIFI_List,flash_overtime
        a = self.d(text=WIFI_A)
        b = self.d(text=WIFI_B)
        c = self.d(text='yunlu-guest')
        d = self.d(text=WIFI_List[wifi_index])
        if a.exists or b.exists or c.exists or d.exists:

            if not d.exists:
                self.logger.warning(u'未找到WiFi')
                # t += 1
                self.d.swipe(0.483,0.607,0.446, 0.875)
                flash += 1
                time.sleep(6)
                # self.click_WiFi(flag)
                if flash == 3:
                    flash_overtime = True
                    flash = 0
                else:
                    self.click_WiFi(flag)
            else:
                flash_overtime = False
                d.click()
                if self.d(text="路由器名称包含非英文字符").exists:
                    # self.logger.warning(u'路由器名称包含非英文字符')
                    self.d(text='确定').click()
        else:
            self.logger.error(u'未知位置/未找到WiFi')
            self.screenShot(reason='未找到WiFi')

    def flashWIFI(self,flag):
        global WIFI_A,WIFI_B,t,wifi_index,WIFI_List
        a = self.d(text=WIFI_A)
        b = self.d(text=WIFI_B)
        c = self.d(text='yunlu-guest')
        d = self.d(text=WIFI_List[wifi_index])
        if self.d(text="路由器名称包含非英文字符").exists:
            self.logger.warning(u'路由器名称包含非英文字符')
            self.d(text='确定').click()
        # 若是5G WIFI则下滑刷新重新选择WIFI
        if self.d(text='确定').exists(timeout=3):
            self.d(text='确定').click()
            if a.exists or b.exists or c.exists:
                self.logger.warning(u'未找到WiFi(2.4G)')
                self.d.swipe(0.483,0.607,0.446, 0.875)
                time.sleep(6)
        
                self.click_WiFi(flag)
                self.flashWIFI(flag)
            else:
                self.logger.error(u'未知位置/未找到WiFi')
                self.screenShot(reason='未找到WiFi')
        else:
            pass

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
            self.errorReTry()

    def getBluetooth(self):
        global connect_flag
        if self.d(text='同步数据中，请稍后再试(10003)').exists(timeout=45):
            time.sleep(2)
            self.d()
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
            ser = serial.Serial(com,'1500000',timeout=0.00001)
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
                    # print(WIFI_List[wifi_index])
                    #success_flag = re.findall("\"method\":\"_internal.wifi_connected\",\"params\":{\"ssid\":\""+WIFI_List[wifi_index].encode(), rsp)
                    #cloud_connect = re.findall("\"method\": \"local.status\", \"params\": \"cloud_connected\"",rsp)
                    success_flag = re.findall("My Lan IP : "+WIFI_IP_List[wifi_index],rsp)
                    wifi_a = re.findall("My Lan IP : "+WIFI_IP_List[0],rsp)
                    wifi_b = re.findall("My Lan IP : "+WIFI_IP_List[1],rsp)
                    wifi_c = re.findall("My Lan IP : "+WIFI_IP_List[2],rsp)
                    # reconnect_flag = re.findall("My Lan IP : "+WIFI_B_IP, rsp)
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
                    
                        # self.write_csv(kind1=flag+'更换成功（日志）')
                    # elif cloud_connect :
                    #     self.logger.info(u'cloud_connect')
                    #     # self.write_csv(kind1=flag+'更换成功')
                    #     connect = 1
                    #     break
        ser.close()


if __name__ == '__main__':
    currentTime = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
    t = 0
    flash = 0
    flash_overtime = False
    success = 0
    plu = '云鹿智能门P2'
    fileName = '-switch_wifi-'
    WIFI_A = 'Xiaomi_F49A'
    WIFI_B = 'NovaDoor'
    WIFI_C = 'yunding'
    # WIFI_C = 'Redmi'
    # WIFI_D = 'yunlu'
    # WIFI_E = 'yunlu'
    WIFI_A_IP = '192.168.28.109'
    WIFI_B_IP = '192.168.50.231'
    WIFI_C_IP = '192.168.0.115'
    WIFI_List = [WIFI_A,WIFI_B,WIFI_C]
    WIFI_IP_List = [WIFI_A_IP,WIFI_B_IP,WIFI_C_IP]
    wifi_index = 0
    # send_key = False
    flag = WIFI_List[0]
    connect_flag = 0
    connect = 0
    com = 'com18'
    r = WIFIChange()
    # s = WIFIChange()
    # th = threading.Thread(target=s.main())
    # th = threading.Thread(target=r.match_log())
    # th.start()

    while True:
        try:
            # r.restartAPP()
            # r.TryIn()
            # r.settingIn()
            r.switchWIFI()
        except:
            r.logger.error('\n'+traceback.format_exc())
            r.screenShot()
            # r.errorReTry()
            pass


