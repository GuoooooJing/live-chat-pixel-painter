from pytz import timezone
import requests
from pytz import timezone
from datetime import date, datetime, tzinfo
from collections import defaultdict
from args import ROOMID, URL, RGB_REG, NUM_REG, COLOR_CODE
import re

class Listener:
    def __init__(self) -> None:
        
        self.headers = {
            "Host": "api.live.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }
        self.data = {
            "roomid": ROOMID,
        }
        self.log = defaultdict(tuple)
        self.url = URL
        cst_timezone = timezone('Asia/Shanghai')
        self.startTime = datetime.now(cst_timezone).replace(tzinfo=None)

    def get_chat(self):
        html = requests.post(url=self.url, headers=self.headers, data=self.data).json()
        room_lst = html['data']['room']
        return room_lst

    def valid_command(self, text, chatTime):
        if chatTime < self.startTime:
            return 0
        r1 = re.compile(RGB_REG)
        r2 = re.compile(NUM_REG)
        if r1.match(text):
            return 1
        elif r2.match(text):
            return 2
        else:
            return 0

    def get_pos(self, text):
        pos = text.split(",")
        return (int(pos[0]), int(pos[1]))

    def get_color(self, text):
        color = text.split(",")
        return (int(color[0]),int(color[1]),int(color[2]))

    def get_command(self, text, code):
        # !(1,2)_()
        if code == 1:
            raw_text = text[1:].split('_')
            return self.get_pos(raw_text[0]), self.get_color(raw_text[1])
        else:
            raw_text = text[1:].split('_')
            return self.get_pos(raw_text[0]), COLOR_CODE[int(raw_text[1])-1]

    def new_chat(self):
        room_lst = self.get_chat()
        # print('{:<10}{:<10}{:<10}'.format('nickname', 'uid','text'))
        res = []
        for i in room_lst:
            usrname, uid, text, msgtime = i['nickname'], i['uid'], i['text'], i['timeline']
            chatTime = datetime.strptime(msgtime, "%Y-%m-%d %H:%M:%S")
            code = self.valid_command(text, chatTime)
            print('{}{:<10}{:<10}{:<10}{:<10}'.format(code, i['nickname'], i['uid'],i['text'], i['timeline']))
            if code != 0:
                position, color = self.get_command(text, code)
                key = str(uid)+'_'+msgtime
                if not self.log[key]:
                    self.log[key] = (position, color)
                    res.append((position[0], position[1], color, uid, msgtime))
        return res