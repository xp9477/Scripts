# cron: 0 1 * * *
# const $ = new Env("华住会");
# 需要配置环境变量 huazhu_usertoken, 抓包 cookie 中的 userToken
# todo: 活跃值检测， 超过50抽奖
# todo: 年度签到检测， 领取盲盒


import os
import requests
import time
from notify import send
from utils import retry_on_error


cookies = {
    'userToken': os.environ.get('huazhu_usertoken', ''),
}

@retry_on_error()
def sign():
    url = f'https://appgw.huazhu.com/game/sign_in'

    headers = {
        'Client-Platform': 'APP-IOS',
        'Sec-Fetch-Site': 'same-site',
        'Accept': 'application/json, text/plain, */*',
        'Host': 'appgw.huazhu.com',
        'Origin': 'https://cdn.huazhu.com',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'HUAZHU/ios/iPhone/18.1/9.26.0/RNWEBVIEW',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://cdn.huazhu.com/',
    }

    params = {
        'date': str(int(time.time())),
    }

    response = requests.get(url, params=params, headers=headers, cookies=cookies)
    response_json = response.json()
    
    sign_result = response_json.get('content', {}).get('SignResult', '')
    
    if not sign_result:
        print(f"签到失败: {response_json}")
        send(f"华住会签到失败: {response_json}")
    else:
        point = response_json.get('content', {}).get('point', '')
        print(f"签到成功, 获得积分: {point}")

if __name__ == "__main__":
    sign()


# {"code":200,"message":"","content":{"signResult":true,"point":3,"activityPoints":1,"supplementSignPoint":null,"supplementSignDate":null,"supplementSignTimes":null,"signReminder":false,"awardMap":{"3":[{"awardIcon":"https://res-pub.huazhu.com/huazhuapp2020/38fe337e4b85835a9af3a81322037867.png","awardName":"早餐券","awardRealName":"早餐券","awardType":"3","awardGetType":"1","awardValue":"","subAwardList":null},{"awardIcon":"https://res-pub.huazhu.com/huazhuapp2020/38fe337e4b85835a9af3a81322037867.png","awardName":"5元立减券","awardRealName":"5元立减券","awardType":"3","awardGetType":"1","awardValue":"","subAwardList":null},{"awardIcon":"https://res-pub.huazhu.com/huazhuapp2020/ed141dd4060b8ab81a9131fcdf7657d1.png","awardName":"5积分","awardRealName":"5积分","awardType":"4","awardGetType":"1","awardValue":"5","subAwardList":null},{"awardIcon":"https://res-pub.huazhu.com/huazhuapp2020/c307e8a79efc02459471147d2fa06aca.png","awardName":"10活跃值","awardRealName":"10活跃值","awardType":"7","awardGetType":"1","awardValue":"10","subAwardList":null},{"awardIcon":"https://res-pub.huazhu.com/huazhuapp2020/c307e8a79efc02459471147d2fa06aca.png","awardName":"1活跃值","awardRealName":"1活 跃值","awardType":"7","awardGetType":"0","awardValue":"1","subAwardList":null}],"7":[{"awardIcon":"https://res-pub.huazhu.com/huazhuapp2020/38fe337e4b85835a9af3a81322037867.png","awardName":"10元立减券","awardRealName":"10元立减券","awardType":"3","awardGetType":"1","awardValue":"","subAwardList":null},{"awardIcon":"https://res-pub.huazhu.com/huazhuapp2020/38fe337e4b85835a9af3a81322037867.png","awardName":"1小时延退券","awardRealName":"1小时延退券","awardType":"3","awardGetType":"1","awardValue":"","subAwardList":null},{"awardIcon":"https://res-pub.huazhu.com/huazhuapp2020/ed141dd4060b8ab81a9131fcdf7657d1.png","awardName":"20积分","awardRealName":"20积分","awardType":"4","awardGetType":"1","awardValue":"20","subAwardList":null},{"awardIcon":"https://res-pub.huazhu.com/huazhuapp2020/c307e8a79efc02459471147d2fa06aca.png","awardName":"15活跃值","awardRealName":"15活跃值","awardType":"7","awardGetType":"1","awardValue":"15","subAwardList":null},{"awardIcon":"https://res-pub.huazhu.com/huazhuapp2020/c307e8a79efc02459471147d2fa06aca.png","awardName":"1活跃值","awardRealName":"1活跃值","awardType":"7","awardGetType":"0","awardValue":"1","subAwardList":null}]}},"responseDes":"","businessCode":"1000","page":null}
# {"code":5004,"message":"今日已签到","content":{"signResult":false,"point":null,"activityPoints":null,"supplementSignPoint":null,"supplementSignDate":null,"supplementSignTimes":null,"signReminder":null,"awardMap":null},"responseDes":"","businessCode":"5004","page":null}