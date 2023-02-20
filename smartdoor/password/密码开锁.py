import serial
import logging
import time
import random


class Relay:
    def __init__(self):
        self.current_key = 0x7f  # 默认第8路对应的bit设置为0，设置为1会有问题，所以第8路不要用 0111 1111
        self.ser = serial.Serial('com7', 9600, timeout=0.5)

    # 初始化继电器，重新初始化需要给继电器重新上电
    def init_relay(self):
        # 0x50关闭串口模块，继电器不工作
        self.ser.write(chr(0x50).encode("utf-8"))
        time.sleep(0.5)
        # 首次上电才会打印，返回ac代表是8路继电器，ab代表是4路继电器，ad代表是2路继电器
        print(str(self.ser.read())[-3:-1:])
        # 打开串口模块，继电器正常工作
        self.ser.write(chr(0x51).encode("utf-8"))
        time.sleep(0.5)
        self.ser.write(chr(self.current_key).encode("utf-8"))

    # 开 默认开的那路，即将该路对应bit设为0
    def open_key(self, num):
        # 开哪路将对应的bit位设置为0，其他bit位不变
        mark = (2 ** (num - 1)) ^ 0xff  # 异或运算：对应位数不相同结果为1，否则为0 0xff=11111111
        self.current_key = self.current_key & mark  # 与运算：对应位数都为1，否则为0
        self.ser.write(chr(self.current_key).encode("utf-8"))

    # 停 默认断开的那路，即将该路对应bit设为1
    def close_key(self, num):
        # 关哪路将对应的bit位设置为1，其他bit位不变
        mark = 2 ** (num - 1)  # **幂运算
        self.current_key = self.current_key | mark  # 或运算：只要出现1，结果就为1
        self.ser.write(chr(self.current_key).encode("utf-8"))

    # 关闭1-7路，默认第8路对应的bit设置为0，设置为1会有问题，所以第8路不要用
    def close_all(self):
        self.current_key = 0x7f  # 关闭1-7路
        self.ser.write(chr(self.current_key).encode("utf-8"))

    def open_all(self):  # 开1-8路
        self.current_key = 0x00
        self.ser.write(chr(self.current_key).encode("utf-8"))

    def close_ser(self):  # 关闭串口
        self.ser.close()


class Test:
    def __init__(self, log_level):
        self.LEVEL = log_level
        self.FORMAT = '%(asctime)-15s %(levelname)s %(module)s %(funcName)s %(lineno)d %(message)s'
        self.logger = logging.getLogger("name")
        formatter = logging.Formatter(self.FORMAT)
        self.logger.setLevel(self.LEVEL)
        console = logging.StreamHandler()
        file = logging.FileHandler(filename=currentTime+'touch_open.log', encoding='utf-8')
        console.setFormatter(formatter)
        file.setFormatter(formatter)
        console.setLevel(self.LEVEL)
        file.setLevel(self.LEVEL)
        self.logger.addHandler(console)
        self.logger.addHandler(file)

    def logger(self, name=None, fp='./test.log'):
        logger = logging.getLogger(name)
        formatter = logging.Formatter(self.FORMAT)
        logger.setLevel(self.LEVEL)

        console = logging.StreamHandler()
        file = logging.FileHandler(filename=fp, encoding='utf-8')

        console.setFormatter(formatter)
        file.setFormatter(formatter)

        console.setLevel(self.LEVEL)
        file.setLevel(self.LEVEL)

        logger.addHandler(console)
        logger.addHandler(file)
        return logger

    def touch_key(self, pwd, com, lightup=True):
        # B:电池
        # K：钥匙图标
        btn = {"4": 0x04, "M": 0x0E, "9": 0x09, "5": 0x05, "1": 0x01, "2": 0x02,
               "3": 0x03, "0": 0x0B, "7": 0x07, "8": 0x08, "6": 0x06, "B": 0x0A, "K": 0x0C}
        try:
            if lightup is True:
                pwd = '1' + pwd
            for i in pwd:
                # 写入数字
                ser = serial.Serial(com, 9600, timeout=1)
                # press flag
                ser.write(chr(0x01).encode('utf-8'))
                # write char
                ser.write(chr(int(btn[i])).encode('utf-8'))
                # serial quits
                ser.write(chr(0x5A).encode('utf-8'))
                time.sleep(0.2)
                ser.close()

                # 释放手指
                ser = serial.Serial('com7', 9600, timeout=1)
                # press flag
                ser.write(chr(0x01).encode('utf-8'))
                # write char
                ser.write(chr(0x00).encode('utf-8'))
                # serial quits
                ser.write(chr(0x5A).encode('utf-8'))
                time.sleep(0.2)
                ser.close()
            return 1
        except Exception as e:
            self.logger.error(str(e))
            return 0

    def test_unlock_by_password(self, pwd_list, times, com):
        self.logger.info('***************************测试开始*****************************')
        for i in range(times):
            index = random.randint(0, len(pwd_list) - 1)
            self.touch_key(pwd_list[index], com)
            self.logger.info('第{}次开锁,密码{}'.format(i + 1, pwd_list[index]))
            time.sleep(random.randint(6,15))
        self.logger.info('***************************测试结束*****************************')


if __name__ == '__main__':
    currentTime = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
    # 自动开锁需要用到的密码
    # passwords = ['147258', '100001', '100002']
    passwords = ['147258']
    test = Test(logging.INFO)
    # test.logger(name='随便什么名字', fp='随便写个文件名.log')
    test.test_unlock_by_password(passwords, 20000000, 'com7')
