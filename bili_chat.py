import json
import struct
import time
import threading
import zlib
from datetime import datetime
from collections import namedtuple
import websocket
from args import ROOMID, RGB_REG, NUM_REG, COLOR_CODE
import re

HEADER_STRUCT = struct.Struct('>I2H2I')
# 大端 >
# 四字节长度 I
# 2字节长度 H

HeaderTuple = namedtuple('HeaderTuple', ('pack_len', 'raw_header_size', 'ver', 'operation', 'seq_id'))


class Spider(object):
    def __init__(self):
        self.ws = websocket.create_connection('wss://broadcastlv.chat.bilibili.com:443/sub')
        self.uid = 0
        self.room_id = ROOMID
        self.login()
        self.heartBeat()

    # 消息处理
    def _handle_message(self, data):
        offset = 0
        res = []
        while offset < len(data):
            try:
                header = HeaderTuple(*HEADER_STRUCT.unpack_from(data, offset))
            except struct.error:
                break
            if header.operation == 5:
                # 弹幕消息
                body = data[offset + HEADER_STRUCT.size: offset + header.pack_len]
                if header.ver == 2:
                    # zlib加密消息
                    body = zlib.decompress(body)
                    res += self._handle_message(body)

                else:
                    # 正常json消息
                    try:
                        body = json.loads(body.decode('utf-8'))
                        # 弹幕
                        if body['cmd'] == 'DANMU_MSG':
                            info = body['info']
                            # info结构是数组，第二个值为弹幕内容，第三个为用户信息，包括uid和昵称，第四个为粉丝牌信息，其他不清楚
                            user = info[2][1]
                            msg = info[1]
                            uid = info[2][0]
                            msgtime = datetime.fromtimestamp(info[0][4]/1000.0).strftime("%Y-%m-%d %H:%M:%S") 
                            print(user, ':', msg)
                            code = self.valid_command(msg)
                            if code != 0:
                                position, color = self.get_command(msg, code)
                                res.append((position[0], position[1], color, uid, msgtime))
                    except Exception as e:
                        print("Get message error", e)
                        raise
            else:
                pass
            offset += header.pack_len
        return res

    # 封包
    def make_packet(self, data, operation):
        body = json.dumps(data).encode('utf-8')
        header = HEADER_STRUCT.pack(
            HEADER_STRUCT.size + len(body),
            HEADER_STRUCT.size,
            1,
            operation,
            1
        )
        return header + body

    # 登录
    def login(self):
        auth_params = {
            'uid': self.uid,
            'roomid': self.room_id,
            'protover': 2,
            'type': 2,
            'platform': 'web',
            'clientver': '2.6.2',
        }
        try:
            self.ws.send(self.make_packet(auth_params, 7))
            print('Login')
        except Exception as e:
            print('Login Failed')
            exit(1)

    # 获取消息
    def get_msg(self):
        while True:
            try:
                msg_bytes = self.ws.recv()
                msg = self._handle_message(msg_bytes)
                if msg:
                    return msg
            except Exception as e:
                print("Get message failed")
                pass

    # 心跳连接
    def keep_alive(self):
        """
        客户端每隔 30 秒发送心跳信息给弹幕服务器
        """
        while True:
            try:
                print('\nHeart Beat\n')
                self.ws.send(self.make_packet({}, 2))
                time.sleep(30)
            except Exception as e:
                print("Heart Beat Failed",e)
                exit(1)

    def valid_command(self, text):
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

    def heartBeat(self):
        t2 = threading.Thread(target=self.keep_alive)
        t2.setDaemon(True)
        t2.start()