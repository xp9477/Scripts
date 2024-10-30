# 老娘舅签到
# 需要配置环境变量 laoniangjiu_accounts, 格式: "phone1,token1;phone2,token2"
# cron: 0 1 * * *

# todo: 签到失败通知


import requests
import os
from notify import send
from utils import retry_on_error


@retry_on_error()
def login(session, login_url, credentials=None):
    response = session.post(login_url, data=credentials)


@retry_on_error()
def sign_in(session, sign_in_url):
    json_data = {'activityId': '886927829877411841', 'appid': 'wx6970ed1a10abf76e'}
    response = session.post(sign_in_url, json=json_data)
    sign_in_result = response.json().get('data', {}).get('rewardDetailList', None)
    print(f"签到结果: {sign_in_result}")


@retry_on_error()
def fetch_user_info(session, user_info_url):
    json_data = {'appid': 'wx6970ed1a10abf76e'}
    response = session.post(user_info_url, json=json_data)
    user_info = response.json().get('data', {}).get('totalPoints', None)
    print(f"用户信息：{user_info}")


def main():
    login_url = ''
    sign_in_url = 'https://webapi.qmai.cn/web/cmk-center/sign/takePartInSign'
    user_info_url = 'https://webapi.qmai.cn/web/catering/crm/points-info'

    # 从环境变量读取账号信息
    env_accounts = os.getenv('laoniangjiu_accounts', '')
    accounts = []
    
    # 解析环境变量字符串，格式: "phone1,token1;phone2,token2"
    if env_accounts:
        for account_str in env_accounts.split(';'):
            if ',' in account_str:
                phone, token = account_str.strip().split(',')
                accounts.append({
                    'username': phone,
                    'password': '',
                    'headers': {
                        'Qm-User-Token': token,
                        'Qm-From-Type': 'catering',
                        'Qm-From': 'wechat'
                    }
                })

    if not accounts:
        print("未配置账号信息，请设置环境变量 laoniangjiu_accounts")
        return

    for account in accounts:
        print(f"\n账户 【{account.get('username', 'Unknown')}】")
        with requests.Session() as session:
            try:
                if account['headers']:
                    session.headers.update(account['headers'])
                else:
                    credentials = {'username': account['username'], 'password': account['password']}
                    login(session, login_url, credentials=credentials)

                sign_in(session, sign_in_url)
                fetch_user_info(session, user_info_url)

            except Exception as e:
                print(f"处理账户 {account.get('username', 'Unknown')} 时出错: {e}")

if __name__ == '__main__':
    main()
