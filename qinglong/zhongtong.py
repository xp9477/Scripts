# cron: 0 1 * * *
# const $ = new Env("中通快递");
# 需要配置环境变量 zhongtong_accounts, 格式: "phone1,token1;phone2,token2"
import os
import requests
from utils import QlLogger

logger = QlLogger("中通快递")

def sign_in(headers, sign_in_url):
    response = requests.post(sign_in_url, headers=headers, json={})
    response_json = response.json()
    
    if response_json.get('code') != 0 and response_json.get('msg') != '今日已签到':
        logger.error(f"签到失败: {response_json}")
    else:
        logger.info(f"签到成功, {response_json}")

def fetch_user_info(headers, user_info_url):
    response = requests.post(user_info_url, headers=headers, json={})
    response_json = response.json()
    
    if response_json.get('code') != 0:
        logger.error(f"获取用户信息失败: {response_json}")
    else:
        point = response_json.get('data', {}).get('point', 0)
        logger.info(f"当前积分: {point}")

def parse_accounts(env_accounts):
    accounts = []
    if not env_accounts:
        return accounts
        
    for account_str in env_accounts.split(';'):
        if ',' not in account_str:
            continue
            
        phone, token = account_str.strip().split(',')
        accounts.append({
            'username': phone,
            'headers': {
                'token': token,
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
            }
        })
    return accounts

def main():
    sign_in_url = 'https://api.ztomember.com/api/member/sign/v2/userSignIn'
    user_info_url = 'https://api.ztomember.com/api/user/point/get'
    
    accounts = parse_accounts(os.getenv('zhongtong_accounts', '17770808819,eyJhbGciOiJIUzUxMiJ9.eyJnZW5lcmF0ZVRpbWUiOjE3MDY3MjMxNTkxNzEsInVzZXJJZCI6IjgyODkyMTgyNjk5NjQyODgifQ.B42A41iiZLbZCESvC2ibPGyDaezxkhBwPcKKfhxi4pP1RxZzN9TAwlmAzmTp79vRYzEyQoL9O4pRU8ZBzOuXeA;18916173004,eyJhbGciOiJIUzUxMiJ9.eyJnZW5lcmF0ZVRpbWUiOjE3MDY3MjM5MzMxMTUsInVzZXJJZCI6IjIwNzAzMjc2MDc1NzQ2MzA0In0.l1iDfVDKODs4c4HqsT56cDLQsyY404o6i9yY3WQVc81b-Zk8n17lKI2dXZyuOzPywXmSNx5f5ecTc3Vy-xvl5Q;15618626263,eyJhbGciOiJIUzUxMiJ9.eyJnZW5lcmF0ZVRpbWUiOjE3MDY3MjQxMzk5NTIsInVzZXJJZCI6IjIwNzAzMzI2Mjc2MzIyMzA0In0.3AcfD_tQr1C9OxH7RM5k28TCSz15CODPv55TLiOYJUAZfLXRc7XOlhXTPKt6LZ7WUc74E2zUqu2afkIWRrHRZA;'))
    if not accounts:
        logger.info("未配置账号信息，请设置环境变量 zhongtong_accounts")
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
