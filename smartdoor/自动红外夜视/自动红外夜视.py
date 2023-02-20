import csv
from doctest import OutputChecker
import subprocess
import traceback
import uiautomator2 as u2
import time,datetime
import serial
import re
import os
import logging
import threading


class InfraredChange():

    def __init__(self):
        self.logger = logging.getLogger(currentTime+'-InfraredChange.log')
        terminalformat = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        outputformat = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(terminalformat)
        th = logging.FileHandler(filename=currentTime+'-InfraredChange.log',encoding='utf-8')
        th.setFormatter(outputformat)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)


        subprocess.run('python -m uiautomator2 init')
        time.sleep(3)
        self.d = u2.connect(devices)
        self.restartAPP()

    def restartAPP(self):
        self.d.app_stop("com.xiaomi.smarthome")
        self.d.app_start("com.xiaomi.smarthome",use_monkey=True)
        start = time.time()
        end = time.time()
        while True:
            end = time.time()
            if end - start > 5:
                break
            elif self.d(text = '取消').exists:
                self.d(text = '取消').click()

    def TryIn(self):
        a = self.d(className='android.widget.TextView', text=plu)
        if not a.exists(timeout=3):
            for i in range(5):
                self.d.swipe_ext("up",scale=0.6)
                if not a.exists(timeout=3):
                    continue
                else:
                    break
        for i in range(4):
            if a:
                time.sleep(5)
                a.click()
                break
        if self.d(text='稍后再说').exists(timeout=10):
            self.d(text='稍后再说').click()

    def screenShot(self,reason = ''):
        now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        image = self.d.screenshot()
        image.save(reason + now + ".jpg")

    def settingIn(self):
        if self.d(description='消息中心').exists(timeout=1):
            self.logger.warning(u'返回到米家首页')
            self.TryIn()
        self.d(description="更多设置").click()
        time.sleep(1)
        s = self.d(text='摄像头设置')
        if s.exists(timeout=5):
            s.click()
            time.sleep(1)
            if self.d(text="摄像头设置").exists(timeout=5):
                self.d(text='摄像头设置').click()
            else:
                pass
            self.d.swipe_ext("up",scale=0.6)
            if self.d(text='自动红外线夜视').exists(timeout=5):
                self.d(text='自动红外线夜视').click()
                time.sleep(1)
                if self.d(text="录像灵敏度").exists(timeout=5):
                    self.d(text='自动红外线夜视').click()
                else:
                    pass
        else:
            self.settingIn()

    def change(self):
        global flag,t,sel,index
        # next = 0
        # now = 0
        # if len(sel)-1 == index:
        #     # next = 0
        #     # now = index
        #     index = 0
        # else:
            # next = index + 1
            # now = index
            # index += 1
        th = threading.Thread(target=self.exceptionCheck)
        if com !='':
            ser = serial.Serial(com,'115200',timeout=0.01)
        time.sleep(1)
        # if flag == "一直关闭" and self.d(text='一直关闭').exists:
        if self.d(text='自动红外线夜视').exists:
            # self.logger.info(sel[now]+u'————>'+sel[next])
            self.logger.info(u'红外夜视切换为-'+sel[index])
            self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.View[1]/android.widget.ImageView[1]').click()
            time.sleep(1)
            self.d(text=sel[index]).click()
            # time.sleep(0.5)
            th.start()
            if self.d(text=sel[index]).exists(timeout=3):
                self.logger.info(u'切换成功')
                flag=sel[index]
                index+=1
                if index >= len(sel):
                    index = 0
            elif self.d(text='请检查网络后重试').exists(timeout=2):
                self.logger.warning(u'网络出错')
                # index -= 1
                self.change()
            else:
                self.logger.warning(u'切换失败')
                # self.write_csv("一直打开切换失败")
        else:
            self.logger.error(u'异常')
            self.errorRetry()

    def Inlive(self):
        global flag,t,i,inlive,sum,t5,t10,t30,t60
        if self.d(text='云鹿智能门P2').exists(timeout=10):
            # self.d(className='android.view.ViewGroup',index=7).click()
            self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()
            starttime = time.time()
            aftertime = time.time()
            self.logger.info(u'进入直播')
            if self.d(text='快速回复').exists(timeout=3):
                self.logger.info(u'进入直播成功')
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
                    elif self.d(textContains='请检查摄像头电池电量').exists:
                        self.logger.warning(u'请检查摄像头电池电量')
                        break
                if self.d(textContains='连接失败').exists:
                    inlive+=1
                    i+=1
                    # self.write_csv("直播连接失败")
                    self.d(className='android.widget.ImageButon').click()
                    self.Inlive()
                elif self.d(textContains='请检查摄像头电池电量').exists:
                    inlive+=1
                    i+=1
                    # self.write_csv("检查摄像头电池电量")
                    self.d(className='android.widget.ImageButon').click()
                    self.Inlive()
                elif self.d(className='android.widget.TextView', text=plu).exists:
                    self.logger.warning(u'进直播成功但返回到米家首页')
                    self.TryIn()
                    self.Inlive()
                else:
                    inlive+=1
                    if self.d(className='android.view.ViewGroup',index=7).exists():
                        self.d(className='android.view.ViewGroup',index=7).click()
                    else:
                        self.d.click(0.448, 0.508)
                        self.d(className='android.view.ViewGroup',index=7).click()
                    time.sleep(9)
                    if self.d(text='取消').exists(timeout=1):
                        self.d(text='取消').click()
                    if self.d(textContains='连接失败').exists(timeout=1):
                        inlive+=1
                        i+=1
                        self.logger.warning(u'直播连接失败')
                        # self.write_csv("直播连接失败")
                        self.d(className='android.widget.ImageButon').click()
                        self.Inlive()
                    elif self.d(textContains='请检查摄像头电池电量').exists(timeout=1):
                        inlive+=1
                        i+=1
                        self.logger.warning(u'请检查摄像头电池电量')
                        # self.write_csv("检查摄像头电池电量")
                        self.d(className='android.widget.ImageButon').click()
                        self.Inlive()
                    else:
                        self.logger.info(u'直播连接成功')
                        if flag :
                            ti = aftertime - starttime
                            if ti < 5:
                                t5 += 1
                            elif ti < 10:
                                t10+= 1
                            elif ti < 30:
                                t30 += 1
                            else:
                                t60 += 1
                            sum+=ti
                            i+=1
                            t+=1
                            avg=sum/t
                            # self.screenShot(reason =flag+"第%s次,"%t+"切换后第%s次进入直播" %inlive)
                            # self.write_csv(kind1=flag,time1=ti,ti5=t5,ti10=t10,ti30=t30,ti60=t60,total=sum,avg=avg)
                        else: pass
                        # self.d(className='android.view.ViewGroup', index=5).click()
                        # self.saveSuccess()
                        self.d(className='android.widget.ImageButon').click()
            else:
                self.logger.warning(u'进入直播失败')
                if self.d(textContains='直播').exists(timeout=1):
                    self.Inlive()
                else:
                    self.logger.warning(u'未找到直播入口')
                    self.restartAPP()
                    self.TryIn()
                    self.Inlive()
        else:
            self.logger.warning(u'未找到直播入口')
            self.restartAPP()
            self.TryIn()
            self.Inlive()

    def checkresult(self):
        global flag,t,i,inlive,sum,t5,t10,t30,t60
        if self.d(text='云鹿智能门P2').exists(timeout=10):
            self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()
            starttime = time.time()
            aftertime = time.time()
            while True:
                syntime = time.time()
                if syntime -starttime >= 60:
                    break
                if self.d(textContains='KB/s').exists:
                    aftertime = time.time()
                    self.logger.info(u'连接成功')
                    time.sleep(5)
                    if self.d(textContains='连接失败').exists:
                        self.logger.warning(u'连接失败')
                        self.d(text='点击重试').click()
                        self.checkresult()
                    elif self.d(textContains='请检查摄像头电池电量').exists:
                        self.logger.warning(u'请检查摄像头电池电量')
                        self.d(text='点击重试').click()
                        self.checkresult()
                    elif flag :
                            ti = aftertime - starttime
                            if ti < 5:
                                t5 += 1
                            elif ti < 10:
                                t10+= 1
                            elif ti < 30:
                                t30 += 1
                            else:
                                t60 += 1
                            sum+=ti
                            i+=1
                            t+=1
                            avg=sum/t
                            self.screenShot(reason ="第%s次,"%t+flag)
                            self.write_csv(kind1=flag,time1=ti,ti5=t5,ti10=t10,ti30=t30,ti60=t60,total=sum,avg=avg)
                    else:pass
                    
                    break
                elif self.d(textContains='连接失败').exists:
                    self.logger.warning(u'连接失败')
                    self.d(text='点击重试').click()
                    self.checkresult()
                    break
                elif self.d(textContains='请检查摄像头电池电量').exists:
                    self.logger.warning(u'请检查摄像头电池电量')
                    self.d(text='点击重试').click()
                    self.checkresult()
                    break
            self.d(description="返回").click()
        else:
            self.logger.warning(u'未找到直播入口')
            self.restartAPP()
            self.TryIn()
            self.checkresult()

    def saveSuccess(self):
        if self.d(text='已保存到手机相册').exists(timeout=1):
            pass
        elif self.d(text='录制视频过短').exists:
            self.logger.warning(u'录制视频过短')
            pass
        elif self.d(text='取消').exists:
            self.d(text='取消').click()
        else:
            self.logger.warning(u'未结束录制')
            self.d(className='android.view.ViewGroup', index=5).click()
            self.saveSuccess()

    def exceptionCheck(self):
        if self.d(text='摄像头休眠中，本次修改将会在摄像头上线时生效').exists:
            self.logger.warning(u'摄像头休眠中')
        # elif self.d(text='请检查网络后重试').exists:
        #     self.logger.warning(u'请检查网络后重试')

    def mainFun(self):
        # global inlive
        self.change()
        self.d(description="返回").click()
        time.sleep(1)
        self.d(description="返回").click()
        time.sleep(1)
        self.d(description="返回").click()
        time.sleep(1)
        self.checkresult()
        # inlive=0
        self.settingIn()

    def write_csv(self,kind1,time1='',ti5='',ti10='',ti30='',ti60='',total='',avg=''):
        with open(currentTime+'红外夜视切换.csv', 'a', newline='',encoding='UTF-8') as f:
            row = [time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()),'第%s次进入直播' % i,kind1,time1,ti5,ti10,ti30,ti60,total,avg]
            file = csv.writer(f)
            file.writerow(row)

    def write_log(self, write_info="", logname="log.txt", write_way='a+', log_print=True, time_mark=True):
            try:
                with open(log_path + "\\" + logname, write_way) as fl:
                    if time_mark:  # 日志中记录时间
                        Current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        fl.write("[" + Current_time + "]"+ "\n" + (str(write_info) + "\n").replace("\r", ""))
                    else:
                        fl.write(str(write_info))
                if log_print:  # 日志打印在控制台
                    print(str(write_info).strip())
                return True
            except:
                return False

    def errorRetry(self):
        try:
            self.restartAPP()
            self.TryIn()
            self.settingIn()
        except:
            self.logger.error('\n'+traceback.format_exc())
            self.errorRetry()

if __name__ == '__main__':
    currentTime = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
    plu = '云鹿智能门P2'
    # sel = ['一直关闭','一直打开','自动切换']
    sel = ['一直关闭','一直打开']
    index = 0
    i = 0
    sum = 0
    flag = ""
    t = 0
    t5 = 0
    t10 = 0
    t30 = 0
    t60 = 0
    inlive=0
    com=''
    log_path='D:\code\python'
    devices = ''
    r = InfraredChange()
    r.TryIn()
    r.settingIn()
    while True:
        try:
            r.mainFun()
        except:
            r.logger.error('\n'+traceback.format_exc())
            r.errorRetry()
            pass


