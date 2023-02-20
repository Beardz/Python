import csv
import subprocess
import traceback
import uiautomator2 as u2
import time
import serial
import re
import os
import logging
import threading


class LIVE():

    def __init__(self):
        subprocess.run('python -m uiautomator2 init')
        time.sleep(3)
        self.d = u2.connect(devices)
        
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
                row = ['时间','次数','时长']
                file = csv.writer(f)
                file.writerow(row)
        self.restartAPP()
        thread1 = threading.Thread(target=self.click)
        thread1.start()

        
        
        
        

    def restartAPP(self):
        self.logger.info(u'重启app')
        time.sleep(2)
        self.d.app_stop("com.xiaomi.smarthome")
        time.sleep(2)
        self.d.app_start("com.xiaomi.smarthome",use_monkey=True)

    def click(self):
        while True:
            if self.d(text='稍后再说').exists():
                self.d(text='稍后再说').click()
                time.sleep(1)
            else:
                pass

    def TryIn(self):
        
        a = self.d(text=plu)
        # self.d.dump_hierarchy()
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

    def Inlive(self):
        global flag,t,i,j,t5,t10,t30,t60
        thread1 = threading.Thread(target=self.click)
        connect_time= 0
        if self.d(text='小米智能门Pro 2').exists(timeout=10):
            thread1.start()
            starttime = time.time()
            aftertime = time.time()
            self.logger.info(u'进入插件')
            while True:
                if self.d(text='点击重试').exists:
                    self.logger.info(u'直播连接失败')
                    self.screenShot(reason="直播连接失败")
                    break
                elif self.d(text='0 b/s').exists:
                    aftertime = time.time()
                    if aftertime - starttime >= 60:
                        i += 1
                        self.logger.warning(u'直播黑屏')
                        self.screenShot(reason="直播黑屏")
                        self.write_csv(kind1="直播黑屏")
                        break
                elif self.d(textContains='KB/s').exists() :
                    self.logger.info(u'直播连接成功')
                    starttime = time.time()
                    while True:
                        if self.d(description="更多设置").exists():
                            if self.d(text='点击重试').exists:
                                i += 1
                                aftertime = time.time()
                                connect_time = aftertime - starttime
                                h = int(connect_time) // 3600
                                m = int(connect_time) // 60 % 60
                                s = int(connect_time) % 60
                                self.screenShot(reason="直播连接失败")
                                self.logger.info(u'直播连接失败')
                                self.logger.info(u'连接时长:%s'%h+'时%s分'%m+'%s秒'%s)
                                self.write_csv(kind1='%s'%h+'时%s'%m+'分%s秒'%s)
                                break
                        else:
                            self.screenShot(reason="未知位置")
                            self.logger.warning(u'未知位置')
                            break
                    break
        else:
            self.logger.warning(u'未进入插件')

    def mainFun(self):
        self.TryIn()
        self.Inlive()
        self.restartAPP()

    def write_csv(self,kind1):
        if kind1 == "直播黑屏":
            with open(currentTime+'-'+fileName+'.csv', 'a', newline='',encoding='UTF-8') as f:
                row = [time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()),'第%s次' % i,kind1]
                file = csv.writer(f)
                file.writerow(row)
        else:
            with open(currentTime+'-'+fileName+'.csv', 'a', newline='',encoding='UTF-8') as f:
                row = [time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()),'第%s次' % i,kind1]
                file = csv.writer(f)
                file.writerow(row)


if __name__ == '__main__':
    currentTime = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
    plu = '智能门Pro 2'
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
    while True:
        try:
            r.mainFun()
        except:
            r.logger.error('\n'+traceback.format_exc())
            r.restartAPP()
            pass


