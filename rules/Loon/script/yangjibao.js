/******************************

脚本功能：养基宝解锁vip
脚本作者：xp9477
更新时间：2024-12-12

*******************************

[rewrite_local]

^https:\/\/app-api\.yangjibao\.com\/account url script-response-body https://raw.githubusercontent.com/xp9477/Scripts/main/rules/Loon/script/yangjibao.js

[mitm] 

hostname = app-api.yangjibao.com

*******************************/

var body = $response.body;
var url = $request.url;
var obj = JSON.parse(body);

const vip = '/account';


if (url.indexOf(vip) != -1) {
    obj.data.is_pay = true;
    obj.data.vip_expiry_date = "2099-12-31";
    obj.data.vip_label = true;

	body = JSON.stringify(obj);
}
