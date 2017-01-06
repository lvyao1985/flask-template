## 系统环境变量设置

    FLASK_CONFIG * [development|testing|production]
    FLASK_SECRET_KEY
    FLASK_MYSQL_USER
    FLASK_MYSQL_PASSWORD
    FLASK_MYSQL_DB *
    FLASK_REDIS_DB *
    FLASK_CELERY_BROKER *
    FLASK_CELERY_BACKEND *
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
    WEIXIN_MCH_ID
    WEIXIN_PAY_KEY
    WEIXIN_CERT_PATH
    WEIXIN_KEY_PATH

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
