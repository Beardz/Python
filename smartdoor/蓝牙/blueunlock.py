#coding=utf8
import csv
import subprocess
import threading
import uiautomator2 as u2
import time
import logging

class BluetoothUnlock():
    def __init__(self):
        currentTime = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
        self.logger = logging.getLogger(currentTime+'-'+ fileName + '.log')
        format = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(format)
        th = logging.FileHandler(filename=currentTime+'-'+ fileName + '.log',encoding='utf-8')
        th.setFormatter(format)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)
        subprocess.run('python -m uiautomator2 init')
        # time.sleep(3)
        self.d = u2.connect(device)
        t1 = threading.Thread(target=self.status_flag)
        t1.start()

    def unlock(self):
        global status,i
        while True:
            if self.d(text='长按开锁').exists and status == 1:
                now = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
                print('时间：%s 第%s次蓝牙开锁' % (now, i))
                self.d(text='长按开锁').long_click()
                if self.d(text='解锁成功').exists(timeout=1):
                    self.logger.info(u'第%s次解锁成功' % i)
                    # print('第%s次解锁成功' % i)
                    i += 1
                else:
                    status = 0
                time.sleep(10)
            elif status == 1 and not self.d(text='长按开锁').exists:
                self.d.swipe_ext("up")
            elif status == 0 :
                self.d.swipe_ext("down")
                if self.d(text='未连接').exists:
                    self.d(text='未连接').click()


    def status_flag(self):
        global status
        while True:
            if self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.ImageView[1]').exists:
                if status!= 1:
                    self.logger.info(u'蓝牙已连接')
                status = 1
            elif self.d(text='请打开手机蓝牙并靠近门锁操作').exists:
                if status!= 0:
                    self.logger.info(u'蓝牙断连')
                status = 0
            elif self.d(text='解锁失败').exists:
                if status!= 0:
                    self.logger.info(u'解锁失败')
                status = 0


    # def write_csv(self, kind):
    #     with open('bluetooth-qc8.csv', 'a', newline='') as f:
    #         row = [time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime()), kind]
    #         file = csv.writer(f)
    #         file.writerow(row)

    def main(self):
        self.unlock()

if __name__ == '__main__':
    status = 1
    i = 1
    fileName = 'smartdoor'
    device = ''
    run = BluetoothUnlock()
    try:
        run.main()
    except:
        run.main()

