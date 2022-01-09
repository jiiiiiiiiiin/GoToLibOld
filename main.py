import time
import json
import execjs
import requests
from lxml import etree


def rob(cookies, seats_expect, my_seats_first=False, keep_alive=False, get_except=False):
    url = "https://wechat.v2.traceint.com/index.php/reserve/index.html?f=wechat"
    headers = {
        "Host": "wechat.v2.traceint.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.20(0x17001426) NetType/4G Language/zh_CN",
        "Accept-Language": "zh-cn",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://wechat.v2.traceint.com/index.php/reserve/index.html?f=wechat",
        "X-Requested-With": "XMLHttpRequest"
    }
    session = requests.session()
    res = session.get(url, headers=headers)
    res.encoding = 'utf-8'
    try:
        if "请在微信客户端打开链接" in res.text or res.json().get("code") == 4:
            return False
    except:
        pass

    if keep_alive:
        return True

    element = etree.HTML(res.text)
    seats_all = []
    if my_seats_first:
        my_seats = element.xpath('//td[@seat_key]')
        for my_seat in my_seats:
            seats_all.append({"lib_id": my_seat.attrib.get("lib_id"), "seat_key": my_seat.attrib.get("seat_key"), 'name':my_seat.text})

    if get_except:
        return seats_all

    seats_all.extend(seats_expect)
    for seat_pre in seats_all:
        url = "https://wechat.v2.traceint.com/index.php/reserve/layout/libid={libid}.html&{time}".format(
            libid=seat_pre.get("lib_id"), time=int(time.time()))
        res = session.get(url)
        element = etree.HTML(res.text)
        scripts = element.xpath('//script/@src')
        hex_url = None
        for script in scripts:
            if "layout/" in script:
                hex_url = script
                break

        hex_js = session.get(hex_url)
        hex_code = hex_js.text.split("T.ajax_get")[0] + 'return ' + hex_js.text.split('"&"+')[1].split('+"="')[0] + ';};'
        if 'JSON.parse("' in hex_code:
            hex_code = hex_code.replace('JSON.parse("', '').replace('"),', ',')
        js = execjs.compile(hex_code)
        hex_code = js.call('reserve_seat', "1", "1", int(time.time()))

        url = "https://wechat.v2.traceint.com/index.php/reserve/get/libid={lib_id}&{hex_code}={seat_key}&yzm=".format(
            lib_id=seat_pre.get("lib_id"),
            hex_code=hex_code,
            seat_key=seat_pre.get("seat_key")
        )
        res = session.get(url)
        json = res.json()

        if json.get('code') == 1:
            pass
        elif json.get('code') == 0:
            return seat_pre.get("name") + '预定成功'
    return False


if __name__ == '__main__':
    cookie = ""
    # keep cookie
    ret = utils.rob(cookies=cookie, seats_expect=[], keep_alive=True)
    if len(ret) == 2:
        is_alive, seats = ret
    else:
        # cookie失效
        is_alive = False

    # rob seats 抢常用座位
    ret = utils.rob(cookies=cookie, seats_expect=[], my_seats_first=True)