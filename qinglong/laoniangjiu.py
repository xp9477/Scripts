# cron: 0 1 * * *
# const $ = new Env("老娘舅");
# 需要配置环境变量 laoniangjiu_accounts, 格式: "phone1,token1;phone2,token2"
import requests
import os
from utils import QlLogger
import time


logger = QlLogger("老娘舅")

def sign_in(headers, sign_in_url):
    headers.update({
        'Host': 'webapi.qmai.cn',
        'Qm-From': 'wechat',
        'store-id': '32090',
        'Qm-From-Type': 'catering',
        'content-type': 'application/json',
    })

    json_data = {
        'activityId': '1003628982136791041',
        'storeId': 32090,
        'timestamp': str(int(time.time() * 1000)),
        'signature': '2E3826A3A7676AF15112346DF0F82004',
        'appid': 'wx6970ed1a10abf76e',
    }

    response = requests.post(sign_in_url, headers=headers, json=json_data)
    response_json = response.json()
    
    if response_json.get('code') != 0:
        logger.error(f"签到失败: {response_json.get('message')}")
    else:
        logger.info("签到成功")
    return response_json

def fetch_user_info(headers, user_info_url):
    headers.update({
        'Host': 'webapi.qmai.cn',
        'content-type': 'application/json',
        'store-id': '32090',
        'Referer': 'https://servicewechat.com/wx6970ed1a10abf76e/302/page-frame.html',
    })

    json_data = {
        'appid': 'wx6970ed1a10abf76e',
    }

    response = requests.post(user_info_url, headers=headers, json=json_data)
    response_json = response.json()
    
    if response_json.get('code') != '0':
        logger.error(f"获取用户信息失败: {response_json.get('message')}")
    else:
        totalPoints = response_json.get('data', {}).get('totalPoints', 0)
        logger.info(f"当前积分: {totalPoints}")
    return response_json

def parse_accounts(env_accounts: str) -> list:
    """解析环境变量中的账号信息"""
    accounts = []
    if not env_accounts:
        return accounts
        
    for account_str in env_accounts.split('\n\n'):
        if ',' not in account_str:
            continue
            
        phone, token = account_str.strip().split(',')
        accounts.append({
            'username': phone,
            'headers': {
                'Qm-User-Token': token,
                'Qm-From-Type': 'catering',
                'Qm-From': 'wechat'
            }
        })
    return accounts

def main():
    sign_in_url = 'https://webapi.qmai.cn/web/cmk-center/sign/takePartInSign'
    user_info_url = 'https://webapi.qmai.cn/web/catering/crm/points-info'
    
    accounts = parse_accounts(os.getenv('laoniangjiu_accounts', ''))
    if not accounts:
        logger.info("未配置账号信息，请设置环境变量 laoniangjiu_accounts") 
        return

    for account in accounts:
        logger.info(f"账户 【{account.get('username', 'Unknown')}】")
        try:
            sign_in(account['headers'], sign_in_url)
            fetch_user_info(account['headers'], user_info_url)
        except Exception as e:
            logger.error(f"处理账户 {account.get('username', 'Unknown')} 时出错: {e}")

if __name__ == '__main__':
    main()
