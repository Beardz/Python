'''
配置下方参数即可，设备类型为必选，其他类型非必选，根据设备需求进行注释掉或者解除注释
设备类型查找链接：https://ydwiki.dding.net/pages/viewpage.action?pageId=36372500
null值需要注释掉参数实现，undefined需要定义参数值
'''
#固件版本
app_version = '1.0.0.0'
#zigbee版本
# zigbee_version = '0.0.1.0'
#语音版本
media_version='0.0.0.0'
#蓝牙版本
ble_version='1.0.0.0'
#EFM8版本
# stm_version = '1.6.0.0'
#指纹版本
fp_version = '3.0.2.0'
#软件版本
hardware_version = '1.0.0.0'
#设备型号
model = 'QG-WZ01'
# touch_version = "2.9"
token = 'e53879dc1d4d4a43b478ce02c936dff7'

data = {'app_version':app_version,
        # 'zigbee_version':zigbee_version,
        'media_version':media_version,
        'ble_version':ble_version,
        # 'stm_version':stm_version,
        'fp_version':fp_version,
        'hardware_version':hardware_version,
        # 'touch_version':touch_version,
        'model':model,
        "token":token}
