
import subprocess
import threading
import uiautomator2 as u2
import time
import logging
import random
import traceback
import configparser

class User():
    def __init__(self):
        global p
        p = 7
        self.d = u2.connect(device)
        
    def addPassword(self):
        global p,i
        self.d.swipe_ext('up')
        time.sleep(2.5)
        password = random.randint(100000,9999999999)
        xpath = '//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup['+str(p)+']/android.view.ViewGroup[1]/android.view.View[1]/android.widget.TextView[1]'
        if self.d(text='添加').exists(2): 
            self.d.xpath(xpath).click()
        if self.d(text="下一步").exists(2): 
            self.d(className='android.widget.EditText').click()
            time.sleep(1)
            self.d(focused=True).set_text(password)
        time.sleep(2)
        self.d(text="下一步").click()
        time.sleep(2)
        if self.d(text="下一步").exists(2): 
            self.d(className='android.widget.EditText').click()
            time.sleep(1)
            self.d(focused=True).set_text(password)
        self.d(text="下一步").click()
        time.sleep(1)
        self.d(text="完成").click()
        if p == 9 and i < 2 or p == 10:
            i+=1
            pass
        else:
            p+=1
        # if i == 2:
        #     # p+=1
        #     i = 0
        time.sleep(2)
    
    def add(self):
        self.d.swipe_ext('up')
        # time.sleep(1)
        if self.d(text='添加').exists(2):
            self.d(text='添加').click()
        self.d(text='随机生成').click()
        time.sleep(1)
        self.d(text='随机生成').click()
        time.sleep(1)
        self.d(text='开始时间').click()
        time.sleep(1)
        self.d(text='确定').click()
        time.sleep(1)
        self.d(text='结束时间').click()
        time.sleep(1)
        self.d(text='确定').click()
        time.sleep(1)
        self.d(description='完成').click()
        time.sleep(1)
        self.d(text='完成').click()
        time.sleep(2)
        self.d(text='完成').click()
        time.sleep(1)
        self.d(text='确定').click()
        time.sleep(1.5)
    
    def createUser(self):
        global p
        p = 7
        self.d.xpath('//*[@resource-id="com.xiaomi.smarthome:id/aro"]/android.widget.FrameLayout[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[2]').click()
        if self.d(text='管理员').exists(10):
            self.d(text='管理员').click()
            time.sleep(2)
        self.addPassword()
        self.d(description='返回').click()
        time.sleep(1.5)
    
    def delmobNFC(self):
        self.d.press("power")
        self.d.press("power")
        time.sleep(1)
        self.d(description='刷卡方式设置').click()
        time.sleep(1)
        self.d(text='添加门卡').click()
        time.sleep(1)
        if not self.d(text='更多设置').exists:
            self.d(textContains='小米智能门锁').click()
        time.sleep(1)
        self.d(text='更多设置').click()
        time.sleep(1)
        self.d(text='删除本机门卡').click()
        time.sleep(1)
        self.d(text='确定').click()

    def addmobNFC(self):
        self.d.press("power")
        self.d.press("power")
        time.sleep(1)
        if self.d(text='门卡·钥匙').exists:
            self.d(text='门卡·钥匙').click()
        if self.d(text='智能门锁').exists(15):
            self.d(text='智能门锁').click()
        time.sleep(1)
        self.d(text='立即开卡').click()
        if self.d(text='完成').exists(15):
            self.d(text='完成').click()

    def addNFC(self):
        pass

    def test(self):
        self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[9]/android.view.ViewGroup[1]/android.view.View[1]/android.widget.TextView[1]').click()
        time.sleep(1)
        self.d(text='去激活').click()
        time.sleep(10)
        self.d.app_start("com.xiaomi.smarthome",use_monkey=True)
        # config = configparser.ConfigParser()
        # config.read('D:\code\python\smartdoor\wifi.conf',encoding='utf-8')

        # # 查询类方法
        # secs = config.sections()  # 获取所有的节点名称
        # print("所有的节点名称:", secs)
        # options = config.options('wifi')  # 获取指定节点的所有key
        # print("指定节点的所有key:", options)
        # val = config.get('plu', 'name')  # 获取指定节点的指定key的value
        # print("指定节点的指定key的value:", val)
        # print(len(options))
        # wifi = config.options('wifi')
        # WIFI_List = []
        # WIFI_IP_List = []
        # WIFI_PWD = []
        # for i in range(len(wifi)):
        #     WIFI_List.append(wifi[i])
        #     WIFI_IP_List.append(config.get('ip',wifi[i]))
        #     WIFI_PWD.append(config.get('wifi',wifi[i]))
        # print(WIFI_List)
        # print(WIFI_IP_List)
        # print(WIFI_PWD)




    
if __name__ == '__main__':
    status = 1
    i = 0
    fileName = 'smartdoor'
    plu = '云鹿智能门P2'
    device = ''
    run = User()
    name = ''
    try:
        while True:
            print(i)
            run.addPassword()
            run.addPassword()
            
    except :
        traceback.format_exc()
        # run.restartApp()
        pass