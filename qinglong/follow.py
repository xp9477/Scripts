# cron: 0 1 * * *
# const $ = new Env("follow RSS阅读器");
# 需要配置环境变量 follow_cookie, follow_csrfToken
# todo: 签到成功后，获取积分
import os
import requests
import json
from utils import QlLogger


cookie = os.environ.get('follow_cookie', '')
csrfToken = os.environ.get('follow_csrfToken', '')

logger = QlLogger("follow RSS阅读器")

def sign():
    url = 'https://api.follow.is/wallets/transactions/claim_daily'
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x1800262c) NetType/4G Language/zh_CN',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Cookie': cookie  
    }
    data = json.dumps({"csrfToken": csrfToken})


    response = requests.post(url, headers=headers, data=data)
    response_json = response.json()
    
    code = response_json.get('code', '')
    message = response_json.get('message', '')
    
    if code != 0 and message != 'Already claimed':
        logger.error(f"签到失败: {message}")
    else:
        logger.info("签到成功")


if __name__ == "__main__":
    sign()
