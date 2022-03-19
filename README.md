# 哈小深自动上报

## 使用方法

### 简述

0. 确定是您的电脑是 Windows 系统，有 Chrome 浏览器，下载 哈小深自动上报.zip 并解压；
1. 将个人信息录入 `config.json` 配置文件中；
2. 运行 `哈小深自动上报.exe` 即可完成当日上报。

强烈推荐使用 Windows10,11 提供的“任务计划程序”(Task Scheduler) 将其设置为每日定时运行。

### 基本使用

**未在校，且处在低风险区的同学**，仅需替换原文件中的汉字内容，即如下四项：

1. 您的学号
2. 您的密码
3. 所在地的纬度
4. 所在地的经度

注意：

- 不要破坏 json 文件的格式，如删除或增添双引号，逗号等；
- 您所在地的经纬度可由手机的指南针或者搜索引擎获知；
- 请将经纬度的 60 进制（度分秒）转化为 10 进制，如 $36^\circ30^\prime=36.5^\circ$；
- 确保 json 文件与 exe 文件在同一文件夹中；
- 若使用“任务计划程序”每日定时完成，需要将“创建基本任务”中的“起始于”参数修改为相应文件夹。


完整的配置文件示例如下：

```json
{
    "profiles":
    {
        "id": "180328888",
        "password": "88888888",
        "current_status": 7,
        "geo-location-emulation": 
        {
            "enable": true, 
            "latitude": 35.38,
            "longitude": 116.06
        },
        "current_location_risk_level": "low",
        "current_location_name": "若您处在中/高风险地区，此处内容替换为所在街道与社区名称，低风险地区无需修改"
    },
    "settings":
    {
        "log_level": "INFO",
        "headless": true
    }
}
```

## 日志与调试

1. 本程序每次运行会在 `log` 文件夹中生成命名为当天日期的日志文件，其中记录了执行过程与结果。**强烈建议您第一次使用后检查日志文件，判断其是否正常运行、上报成功**。若上报失败，日志中同样提示了可能的错误原因。
2. 如果您想获得更详细的日志信息，可将配置文件中 `"log_level"` 的内容改为 `"DEBUG"`
3. 如果您想观察这个程序到底做了什么，可将配置文件中 `"headless"` 的内容改为 `false`