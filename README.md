# ESP32 智能环境监测系统

<img width="2878" height="1376" alt="index" src="https://github.com/user-attachments/assets/fcd74118-175e-4ce4-8f90-508045d6691d" />
<img width="2878" height="1372" alt="weather" src="https://github.com/user-attachments/assets/e54d7f16-588c-4d8a-b0a9-6cfeb7db0f43" />
<img width="2878" height="1378" alt="info" src="https://github.com/user-attachments/assets/f3a9892b-5aa7-410a-92ac-61135c251a7c" />
<img width="2878" height="1378" alt="data" src="https://github.com/user-attachments/assets/edfe019f-b6fe-43b7-b639-d725ef345ca4" />

## 📖 项目概述

这是一个基于 ESP32 微控制器的智能环境监测系统，配合 Django Web 服务器实现远程数据监控和报警功能。系统能够实时监测多种环境参数，并在异常情况下通过蜂鸣器和网络通知进行报警。

## 🎯 主要功能

### 传感器监测模块：
- **温湿度监测**：DHT11 传感器，定时采集（1秒间隔）
- **烟雾检测**：MQ2 烟雾传感器（模拟量+数字量）
- **人体红外检测**：HC-SR501 人体感应模块
- **火焰检测**：火焰传感器
- **土壤湿度检测**：土壤湿度传感器
- **光照强度检测**：光敏电阻传感器

### 报警功能：
- 温度超过阈值（默认28°C）
- 烟雾浓度超标（≥40%）
- 检测到火焰
- 检测到人体靠近
- 蜂鸣器声音报警

### 数据上传：
- 通过 HTTP POST 将传感器数据上传到 Django 服务器
- 支持 JSON 格式数据传输
- 实时数据监控和存储

## 🛠 硬件配置

### 所需硬件：
- ESP32 开发板
- DHT11 温湿度传感器（GPIO 27）
- MQ2 烟雾传感器
  - 模拟输出：GPIO 32
  - 数字输出：GPIO 35
- HC-SR501 人体红外传感器（GPIO 4）
- 火焰传感器（GPIO 13）
- 土壤湿度传感器（GPIO 33）
- 光敏传感器（GPIO 34）
- 蜂鸣器（GPIO 26）
- 杜邦线若干

### 引脚连接表：
| 传感器 | ESP32 GPIO | 功能说明 |
|--------|------------|----------|
| DHT11 | GPIO 27 | 温湿度数据 |
| MQ2 模拟 | GPIO 32 | 烟雾浓度 |
| MQ2 数字 | GPIO 35 | 烟雾状态 |
| 人体红外 | GPIO 4 | 人体检测 |
| 火焰传感器 | GPIO 13 | 火焰检测 |
| 土壤湿度 | GPIO 33 | 湿度测量 |
| 光敏传感器 | GPIO 34 | 光照强度 |
| 蜂鸣器 | GPIO 26 | 报警声音 |

## 🖥 软件架构

### 1. ESP32 客户端 (`esp32.py`)
- 使用 MicroPython 编程
- 实时采集所有传感器数据
- 数据处理和阈值判断
- HTTP 客户端功能，上传数据到服务器
- 本地报警控制

### 2. Django 服务器端
- **URL 路由** (`urls.py`)：
  - 数据上传接口：`/blog/upload`
  - 报警接收接口：`/blog/alarm`
  - 用户认证和管理功能
- **视图处理** (`views.py`)：
  - 主页显示
  - 搜索功能
  - 联系表单处理

## 📡 网络配置

### Wi-Fi 连接：
```python
SSID: 'Kee'
密码: '17368601723'
```
*注意：实际使用前请修改为您的网络配置*

### 服务器配置：
```python
服务器地址: 'http://192.168.123.2:8000'
上传接口: '/blog/upload'
报警接口: '/blog/alarm'
```

## 🚀 安装和部署

### ESP32 环境配置：
1. 刷写 MicroPython 固件到 ESP32
2. 安装所需库：
   - `machine`
   - `time`
   - `dht`
   - `network`
   - `urequests`
   - `json`

3. 上传代码到 ESP32：
```bash
ampy put esp32.py /main.py
```

### Django 服务器配置：
1. 安装 Django：
```bash
pip install django
```

2. 创建 Django 项目：
```bash
django-admin startproject djpsk
```

3. 创建应用：
```bash
python manage.py startapp blog
```

4. 配置数据库：
```bash
python manage.py migrate
```

5. 运行服务器：
```bash
python manage.py runserver 0.0.0.0:8000
```

## ⚙️ 配置说明

### 重要参数：
```python
# 温度报警阈值
TempThreshold = 28

# 烟雾浓度阈值
MQ2_threshold = 40

# 数据上传间隔
upload_interval = 1  # 秒
```

### 报警逻辑：
1. **温度报警**：温度 ≥ 28°C
2. **烟雾报警**：烟雾浓度 ≥ 40%
3. **火焰报警**：火焰传感器检测到火焰
4. **入侵报警**：人体红外传感器检测到移动

## 📊 数据格式

### 上传数据格式（JSON）：
```json
{
  "Temperature": 25.5,
  "Humidity": 60.0,
  "MQ": 12.3,
  "WaterRate": 45.0,
  "detected": "no",
  "Illumination": 75.2,
  "fire": "no"
}
```

### 报警数据格式：
```json
{
  "alert": "temperature warning",
  "value": 29.5
}
```

## 🔧 调试和测试

### 测试传感器：
1. 温湿度传感器：查看串口输出的温湿度值
2. 烟雾传感器：使用烟雾源测试
3. 人体红外：在传感器前移动测试
4. 火焰传感器：使用打火机测试
5. 蜂鸣器：触发报警时应有声音

### 网络测试：
1. 检查 Wi-Fi 连接状态
2. 测试服务器可达性
3. 验证数据上传功能

## 📁 项目结构

```
项目根目录/
├── esp32.py              # ESP32主程序
├── django_project/       # Django项目
│   ├── urls.py          # 主路由配置
│   ├── views.py         # 视图函数
│   └── blog/            # 应用目录
│       ├── urls.py      # 应用路由
│       └── views.py     # 应用视图
├── requirements.txt      # Python依赖
└── README.md            # 项目说明
```

## ⚠️ 注意事项

1. **电源要求**：确保 ESP32 和所有传感器有稳定电源
2. **网络环境**：保持稳定的 Wi-Fi 连接
3. **传感器校准**：部分传感器需要定期校准
4. **安全警告**：
   - 不要将火焰传感器靠近实际火源
   - 烟雾传感器测试时注意安全
   - 避免传感器受潮

5. **数据安全**：
   - 修改默认 Wi-Fi 密码
   - 更新服务器地址
   - 考虑添加数据加密

## 🔄 扩展功能

### 可添加的功能：
1. LCD 显示屏实时显示数据
2. 手机 App 通知功能
3. 数据历史记录和图表
4. 多设备组网监控
5. 自动化控制（如自动浇水、通风）

### 优化建议：
1. 添加数据本地存储（SD卡）
2. 实现低功耗模式
3. 添加 OTA 远程更新
4. 完善用户管理界面

## 📞 支持与联系

如有问题，请：
1. 检查串口调试信息
2. 验证网络连接
3. 检查服务器状态
4. 查看传感器连接

## 📄 许可证

本项目为开源项目，遵循 MIT 许可证。

---
