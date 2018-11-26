# -*- coding: utf-8 -*-

import sys
import re
import json
import urllib.request
import urllib.parse
import random
# case in Python 2.6~
# from __future__ import print_function

MESSAGE_PARAM = sys.argv[1]
KEY_PARAM = '004bc21799cf95ed2b84'
# URL + 'key=' + KEY_PARAM + '&' + 'message=' + MESSAGE_PARAM
URL = 'https://chatbot-api.userlocal.jp/api/chat?'
params = {
    'message': MESSAGE_PARAM,
    'key': KEY_PARAM
}
URL += urllib.parse.urlencode(params)

# \dは半角数字の0~9を表す．{4}は4桁を表す.
match_year = re.search('\d{4}', MESSAGE_PARAM)
match_kuji = re.search('くじ', MESSAGE_PARAM)
match_matsu = re.search('まつけん', MESSAGE_PARAM)

if match_year:
    # 4桁の数字抽出．干支スタンプの出力
    year = int(match_year.group(0))
    etonum = ((year - 4) % 12)
    eto = ['子(ねずみ)', '丑(うし)', '寅(とら)', '卯(うさぎ)', '辰(たつ)', '巳(へび)', '午(うま)', '未(ひつじ)', '申(さる)', '酉(とり)', '戌(いぬ)', '亥(いのしし)']
    text = '{eto}年生まれなんだね！'.format(eto = eto[etonum])
    # スタンプだけ，ひつじとたつが入れ替わっていることに対する処理．
    if etonum == 4:
        etonum = 7
    elif etonum == 7:
        etonum = 4

    packageId = '4'
    stickerId = 621 + etonum
    print(text + ',' + packageId + ',' + str(stickerId), end='')

elif match_kuji:
    # くじ引き
    kuji = ['大吉', '中吉', '凶']
    rnd = random.randint(0, 2)
    rtrn_msg = kuji[rnd]

    emoji = {}
    if rnd == 0:
        emoji = u'\U0001F601'
    elif rnd == 1:
        emoji = u'\U0001F609'
    elif rnd == 2:
        emoji = u'\U0001F631'

    packageId = '2'
    stickerId = '144'

    print(rtrn_msg + emoji + ',' + packageId + ',' + stickerId, end='')

elif match_matsu:
    # まつけん
    packageId = '4'
    stickerId = random.randint(260, 307)
    print('わたしまつけんです' + ',' + packageId + ',' + str(stickerId), end='')

else:
    with urllib.request.urlopen(URL) as res_:
        _html = res_.read().decode('utf-8')
        _root = json.loads(_html)
        print(_root['result'], end='')
