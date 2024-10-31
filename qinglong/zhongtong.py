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
    
    if response_json.get('success') != True:
        logger.error(f"签到失败: {response_json}")
    else:
        logger.info(f"签到成功, {response_json}")

def fetch_user_info(headers, user_info_url):
    response = requests.post(user_info_url, headers=headers, json={})
    response_json = response.json()
    
    if response_json.get('success') != True:
        logger.error(f"获取用户信息失败: {response_json}")
    else:
        point = response_json.get('data', {}).get('point', 0)
        logger.info(f"当前积分: {point}")

def parse_accounts(env_accounts):
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
                'token': token,
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
            }
        })
    return accounts

def main():
    sign_in_url = 'https://api.ztomember.com/api/member/sign/v2/userSignIn'
    user_info_url = 'https://api.ztomember.com/api/user/point/get'
    
    accounts = parse_accounts(os.getenv('zhongtong_accounts', ''))
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
