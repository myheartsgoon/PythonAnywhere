#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename main.py
from flask import Flask, make_response, request
import translate
import xml.etree.ElementTree as ET
import hashlib, time
import requests

app = Flask(__name__)

app.secret_key = 'development-key'

@app.route('/wx', methods = ['GET', 'POST'] )
def wechat_auth():
    try:
        if request.method == 'GET':
            data = request.args
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.get('signature')
            timestamp = data.get('timestamp')
            nonce = data.get('nonce')
            echostr = data.get('echostr')
            token = "test123"

            l = [token, timestamp, nonce]
            l.sort()
            l = ''.join(l).encode(encoding='utf-8')
            sha1 = hashlib.sha1(l)
            #map(sha1.update, l)
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return "not"
        elif request.method == 'POST':
            rec = request.stream.read()
            xml_rec = ET.fromstring(rec)
            tou = xml_rec.find('ToUserName').text
            fromu = xml_rec.find('FromUserName').text
            xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName>" \
                        "<CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
            if xml_rec.find('Content') is None:
                event = xml_rec.find('Event').text
                if event == "subscribe":
                    welcome = "感谢关注不知龟鹿~[皱眉]"
                    response = make_response(xml_rep % (fromu, tou, str(int(time.time())), welcome))
                    response.content_type = 'application/xml'
                    return response
            if xml_rec.find('Event') is None:
                content = xml_rec.find('Content').text
                if content.strip().startswith('翻译'):
                    howto = "#翻译功能使用方法\n发送： 翻译+目标语言+需要翻译的文字\n例如： \n翻译 英语 这是一段文字\n"\
                            "翻译 日语 这是一段文字\n已支持语言： 英语， 中文， 日语， 韩语， 法语， 意大利语"
                    lg_list = {'英语':'en', '中文':'zh', '日语':'ja', '韩语':'ko', '法语':'fr', '意大利语':'it'}
                    query = content.strip().lstrip('翻译').strip()
                    query_info = query.split()
                    if len(query) == 0 or query_info[0] not in lg_list \
                            or len(query_info) != 2:
                        response = make_response(
                            xml_rep % (fromu, tou, str(int(time.time())), howto))
                        response.content_type = 'application/xml'
                        return response
                    else:
                        to_l = lg_list.get(query_info[0])
                        response = make_response(xml_rep % (fromu, tou, str(int(time.time())), translate.translate(query_info[1],to_l)))
                        response.content_type = 'application/xml'
                        return response

                if content.strip()[:3] == 'vip':
                    howto = "#VIP视频地址解析功能使用方法\n发送： vip+视频地址\n例如： \n"\
                        "vip http://v.youku.com/v_show/id_XMjg5NzgyNjA5Mg==.html\n" \
                        "注意：vip为小写"\
                        "已支持视频网站： 爱奇艺，优酷，腾讯等\n"
                    query = content.strip().lstrip('vip').strip().split()
                    if len(query) == 0:
                        response = make_response(
                            xml_rep % (fromu, tou, str(int(time.time())), howto))
                        response.content_type = 'application/xml'
                        return response
                    else:
                        first_url = 'http://api.baiyug.cn/vip/index.php?url=' + query[0]
                        second_url = 'http://pupudy.com/play?make=url&id=' + query[0]
                        third_url = 'http://tv.dsqndh.com/?jk=http%3A%2F%2Fjqaaa.com%2Fjx.php%3Furl%3D&url=' + query[0]
                        res = requests.get(first_url)
                        res.encoding = 'utf-8'
                        if res.text[-8:].strip() == '请输入视频地址！':
                            response = make_response(
                                xml_rep % (fromu, tou, str(int(time.time())), '请输入有效的视频地址！'))
                            response.content_type = 'application/xml'
                            return response
                        else:
                            result = '链接一：{0}\n链接二：{1}\n链接三：{2}'.format(first_url, second_url, third_url)
                            response = make_response(
                                xml_rep % (fromu, tou, str(int(time.time())), result))
                            response.content_type = 'application/xml'
                            return response
                else:
                    reply = "我理解不了你说啥诶，那我就来学个舌咯~[耶]\n" + "你说~~" + content + "~~"
                    response = make_response(xml_rep % (fromu, tou, str(int(time.time())), reply))
                    response.content_type = 'application/xml'
                    return response
    except Exception as Argument:
        return str(Argument)

@app.route('/test')
def test():
    return make_response('test page')

if __name__ == "__main__":
    app.run('0.0.0.0', port=8080,debug=True)