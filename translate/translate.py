#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import sys
from xml.etree import ElementTree as ET
from urllib import urlencode

reload(sys)
sys.setdefaultencoding('utf-8')

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
    request = urllib2.Request(
        'http://fanyi.baidu.com/v2transapi?' + urlencode({'from': sourceLang, 'to': toLang, 'query': word}))
    request.add_header("Host", "fanyi.baidu.com")
    result = json.load(urllib2.urlopen(request))
    dict_result = result.get('dict_result')

    webUrl = 'http://fanyi.baidu.com/#%s/%s/%s' % (sourceLang, toLang, urlencode({'': word}).strip('='))
    if len(dict_result):
        try:
            symbol = dict_result.get('simple_means').get('symbols')[0]
            parts = symbol.get('parts')
            title = result.get('trans_result').get('data')[0].get('dst') + ' '
            if (sourceLang == 'en'):
                for it in parts:
                    title += '%s%s ,' % (it.get('part'), unicode.decode(it.get('means')[0]))
                subTitle = '英:[%s], 美:[%s]' % (symbol.get('ph_en'), symbol.get('ph_am'))
            else:
                for it in parts[0].get('means'):
                    title += it.get('word_mean') + ' ,'
                subTitle = '拼音:' + symbol.get('word_symbol')
            items = [{
                'title': unicode(title.strip(',')),
                'subtitle': unicode(subTitle.strip(',')),
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