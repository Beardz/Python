import time, datetime
import serial
import logging
from logging.handlers import RotatingFileHandler
                               


class Match():

    def __init__(self):
        self.logger = logging.getLogger(path+currentTime+'.log')                            
        format = logging.Formatter('%(asctime)s - %(message)s')
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(format)
        th = RotatingFileHandler(path+currentTime+'.log',maxBytes=100*1024*1024,backupCount=20)
        th.setFormatter(format)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)

                                     

    def match_log(self):
        global currentTime
        ser = serial.Serial(com,'1500000',timeout=0.01)
        while True:
            if com !='':
                read = ser.readlines()
                rsp = '\n'.join([str(item).replace(r"\r", "").replace(r"\n'", "").replace(r"b'", "").replace(r"\x1b", "").replace("[0m", "").replace("[33m", "").replace("\\x00","") for item in read])
                if rsp != '':
                    Current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.logger.info('['+Current_time+']'+(str(rsp) + "\n").replace("\r", ""))

                        


if __name__ == '__main__':
    currentTime = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
    path = "D:\code\python\smartdoor\log\com18\\"
    com='com18'
    r = Match()
    while True:
        r.match_log()
    



                



