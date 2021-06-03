from ronglian_sms_sdk import SmsSDK

accId = '容联云通讯分配的主账号ID'
accToken = '容联云通讯分配的主账号TOKEN'
appId = '容联云通讯分配的应用ID'


def send_message(mobile):
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'  # 容联云通讯创建的模板ID,2以上可以自定义内容
    mobile = mobile  # 手机号1,手机号2 # 可以多个手机，也可以一个手机
    datas = ('验证码', '过期时间')  # 升级即可定义,一般来说上线应用app都是定制内容
    resp = sdk.sendMessage(tid, mobile, datas)
