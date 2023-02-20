import csv
import subprocess
import traceback
import uiautomator2 as u2
import time,datetime
import serial
import re
import os
import logging
import threading


class LIVE():

    def __init__(self):
        self.logger = logging.getLogger(currentTime+'-LIVE.log')
        format = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        terminal_format = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(terminal_format)
        th = logging.FileHandler(filename=currentTime+'-LIVE.log',encoding='utf-8')
        th.setFormatter(format)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)
        with open(currentTime+'-'+fileName+'.csv', 'a', newline='',encoding='UTF-8') as f:
                row = ['时间','次数','结果','连接时间','5s内','10s内','20s内','20s以上','平均时间']
                file = csv.writer(f)
                file.writerow(row)

        threading.Thread(target=self.PopupClick).start()

        subprocess.run('python -m uiautomator2 init')
        time.sleep(3)
        self.d = u2.connect(devices)
        self.restartAPP()

    def restartAPP(self):
        time.sleep(2)
        self.d.app_stop("com.xiaomi.smarthome")
        time.sleep(2)
        self.d.app_start("com.xiaomi.smarthome",use_monkey=True)

    def TryIn(self):
        a = self.d(className='android.widget.TextView', text=plu)
        if not a.exists(timeout=2):
            for i in range(5):
                self.d.swipe_ext("up",scale=0.6)
                if not a.exists(timeout=2):
                    continue
                else:
                    break
        for i in range(4):
            if a:
                time.sleep(3)
                a.click()
                break

    def screenShot(self,reason = ''):
        now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        image = self.d.screenshot()
        image.save(reason + now + ".jpg")

    def PopupClick(self):
            while True:
                try:
                    if self.d(text='稍后再说').exists:
                        self.d(text='稍后再说').click()
                except:
                    pass

    def Inlive(self):
        global flag,t,i,j,t5,t10,t30,t60
        if self.d(description="更多设置").exists(timeout=5):
            starttime = time.time()
            aftertime = time.time()
            self.logger.info(u'进入插件')
            while True:
                syntime = time.time()
                if syntime -starttime >= 60:
                    break
                if self.d(textContains='KB/s').exists:
                    aftertime = time.time()
                    break
                elif self.d(textContains='连接失败').exists:
                    self.logger.warning(u'连接失败')
                    break
                elif self.d(textContains='设备离线').exists:
                    self.logger.warning(u'设备离线')
                    break
            if self.d(textContains='连接失败').exists:
                i+=1
                self.write_csv(kind1="失败")
            elif self.d(textContains='设备离线').exists:
                i+=1
                self.write_csv(kind1="设备离线")
            elif syntime -starttime >= 60:
                i+=1
                self.write_csv(kind1="60s未连上")
                self.screenShot(reason="60s未连上")
            else:
                if self.d(textContains='连接失败').exists(timeout=1):
                    i+=1
                    self.logger.warning(u'直播连接失败')
                    self.screenShot(reason="连接失败")
                elif self.d(textContains='设备离线').exists(timeout=1):
                    i+=1
                    self.logger.warning(u'设备离线')
                    self.screenShot(reason="设备离线")
                else:
                    flag = "成功"
                    ti = round(aftertime - starttime,2)
                    if ti < 5:
                        t5 += 1
                    elif ti < 10:
                        t10+= 1
                    elif ti < 20:
                        t30 += 1
                    else:
                        t60 += 1
                    j+=ti
                    i+=1
                    t+=1
                    avg=round(j/t,2)
                    self.logger.info(u'直播连接成功:%ss'%ti)
                    # self.screenShot(reason =flag+"第%s次"%t)
                    self.write_csv(kind1=flag,time1=ti,ti5=t5,ti10=t10,ti30=t30,ti60=t60,avg=avg)
                    flag = ""
        else:
            self.logger.warning(u'未进入插件')
            self.restartAPP()
            self.TryIn()
            self.Inlive()


    def mainFun(self):
        self.TryIn()
        self.Inlive()
        self.restartAPP()

    def write_csv(self,kind1,time1='',ti5='',ti10='',ti30='',ti60='',avg=''):
        if kind1 == "成功":
            with open(currentTime+'-'+fileName+'.csv', 'a', newline='',encoding='UTF-8') as f:
                row = [time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()),i,kind1,time1,ti5,ti10,ti30,ti60,avg]
                file = csv.writer(f)
                file.writerow(row)
        else:
            with open(currentTime+'-'+fileName+'.csv', 'a', newline='',encoding='UTF-8') as f:
                row = [time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()),i,kind1]
                file = csv.writer(f)
                file.writerow(row)


if __name__ == '__main__':
    currentTime = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
    plu = '云鹿智能门P2'
    i = 0
    j = 0
    flag = ""
    t = 0
    t5 = 0
    t10 = 0
    t30 = 0
    t60 = 0
    fileName = 'smartdoor_live'
    com=''
    log_path='D:\code\python'
    devices = ''
    r = LIVE()
    # r.TryIn()
    while True:
        try:
            r.mainFun()
        except:
            r.logger.error('\n'+traceback.format_exc())
            # r.errorRetry()
            pass


