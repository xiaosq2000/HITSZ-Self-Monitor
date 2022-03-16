# 哈小深自动上报v2.0

Todo: 邮件提醒功能、适配网络代理

## 更新内容

1. 新增日志与异常处理
2. 新增风险等级选择
3. 新增运行模式选择
4. 新增定位模拟

## 使用方法

1. 确保您电脑的操作系统是 Windows ，并装有 Chrome 浏览器，没有使用网络代理或者 VPN。
2. 第一次使用前，需要修改 `config.json` 中的内容。
典例如下：

    ```json
    {
        "profiles":
        {
            "id": "180328888",
            "password": "666666",
            "current_status": 7,
            "current_location_risk_level": "low",
            "current_location_name": "若您处在中/高风险地区，此处内容替换为所在街道与社区名称"
        },
        "settings":
        {
            "log_level": "INFO",
            "headless": true
        }
    }
    ```

    **家在低风险地区的同学，仅需要修改`"id"`, `"password"`两项即可。**

    `"id"`的内容是您的学号，含双引号

    `"password"`的内容是您的密码，含双引号

    `"current_status"` 的内容仅为数字，无双引号。若您在校，请将`7`修改为`1`。

    若您所处地区为中风险区，`"current_location_risk_level": "medium",`

    若您所处地区为高风险区，`"current_location_risk_level": "high",`

3. 随后每日双击运行 `哈小深自动上报.exe` 即可。
    可参考网上教程，将其设置为每日定时运行或开机启动。