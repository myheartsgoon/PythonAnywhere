#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests


def translate(querystr, to_l="en", from_l="zh"):
    '''for google translate
    '''
    C_agent = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.165063 Safari/537.36 AppEngine-Google."}
    flag = 'class="t0">'
    tarurl = "http://translate.google.com/m?hl=%s&sl=%s&q=%s \
        " % (to_l, from_l, querystr.replace(" ", "+"))
    response = requests.get(tarurl, headers=C_agent)
    result = response.text[response.text.find('class="t0">') + len('class="t0">'):].split('<')[0]
    return result
#print(translate("After numerous media reports, Nike Business (China) Co., Ltd. finally issued a fourth statement to consumers yesterday:"))
print(translate("不知龟鹿"))