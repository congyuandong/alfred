#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import random
import md5
import json
import sys
from xml.etree import ElementTree as ET
from urllib import urlencode

reload(sys)
sys.setdefaultencoding('utf-8')

appid = '20171229000110334'
secretKey = 'FUUwv0kA_oi0F8Z5mV1E'

# 百度翻译，支持中文⇌英文
def trans(word):
    word = word.lower()
    # 请求要翻译的内容是英文还是中文
    request = urllib2.Request('http://fanyi.baidu.com/langdetect?' + urlencode({'query': word}))
    request.add_header("Host", "fanyi.baidu.com")
    result = json.load(urllib2.urlopen(request))
    sourceLang = result.get('lan')
    if (sourceLang == 'en'):
        toLang = 'zh'
    else:
        toLang = 'en'

    api = 'http://api.fanyi.baidu.com/api/trans/vip/translate?'
    salt = random.randint(32768, 65536)
    sign = appid + word + str(salt) + secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    api = api + urlencode({'appid': appid, 'q': word, 'from': sourceLang, 'to': toLang, 'salt': str(salt), 'sign': sign})

    response = urllib2.urlopen(api)
    result = json.loads(response.read())
    dict_result = result.get('trans_result')

    webUrl = 'http://fanyi.baidu.com/#%s/%s/%s' % (sourceLang, toLang, urlencode({'': word}).strip('='))
    if len(dict_result):
        try:
            dict_result = dict_result[0]
            src = dict_result.get('src')
            dst = dict_result.get('dst')
            items = [{
                'title': unicode(dst),
                'subtitle': unicode(src),
                'arg': webUrl,
                'icon': 'chrome.png'
            }]
            return generate_xml(items)
        except:
            items = [{
                'title': u'没有找到哎，试试在线引擎吧',
                'arg': webUrl,
                'icon': 'chrome.png'
            }]
            return generate_xml(items)
    else:
        items = [{
            'title': u'没有找到哎，试试在线引擎吧',
            'arg': webUrl,
            'icon': 'chrome.png'
        }]
        return generate_xml(items)

def generate_xml(items):
    xml_items = ET.Element('items')
    for item in items:
        xml_item = ET.SubElement(xml_items, 'item')
        for key in item.keys():
            if key in ('arg',):
                xml_item.set(key, item[key])
            else:
                child = ET.SubElement(xml_item, key)
                child.text = item[key]
    return ET.tostring(xml_items)