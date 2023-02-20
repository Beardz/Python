import win32api,win32con,time,logging,keyboard,threading,traceback



class mouseClick():
    def __init__(self):
        currentTime = time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime())
        self.logger = logging.getLogger(currentTime+'-unlock.log')
        format = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(format)
        th = logging.FileHandler(filename=currentTime+'-unlock.log',encoding='utf-8')
        th.setFormatter(format)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)

    def is_number(self,s):
        try:
            float(s)
            if float(s) < 0:
                return False
            else:
                return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def mouse_click(self):
        global lst,stop_flag
        s = len(lst)
        count = s/3
        t = 0
        while t <= count-1 and stop_flag == 0:
            i = t * 3
            self.logger.info(u'点击位置:['+ str(lst[i]) +','+ str(lst[i+1]) +']')
            win32api.SetCursorPos([lst[i], lst[i+1]])
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            btime = time.time()
            etime = time.time()
            # while float(etime - btime) <= float(lst[i+2]) and stop_flag == 0:
            #     etime = time.time()
            #     print(etime-btime)
            time.sleep(float(lst[i+2]))
            t += 1

    def mouse_Cursor(self):
        global lst,th
        print('3s后标记光标')
        time.sleep(3)
        x1 = win32api.GetCursorPos()[0]
        y1 = win32api.GetCursorPos()[1]
        self.logger.info(u'光标位置:['+ str(x1) +','+ str(y1) +']')
        lst.append(x1)
        lst.append(y1)
        stime = input("间隔时间:")
        while not self.is_number(stime):
            stime = input("时间输入有误重试:")
        lst.append(stime)

    def stopCheck(self):
        global stop_flag,th,exit_flag
        while True:
            try:
                if exit_flag == False:
                    if keyboard.is_pressed('esc'):
                        stop_flag = 1
                    else:
                        pass
                elif exit_flag == True:
                    break
            except:
                pass

    def main(self):
        global lst,stop_flag,exit_flag
        while True:
            try:
                x = input("1.标记位置  2.重新标记  3.查询标记  4.删除上一个标记  5.执行  6.退出 :")
                if x == "1":
                    self.mouse_Cursor()
                elif x == "2":
                    print(lst)
                    lst = []
                    print(lst)
                elif x == "3":
                    print(lst)
                elif x == "4":
                    for j in range(3):
                        del lst[len(lst)-1]
                    print(lst)
                elif x == "5":
                    if len(lst) > 0:
                        i = 1
                        print('3s后开始,按"esc"停止')
                        time.sleep(3)
                        while True:
                            try:
                                if stop_flag != 1:
                                    self.logger.info(u'第%s轮' %i)
                                    self.mouse_click()
                                    i += 1
                                else:
                                    self.logger.info(u'停止')
                                    stop_flag = 0
                                    # th.start()
                                    # lst = []
                                    break
                            except:
                                    print("发生异常")
                                    self.logger.error('\n'+traceback.format_exc())
                                    if lst == []:
                                        stop_flag = 0
                    else:
                        print('请先标记位置')
                elif x == "6":
                    exit_flag = True
                    break
            except:
                pass

if __name__ == '__main__':
    lst = []
    stop_flag = 0
    exit_flag = False
    t = mouseClick()
    th = threading.Thread(target=t.stopCheck)
    th.start()
    t.main()