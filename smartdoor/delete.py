
import subprocess
import threading
import uiautomator2 as u2
import time
import logging

class delete():
    def __init__(self):
        self.d = u2.connect(device)

    def restartApp(self):
        global name
        self.d.app_stop(package_name='com.xiaomi.smarthome')
        time.sleep(2)
        self.d.app_start(package_name='com.xiaomi.smarthome',use_monkey=True)
        self.d(text=plu).click(timeout=10)
        time.sleep(3)
        self.d.swipe_ext("up")
        time.sleep(2)
        self.d(text='用户管理').click(timeout=5)
        self.d(text='我').click(timeout=5)
        if self.d(text=name).exists(timeout=2):
            self.Face_delete()

    def Face_delete(self):
        global name
        
    
    def main(self):
        global name
        self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[3]/android.view.ViewGroup[1]/android.view.View[1]/android.widget.TextView[1]').click()
        self.d.click(0.67, 0.413)
        if self.d(text="开始录入").exists(timeout=30):
            self.d(text="开始录入").click()
        name = self.d(className='android.widget.EditText').get_text()
        print(name)
        if self.d(text="完成").exists(timeout=10): 
            self.d(text="完成").click()
            # time.sleep(1.5)
        if self.d(text=name).exists(timeout=10):
            time.sleep(1)
            self.d(text=name).click()
            self.d(text=name).click()
        if self.d(text="删除").exists(timeout=10):
            self.d(text="删除").click()
        if self.d(text="确定").exists(timeout=10):
            self.d(text="确定").click()  
    
if __name__ == '__main__':
    status = 1
    i = 1
    fileName = 'smartdoor'
    plu = '云鹿智能门P2'
    device = '9651034151002BK'
    run = delete()
    name = ''
    # run.restartApp()
    try:
        while True:
            print(i)
            run.main()
            i+=1
    except :
        run.restartApp()
        