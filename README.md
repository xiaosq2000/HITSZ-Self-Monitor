# 哈小深自动上报

基于python3, selenium, chromedriver

## 使用方法 (Windows)

1. 您的电脑上需要有 Chrome 浏览器

2. 下载并解压 `哈小深自动上报.zip` [[蓝奏云下载链接]](https://wwp.lanzouq.com/iZJLW00evnwb)

3. 修改 `profiles.json` 中的内容，如

```json
{
    "id": "180328888",
    "password": "123456",
    "current_status": 7
}
```

注意：`"current_status"` 的内容仅为数字，无双引号。若您在校，请将`7`修改为`1`。

- 在校（校内宿舍住） - 1
- 在校（走读） - 2
- 在校（校内隔离） - 3
- 校外隔离 - 4
- 病假 - 5
- 事假 - 6
- 其他 - 7

4. 双击运行 `哈小深自动上报.exe` 即可。

5. 后续可参考网上教程，将 `哈小深自动上报.exe` 设置为每日定时运行或开机启动。