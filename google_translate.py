# encoding=utf8
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def translate(querystr, to_l="en", from_l="zh"):
    '''for google tranlate by doom
    '''
    C_agent = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.165063 Safari/537.36 AppEngine-Google."}
    flag = 'class="t0">'
    tarurl = "http://translate.google.cn/m?hl=%s&sl=%s&q=%s \
        " % (to_l, from_l, querystr.replace(" ", "+"))
    request = urllib2.Request(tarurl, headers=C_agent)
    page = str(urllib2.urlopen(request).read().decode('utf-8'))
    target = page[page.find(flag) + len(flag):]
    target = target.split("<")[0]
    return target
#print(translate("After numerous media reports, Nike Business (China) Co., Ltd. finally issued a fourth statement to consumers yesterday:"))
print(translate("然后我又从网上找到了一个Google翻译代码"))