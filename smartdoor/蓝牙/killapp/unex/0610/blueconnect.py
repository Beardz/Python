#coding=utf8
import csv
import re
import traceback
import uiautomator2 as u2
import time
import logging
import os

class BluetoothConnect():
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

    def bluetoochConnect(self):
        global status,i
        self.status_flag()

    def PopupClick(self):
        while True:
            try:
                if self.d(text='稍后再说').exists:
                    self.d(text='稍后再说').click()
            except:
                pass

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

    def status_flag(self):
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

    def write_csv(self,kind1='',time1='',ti5='',ti10='',ti20='',ti60='',avg='',total=''):
        global current_path
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
        else:
            with open(currentTime+'-'+fileName+'.csv', 'a', newline='',encoding='UTF-8') as f:
                row = [time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()),i,kind1]
                file = csv.writer(f)
                file.writerow(row)

    def screenShot(self,reason = ''):
        now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        image = self.d.screenshot()
        image.save(reason + now + ".jpg")

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
    t5 = 0
    t10 = 0
    t20 = 0
    outbound = 0
    atime = 0
    startime = 0
    endtime = 0
    current_path = os.getcwd()
    plu = '智能门Pro'
    fileName = 'smartdoor'
    device = ''
    run = BluetoothConnect()
    while True:
        try:
            run.main()
        except Exception as e:
            logger.error(e)
            run.write_csv(kind1=e)
            # logger.error('\n'+traceback.format_exc())
            pass

