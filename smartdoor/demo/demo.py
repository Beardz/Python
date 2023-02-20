#coding=utf8
import csv
import re
import traceback
import uiautomator2 as u2
import time,datetime
import logging
import os
import threading
import serial

class Demo():
    def __init__(self):
        global logger
        logger = logging.getLogger(currentTime+'-'+ fileName + '.log')
        format = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        terminalformat = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(terminalformat)
        th = logging.FileHandler(filename=currentTime+'-'+ fileName + '.log',encoding='utf-8')
        th.setFormatter(format)
        logger.addHandler(sh)
        logger.addHandler(th)
        # subprocess.run('python -m uiautomator2 init')
        time.sleep(3)
        self.d = u2.connect(device)
        # self.restartAPP()
        # threading.Thread(target=self.PopupClick).start()
        with open(currentTime+'-'+fileName+'.csv', 'a', newline='',encoding='UTF-8') as f:
                row = ['时间','次数','结果','蓝牙连接时间','5s内','10s内','20s内','20s以上','平均时间','成功次数']
                file = csv.writer(f)
                file.writerow(row)


    def PopupClick(self):
        while True:
            try:
                if self.d(text='稍后再说').exists:
                    self.d(text='稍后再说').click()
            except:
                pass

# 重启app
    def restartAPP(self):
        self.d.app_stop("com.xiaomi.smarthome")
        time.sleep(15)
        self.d.app_start("com.xiaomi.smarthome",use_monkey=True)
        start = time.time()
        end = time.time()
        while True:
            end = time.time()
            if end - start > 5:
                break
            elif self.d(text = '取消').exists:
                self.d(text = '取消').click()

# 进入插件
    def TryIn(self):
        global startime
        a = self.d(className='android.widget.TextView', text=plu)
        for i in range(5):
            if not a.exists(timeout=1):
                self.d.swipe_ext("up",scale=0.6)
            else:
                time.sleep(1)
                a.click()
                logger.info(u'进插件')
                # startime = time.time()
                break

# 蓝牙连接并解锁
    def BlueConnectAndUnlock(self):
        global status,t5,t10,t20,outbound,sum,t,i,startime,total
        if self.d(text='小米智能门Pro').exists(timeout=5):
            i+=1
            startime = time.time()
            endtime = time.time()
            if self.d(text='连接中').exists:
                logger.info(u'连接蓝牙中')
                while True:
                    endtime = time.time()
                    if not self.d(text='连接中').exists:
                        endtime = time.time()
                        # time.sleep(1)
                        if self.d(textContains='更新时间：').exists(timeout=1):
                            self.screenShot(reason='蓝牙连接失败')
                            logger.error('蓝牙连接失败')
                            status = 0
                            self.write_csv(kind1='蓝牙连接失败')
                            # self.d(description='返回').click()
                            time.sleep(1)
                            break
                        # self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.ImageView[1]').click()
                        # if self.d(text='蓝牙已连接').exists(timeout=3):
                        if self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').exists or self.d(text='已上锁').exists:
                            logger.info(u'蓝牙连接成功')
                            for j in range(5):
                                if not self.d(text='长按开锁').exists(timeout=1):
                                    self.d.swipe(0.436, 0.867,0.436, 0.227)
                                else:
                                    time.sleep(1)
                                    self.d(text='长按开锁').long_click()
                                    break
                            ti = round(endtime - startime , 2)
                                # print(type(ti))
                            logger.info(u'蓝牙连接时间:%s' %ti)
                            if ti < 5:
                                t5 += 1
                            elif ti < 10:
                                t10+= 1
                            elif ti < 20:
                                t20 += 1
                            else:
                                outbound += 1
                            sum+=ti
                            t+=1
                            total= t5 + t10 + t20 + outbound
                            avg= round(sum / t , 2)
                            if self.d(text='解锁成功').exists(timeout=3):
                                self.screenShot(reason='解锁成功')
                                logger.info(u'解锁成功')
                                status = 0
                                self.write_csv(kind1='蓝牙连接成功',time1=ti,ti5=t5,ti10=t10,ti20=t20,ti60=outbound,avg=avg,total=total)
                            else:
                                self.screenShot(reason='未解锁')
                                logger.error(u'未解锁')
                                status = 0
                                self.write_csv(kind1='未解锁',time1=ti,ti5=t5,ti10=t10,ti20=t20,ti60=outbound,avg=avg,total=total)
                            time.sleep(1)
                            break
                        else:
                            if self.d(text='稍后再说').exists:
                                pass
                            else:
                                self.screenShot(reason='蓝牙连接失败')
                                logger.error('蓝牙连接失败')
                                status = 0
                                self.write_csv(kind1='蓝牙连接失败')
                                # self.d(description='返回').click()
                                time.sleep(1)
                            break
                    elif endtime - startime > 60 :
                        logger.error('蓝牙连接失败')
                        status = 0
                        self.write_csv(kind1='60s未连上')
                        # self.d(description='返回').click()
                        time.sleep(1)
                        break
        elif self.d(description='消息中心').exists:
            logger.warning(u'未成功进入插件')
        else:
            logger.warning(u'未找到插件')
            self.restartAPP()

# 直播时长
    def LiveConnectTime(self):
        global flag,t,i,j,t5,t10,t30,t60
        connect_time= 0
        if self.d(text='小米智能门Pro').exists(timeout=10):
            starttime = time.time()
            aftertime = time.time()
            logger.info(u'进入插件')
            while True:
                if self.d(text='点击重试').exists:
                    # self.screenShot(reason="直播连接失败")
                    break
                elif self.d(text='0 b/s').exists:
                    aftertime = time.time()
                    if aftertime - starttime >= 60:
                        i += 1
                        logger.warning(u'直播黑屏')
                        self.screenShot(reason="直播黑屏")
                        self.write_csv(kind1="直播黑屏")
                        break
                elif self.d(textContains='KB/s').exists() :
                    logger.info(u'直播连接成功')
                    starttime = time.time()
                    while True:
                        if self.d(text="今日来访").exists():
                            if self.d(text='点击重试').exists:
                                i += 1
                                aftertime = time.time()
                                connect_time = aftertime - starttime
                                h = int(connect_time) // 3600
                                m = (int(connect_time) - h * 60) // 60
                                s = int(connect_time) - m * 60
                                self.screenShot(reason="直播连接失败")
                                logger.info(u'直播连接失败')
                                logger.info(u'连接时长:%s'%h+'时%s分'%m+'%s秒'%s)
                                self.write_csv(kind1='%s'%h+'时%s分'%m+'分%s秒'%s)
                                break
                        else:
                            self.screenShot(reason="未知位置")
                            logger.warning(u'未知位置')
                            break
                    break
        else:
            logger.warning(u'未进入插件')

# 切换WiFi
    def SwitchWifi(self):
        global flag,t,WIFI_A,WIFI_B,connect_flag,connect
        # th = threading.Thread(target=self.match_log())
        if not self.d(text='更换Wi-Fi').exists:
            self.d.swipe_ext("up", scale=0.6)
        self.d(text='更换Wi-Fi').click()
        t1 = threading.Thread(target=self.getBluetooth)
        t1.start()
        if self.d(text='选择Wi-Fi',index=0).exists(timeout=45):
            self.d(text='选择Wi-Fi',index=0).click()
            time.sleep(5)
            if flag == WIFI_A:
                self.ClickWIfi(flag)
                self.FlashWifiList(flag)
                flag = WIFI_B

            elif flag == WIFI_B:
                self.ClickWIfi(flag)
                self.FlashWifiList(flag)
                flag = WIFI_A
            if self.d(text='下一步').exists(timeout=1):
                self.d(text='下一步').click()
                begTime = time.time()
                while True:
                    endTime = time.time()
                    if self.d(text='设备添加成功').exists or connect != 0:
                        if connect == 1:
                            logger.info(u'日志显示WiFi更换成功')
                            self.write_csv(kind1=flag+'更换成功（日志）')
                            self.d(className='android.widget.ImageView',index=0).click()
                        elif connect == 2:
                            logger.info(u'连回原来的WiFi')
                            self.write_csv(kind1=flag+'更换失败，连回原来的WiFi')
                            self.d(className='android.widget.ImageView',index=0).click()
                        else:
                            endTime = time.time()
                            linkTime = endTime - begTime
                            logger.info(u'WiFi更换成功')
                            self.write_csv(kind1=flag+'更换成功',time1=linkTime)
                            time.sleep(3)
                        break
                    elif self.d(text='设备连接网络超时 查看原因').exists:
                        logger.warning(u'设备连接网络超时')
                        self.write_csv(kind1=flag+'设备连接网络超时')
                        self.d(className='android.widget.ImageView',index=0).click()
                        break
                    elif endTime - begTime > 120:
                        logger.warning(u'WiFi更换失败')
                        self.write_csv(kind1=flag+'更换失败')
                        self.d(className='android.widget.ImageView', index=0).click()
                        break
                    else:
                        pass
            else:
                logger.error(u'未点击下一步/未知原因')
                self.screenShot(reason='未点击下一步或未知原因')
                self.errorReTry()
        else:
            if self.d(text='更换Wi-Fi').exists and connect_flag == 1:
                logger.error(u'未点击更换Wi-Fi/未知原因')
                self.SwitchWifi()
            elif self.d(text='更换Wi-Fi').exists and connect_flag == 0:
                logger.error(u'蓝牙连接失败')
                self.errorReTry()
            else:
                logger.error(u'未知原因')
                self.screenShot(reason='未知原因')
                self.errorReTry()

# 选择WiFi
    def ClickWIfi(self,flag):
        global WIFI_A,WIFI_B,t
        a = self.d(text=WIFI_A)
        b = self.d(text=WIFI_B)
        c = self.d(text='yunlu-guest')
        if a.exists or b.exists or c.exists:
            if flag == WIFI_A:
                if not b.exists:
                    logger.warning(u'未找到WiFi')
                    t += 1
                    self.d.swipe_ext("down", scale=0.6)
                    time.sleep(6)
                    self.ClickWIfi(flag)
                else:
                    b.click()
            elif flag == WIFI_B:
                if not a.exists:
                    logger.warning(u'未找到WiFi')
                    t += 1
                    self.d.swipe_ext("down", scale=0.6)
                    time.sleep(6)
                    self.ClickWIfi(flag)
                else:
                    a.click()
        else:
            logger.error(u'未知位置/未找到WiFi')
            self.screenShot(reason='未找到WiFi')

# 刷新WiFi列表
    def FlashWifiList(self,flag):
        global WIFI_A,WIFI_B,t
        a = self.d(text=WIFI_A)
        b = self.d(text=WIFI_B)
        c = self.d(text='yunlu-guest')
        if self.d(text="路由器名称包含非英文字符").exists:
            logger.warning(u'路由器名称包含非英文字符')
            self.d(text='确定').click()
        # 若是5G WIFI则下滑刷新重新选择WIFI
        if self.d(text='确定').exists(timeout=3):
            self.d(text='确定').click()
            if a.exists or b.exists or c.exists:
                logger.warning(u'未找到WiFi(2.4G)')
                self.d.swipe(0.483,0.607,0.446, 0.875)
                time.sleep(6)
                if flag == WIFI_A:
                    self.ClickWIfi(flag)
                    self.FlashWifiList(flag)
                elif flag == WIFI_B:
                    self.ClickWIfi(flag)
                    self.FlashWifiList(flag)
            else:
                logger.error(u'未知位置/未找到WiFi')
                self.screenShot(reason='未找到WiFi')
        else:
            pass

# 蓝牙连接状态
    def getBluetooth(self):
        global connect_flag
        if self.d(text='蓝牙连接失败').exists(timeout=45):
            connect_flag = 0
        else:
            connect_flag = 1
# 
    def write_csv(self,kind1='',time1='',ti5='',ti10='',ti20='',ti60='',avg='',total=''):
        global fileName
        if kind1 == '蓝牙连接成功':
            with open(currentTime+'-'+fileName+'.csv', 'a', newline='',encoding='UTF-8') as f:
                row = [time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()),i,kind1,time1,ti5,ti10,ti20,ti60,avg,total]
                file = csv.writer(f)
                file.writerow(row)
        elif kind1 == '未解锁':
            with open(currentTime+'-'+fileName+'.csv', 'a', newline='',encoding='UTF-8') as f:
                row = [time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()),i,kind1,time1,ti5,ti10,ti20,ti60,avg,total]
                file = csv.writer(f)
                file.writerow(row)
        elif kind1 == "直播黑屏":
            with open(currentTime+'-'+fileName+'.csv', 'a', newline='',encoding='UTF-8') as f:
                row = [time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()),'第%s次' % i,kind1]
                file = csv.writer(f)
                file.writerow(row)
        else:
            with open(currentTime+'-'+fileName+'.csv', 'a', newline='',encoding='UTF-8') as f:
                row = [time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()),i,kind1]
                file = csv.writer(f)
                file.writerow(row)

    def screenShot(self,reason = ''):
        now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        image = self.d.screenshot()
        image.save(reason + now + ".jpg")

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
        global com,flag,connect
        while True:
            if com !='':
                ser = serial.Serial(com,'115200',timeout=0.01)
                read = ser.readlines()
                rsp = '\n'.join([str(item).replace(r"\r", "").replace(r"\n'", "").replace(r"b'", "").replace(r"\x1b", "").replace("[0m", "").replace("[33m", "") for item in read])
            if rsp != '':
                self.write_log(write_info=rsp,logname=com+'_'+currentTime+'.log')
            blue_flag = re.findall("on_lock_cmd: 0x81", rsp)
            if blue_flag:
                logger.info(u'收到切换WiFi指令')
            if rsp != '' and flag == WIFI_A:
                success_flag = re.findall("prepare online event information ip="+WIFI_A_IP, rsp)
                reconnect_flag = re.findall("prepare online event information ip="+WIFI_B_IP, rsp)
                if success_flag :
                    logger.info(u'日志显示WiFi更换成功')
                    self.write_csv(kind1=flag+'更换成功（日志）')
                    connect = 1
                elif reconnect_flag :
                    logger.info(u'连回原来的WiFi')
                    self.write_csv(kind1=flag+'更换失败，连回原来的WiFi')
                    connect = 2
            if rsp != '' and flag == WIFI_B:
                success_flag = re.findall("prepare online event information ip="+WIFI_B_IP, rsp)
                reconnect_flag = re.findall("prepare online event information ip="+WIFI_A_IP, rsp)
                if success_flag :
                    logger.info(u'日志显示WiFi更换成功')
                    self.write_csv(kind1=flag+'更换成功（日志）')
                    connect = 1
                elif reconnect_flag :
                    logger.info(u'连回原来的WiFi')
                    self.write_csv(kind1=flag+'更换失败，连回原来的WiFi')
                    connect = 2
            ser.close()

    def main(self):
        self.restartAPP()
        self.TryIn()
        self.status_flag()


if __name__ == '__main__':
    currentTime = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
    i = 0
    status = 0
    sum = 0
    t = 0
    j = 0
    t5 = 0
    t10 = 0
    t20 = 0
    t30 = 0
    t60 = 0
    outbound = 0
    atime = 0
    startime = 0
    endtime = 0

    WIFI_A = 'yunlu'
    WIFI_B = '哈哈哈哈'
    WIFI_A_IP = '10.7.7.'
    WIFI_B_IP = '192.168.31.'
    # send_key = False
    flag = WIFI_A
    connect_flag = 0
    connect = 0
    com = 'com20'

    current_path = os.getcwd()
    plu = '智能门Pro'
    fileName = 'smartdoor'
    device = ''
    run = Demo()
    while True:
        try:
            run.main()
        except Exception as e:
            logger.error(e)
            run.write_csv(kind1=e)
            # logger.error('\n'+traceback.format_exc())
            pass

