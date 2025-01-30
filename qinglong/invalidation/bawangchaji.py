# cron: 0 1 * * *
# const $ = new Env("霸王茶姬");
# 需要配置环境变量 bawangchaji_accounts, 格式: "phone1,token1;phone2,token2"
# todo: 买一送一券获得通知，到期通知
import os
import requests
from utils import QlLogger

logger = QlLogger("霸王茶姬")

def sign_in(headers, sign_in_url):
    json_data = {'activityId': '947079313798000641', 'appid': 'wxafec6f8422cb357b'}
    response = requests.post(sign_in_url, headers=headers, json=json_data)
    response_json = response.json()
    
    if response_json.get('code') != '0':
        logger.error(f"签到失败: {response_json}")
    else:
        logger.info(f"签到成功, {response_json.get('data', {})}")


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
                'Qm-User-Token': token,
                'Qm-From-Type': 'catering',
                'Qm-From': 'wechat'
            }
        })
    return accounts

def main():
    sign_in_url = 'https://webapi2.qmai.cn/web/catering2-apiserver/crm/points-info'
    user_info_url = 'https://webapi2.qmai.cn/web/catering2-apiserver/crm/points-info'
    
    accounts = parse_accounts(os.getenv('bawangchaji_accounts', ''))
    if not accounts:
        logger.info("未配置账号信息，请设置环境变量 bawangchaji_accounts")
        return

    for account in accounts:
        logger.info(f"账户 【{account.get('username', 'Unknown')}】")
        try:
            sign_in(account['headers'], sign_in_url)
        except Exception as e:
            logger.error(f"处理账户 {account.get('username', 'Unknown')} 时出错: {e}")

if __name__ == '__main__':
    main()
