## 系统环境变量设置

    FLASK_CONFIG * [development|testing|production]
    FLASK_SECRET_KEY
    FLASK_MYSQL_USER
    FLASK_MYSQL_PASSWORD
    FLASK_MYSQL_DB *
    FLASK_REDIS_DB *
    CELERY_BROKER_USER
    CELERY_BROKER_PASSWORD
    CELERY_BROKER_VHOST *
    CELERY_BACKEND_DB *
    DES_KEY (8 bytes)
    QINIU_ACCESS_KEY
    QINIU_SECRET_KEY
    QINIU_BUCKET
    QINIU_DOMAIN
    YUNPIAN_KEY
    WEIXIN_ID
    WEIXIN_APP_ID
    WEIXIN_APP_SECRET
    WEIXIN_TOKEN
    WEIXIN_AES_KEY
    WEIXIN_MCH_ID
    WEIXIN_PAY_KEY
    WEIXIN_CERT_PATH
    WEIXIN_KEY_PATH

## API Overview

**All data is sent and received as JSON.**

**success response**

    {
        code: 0
        message: 'Success'
        data: {
            [响应数据]
        }
    }

**error response**

    {
        code: [错误码]
        message: [错误信息]
        data: {}
    }

**错误码对应错误信息**

    1000: 'Internal Server Error'
    1100: 'Bad Request'
    1101: 'Unauthorized'
    1103: 'Forbidden'
    1104: 'Not Found'
    1201: 'GET方法url参数不完整'
    1202: 'GET方法url参数值错误'
    1401: 'POST/PUT方法json数据不完整'
    1402: 'POST/PUT方法json数据值或类型错误'
    1403: '账号不存在'
    1404: '密码错误'
    1405: '密码长度错误'
    1601: 'DELETE方法url参数不完整'
    1602: 'DELETE方法url参数值错误'
    1800: '微信公众平台接口调用失败'
    1801: '微信access_token获取失败'
    1802: '微信jsapi_ticket获取失败'
    1803: '微信素材获取失败'
    1820: '微信支付下单失败'
    1850: '七牛上传凭证获取失败'
    1851: '七牛上传二进制流失败'
    1852: '七牛上传文件失败'

**某些情况下通用的错误码**

    所有请求：1000
    POST/PUT方法：1100
    使用分页参数page/per_page：1202

**通用的可选URL参数**

    fields: 指定返回的对象数据中只包含哪些字段，多个字段以英文逗号分隔

## Model Dependencies

_- : on_delete='CASCADE'_

_* : on_delete='CASCADE', null=True_

**Admin**

**WeixinUser**

**WeixinPayOrder**

    - : WeixinPayRefund

**WeixinPayRefund**

**WeixinMchPay**

**WeixinRedPack**

**User**
