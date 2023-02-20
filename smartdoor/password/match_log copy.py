import csv
import subprocess
import uiautomator2 as u2
import time, datetime
import serial
import keyboard
import re
import logging
                               


class Match():

    def __init__(self):
        self.logger = logging.getLogger(currentTime+'.log')                            
        # format = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        format = logging.Formatter('%(asctime)s - %(message)s')
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(format)
        th = logging.FileHandler(filename=currentTime+'match.log',encoding='utf-8')
        th.setFormatter(format)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)

                                     

    def match_log(self):
        global t,connect_flag,currentTime,count,close_begin,recognize
        
        ser = serial.Serial(com,'1500000',timeout=0.01)
        a = time.time()
        while True:
            b = time.time()
            if com !='':
                read = ser.readlines()
                rsp = '\n'.join([str(item).replace(r"\r", "").replace(r"\n'", "").replace(r"b'", "").replace(r"\x1b", "").replace("[0m", "").replace("[33m", "").replace("\\x00","") for item in read])
                if rsp != '':
                    # self.logger.info(u''+rsp+'')
                    self.write_log(write_info=rsp,logname=com+'_'+currentTime+'.log')
                ready_recognize = re.findall("ready to capture and recognize",rsp)
                recognize_success = re.findall("recognize successfully",rsp)
                recognize_fail = re.findall("face_ppl_unlock failed",rsp)

                if ready_recognize:
                    # print (int(round(time.time() * 1000)))
                    # print (int(round(time.time() )))
                    # if pin:
                    #     self.logger.info(u"int_pin level")
                    t1 = int(round(time.time() * 1000))
                    self.logger.info(u'准备开始识别')
                    while True:
                        read = ser.readlines()
                        rsp = '\n'.join([str(item).replace(r"\r", "").replace(r"\n'", "").replace(r"b'", "").replace(r"\x1b", "").replace("[0m", "").replace("[33m", "").replace("\\x00","") for item in read])
                        if rsp != '':
                            # self.logger.info(u''+rsp+'')
                            self.write_log(write_info=rsp,logname=com+'_'+currentTime+'.log')
                        t2 = int(round(time.time() * 1000))
                        recognize_success = re.findall("recognize successfully",rsp)
                        if t2 - t1 > 10000:
                            self.logger.info("10s未识别到人脸")
                            self.logger.info("===============================================================")
                            break
                        if recognize_fail:
                            self.logger.info(u'识别失败')
                            self.logger.info("===============================================================")
                            recognize = False
                            break
                        if recognize_success:
                            recognize = True                     
                            self.logger.info(u'识别成功')
                            t+=1
                            print(t)
                            # self.logger.info(t1)
                            # self.logger.info(t2)
                            self.logger.info(t2-t1)
                            self.logger.info(t2 - close_begin)
                            count=count+(t2-t1)
                            avg=count/t
                            close_recognize = t2 - close_begin
                            print(t2-t1,close_recognize)
                            self.write_csv(time=t2-t1,avg=avg,close=close_recognize)
                            # if t==50:
                            #     self.logger.info(avg)
                            self.logger.info("===============================================================")
                            break
                if recognize == True:
                    ser.close()
                    break    
                if b - a > 10:
                    print("超时")
                    self.write_csv(time="超时",avg="",close="")
                    ser.close()
                    break





    def write_log(self, write_info="", logname="", write_way='a+', log_print=False, time_mark=True):
            try:
                with open(logname, write_way) as fl:
                # with open(log_path + "\\" + logname, write_way) as fl:
                    if time_mark:  # 日志中记录时间
                        Current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        # fl.write("[--------------------------" + Current_time + "--------------------------]"+ "\n" + (str(write_info) + "\n").replace("\r", ""))
                        fl.write('['+Current_time+']'+(str(write_info) + "\n").replace("\r", ""))
                    else:
                        fl.write('['+Current_time+']'+str(write_info))
                if log_print:  # 日志打印在控制台
                    print(str(write_info).strip())
                return True
            except:
                return False

    def write_csv(self,time='',avg='',close=''):
        with open(currentTime+'.csv', 'a', newline='',encoding='UTF-8') as f:
            row = [time,close]
            file = csv.writer(f)
            file.writerow(row)

if __name__ == '__main__':
    currentTime = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
    t = 0
    count = 0
    connect_flag = 0
    close_begin = 0
    recognize = False
    com='com3'
    r = Match()
    while True:     
        btime = time.time()        
        com='com3'
        if keyboard.is_pressed('space'):
            # logging.info(u'靠近计时')
            print("靠近计时")
            close_begin = int(round(time.time() * 1000))
            while True:
                etime = time.time()
                r.match_log()
                recognize = False
                break
                



