import csv
import subprocess
import uiautomator2 as u2
import time, datetime
import serial
import threading
import re
import logging
import traceback


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
        global t,connect_flag,currentTime,count
        if com !='':
            ser = serial.Serial(com,'1500000',timeout=0.01)
            while True:
                if com !='':
                    read = ser.readlines()
                    rsp = '\n'.join([str(item).replace(r"\r", "").replace(r"\n'", "").replace(r"b'", "").replace(r"\x1b", "").replace("[0m", "").replace("[33m", "").replace("\\x00","") for item in read])
                    if rsp != '':
                        # self.logger.info(u''+rsp+'')
                        self.write_log(write_info=rsp,logname=com+'_'+currentTime+'.log')
                    unlock_succ = re.findall("------POWER_LOCK_UNLOCK_SUCC------", rsp)
                    lock_succ = re.findall("------DOOR LOCK OK!!!------", rsp)
                    unlock_fail = re.findall("------POWER_LOCK_UNLOCK_FAIL------", rsp)
                    lock_fail = re.findall("------POWER_LOCK_LOCK_FAIL------", rsp)
                    lock_open = re.findall("------POWER_LOCK_OPEN------", rsp)
                    lock_UNLATCHED = re.findall("------POWER_LOCK_UNLATCHED------", rsp)
                    moto_reset_succ = re.findall("------POWER_LOCK_MOTO_RESET_SUCC------", rsp)
                    moto_reset_fail = re.findall("------POWER_LOCK_MOTO_RESET_FAIL------", rsp)
                    unlock_timeout = re.findall("------POWER_LOCK_UNLOCK_TIMEOUT------", rsp)
                    lock_unlock_fail = re.findall("MSG_MOTO_UNLOCK_FAILED", rsp)
                    reset_lock = re.findall("send reset locker cmd", rsp)
                    unlock = re.findall("___MOTO____OPEN", rsp)
                    unlock_exception = re.findall("MOTOR_OPEN_TIME_DIFF", rsp)
                    lock_manual_open = re.findall("------POWER_LOCK_MANUAL_OPEN------", rsp)
                    reset_ble = re.findall("ble chip reset by hardware", rsp)
                    ultrasonic = re.findall("ultrasonic_int_handler", rsp)
                    ultrasonic_overtime = re.findall("overtime fw reload", rsp)
                    ultrasonic_count = re.findall("count fw reload", rsp)
                    ultrasonic_event = re.findall("MSG_PEOPLE_APPEAR", rsp)
                    people = re.findall("people appeared",rsp)
                    pin = re.findall("int_pin level",rsp)
                    ready_recognize = re.findall("ready to capture and recognize",rsp)
                    recognize_success = re.findall("recognize successfully",rsp)
                    recognize_fail = re.findall("face_ppl_unlock failed",rsp)
                    capture = re.findall("ms had finished to capture",rsp)
                    # ultrasonic_wifi_event = re.findall("ultrasonic_wifi_event_send_msg", rsp)
                    # if unlock_succ:
                    #     self.logger.info(u'解锁成功')
                        
                    #     break
                    # elif lock_succ:
                    #     self.logger.info(u'上锁成功')
                    #     break
                    # elif unlock_fail:
                    #     self.logger.info(u'解锁失败')
                    #     break
                    # elif lock_fail:
                    #     self.logger.info(u'上锁失败')
                    #     break
                    # elif lock_open:
                    #     self.logger.info(u'门已开')
                    #     break
                    # elif lock_UNLATCHED:
                    #     self.logger.info(u'门虚掩')
                    #     break
                    # elif moto_reset_succ:
                    #     self.logger.info(u'锁体复位成功')
                    #     break
                    # elif moto_reset_fail:
                    #     self.logger.info(u'锁体复位失败')
                    #     break
                    # elif unlock_timeout:
                    #     self.logger.info(u'锁体解锁超时')
                    #     break
                    # elif lock_unlock_fail:
                    #     self.logger.info(u'主控上报解锁失败')
                    #     if reset_ble:
                    #         self.logger.info(u'ble芯片硬件复位')
                    #     break
                    # elif reset_lock:
                    #     self.logger.info(u'复位锁体')
                    #     break
                    # elif unlock:
                    #     self.logger.info(u'------------发送解锁指令------------')
                    #     break
                    # elif unlock_exception:
                    #     self.logger.info(u'解锁异常')
                    #     break
                    # elif lock_manual_open:
                    #     self.logger.info(u'手动开锁')
                    #     break
                    # elif reset_ble:
                    #     self.logger.info(u'ble芯片硬件复位')
                    #     break
                    # elif ultrasonic:
                    #     # print (int(round(time.time() * 1000)))
                    #     # print (int(round(time.time() )))
                    #     # if pin:
                    #     #     self.logger.info(u"int_pin level")
                    #     t1 = int(round(time.time() * 1000))
                    #     self.logger.info(u'触发超声中断')
                    #     while True:
                    #         read = ser.readlines()
                    #         rsp = '\n'.join([str(item).replace(r"\r", "").replace(r"\n'", "").replace(r"b'", "").replace(r"\x1b", "").replace("[0m", "").replace("[33m", "").replace("\\x00","") for item in read])
                    #         if rsp != '':
                    #             # self.logger.info(u''+rsp+'')
                    #             self.write_log(write_info=rsp,logname=com+'_'+currentTime+'.log')
                    #         t2 = int(round(time.time() * 1000))
                    #         ultrasonic_event = re.findall("MSG_PEOPLE_APPEAR", rsp)
                    #         if t2 - t1 > 475:
                    #             self.logger.info("===============================================================")
                    #             break
                    #         # if ultrasonic:
                    #         #     self.logger.info(u'触发超声中断')
                    #         if ultrasonic_event:
                    #             self.logger.info(u'触发超声事件')
                    #             self.logger.info(t1)
                    #             self.logger.info(t2)
                    #             self.logger.info(t2-t1)
                    #             self.logger.info("===============================================================")
                    #             break
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
                            capture = re.findall("ms had finished to capture",rsp)
                            if t2 - t1 > 10000:
                                self.logger.info("10s未识别到人脸")
                                self.logger.info("===============================================================")
                                break
                            if recognize_fail:
                                self.logger.info(u'识别失败')
                                self.logger.info("===============================================================")
                            if capture:

                                t3 = int(round(time.time() * 1000))
                                self.logger.info("抓图成功:"+str(t3-t1))
                                # self.logger.info()
                            if recognize_success:
                                self.logger.info(u'识别成功')
                                t+=1
                                print(t)
                                self.logger.info(t1)
                                self.logger.info(t2)
                                self.logger.info(t2-t1)
                                count=count+(t2-t1)
                                avg=count/t
                                print(count,avg)
                                self.write_csv(time=t2-t1,avg=t3-t1)
                                if t==50:
                                    self.logger.info(avg)
                                self.logger.info("===============================================================")
                                break
                    # elif ultrasonic_event :
                    #     self.logger.info(u'触发超声事件')
                    #     t2 = int(round(time.time() *
                    # 
                    #  1000000))
                    #     self.logger.info(t1)
                    #     self.logger.info(t2)
                    #     self.logger.info(t2-t1)
                    #     self.logger.info("===============================================================")

                                    # self.logger.info("超声事件触发次数:%s" %count)
                                    # if ultrasonic_count:
                                    #     self.logger.info(u'触发超声事件达到200次，重新加载超声固件')
                                    #     count = 0
                                    # continue

                    # elif ultrasonic_event :
                    #     self.logger.info(u'触发超声事件')
                    #     count += 1
                    #     self.logger.info("超声事件触发次数:%s" %count)
                    #     if ultrasonic_count:
                    #         self.logger.info(u'触发超声事件达到次数，重新加载超声固件')
                    #         count = 0
                    #         continue
                    #     break
                    # elif ultrasonic_overtime:
                    #     self.logger.info(u'触发超声中断5s内无超声事件触发，重新加载超声固件')
                    #     break
                    # elif ultrasonic_count:
                    #     self.logger.info(u'触发超声事件达到次数，重新加载超声固件')
                    #     count = 0
                    #     break





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

    def write_csv(self,time='',avg=''):
        with open(currentTime+'.csv', 'a', newline='',encoding='UTF-8') as f:
            row = [time,avg]
            file = csv.writer(f)
            file.writerow(row)

if __name__ == '__main__':
    currentTime = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
    t = 0
    count = 0
    connect_flag = 0
    close_begin = 0
    com='com4'
    r = Match()

    while True:
        try:
            r.match_log()
        except:
            # logging.error(u'未知错误')
            r.logger.error('\n'+traceback.format_exc())
            pass


