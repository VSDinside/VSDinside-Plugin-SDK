# Python SDK

这是一个用于开发Stream Dock插件的Python SDK，提供了简单易用的API接口和完整的开发工具链。通过WebSocket实现与Stream Dock软件的实时通信。

## 功能特性

- WebSocket通信：提供与Stream Dock软件的实时通信功能
- 事件处理：支持按钮点击、设置更改等事件的处理
- 定时器：支持设置定时任务和周期性任务
- 日志系统：集成了日志记录功能，方便调试和问题排查

## 项目结构

```
.
├── src/                # 源代码目录
│   ├── core/          # 核心功能模块
│   │   ├── action.py        # 动作类，处理按钮事件
│   │   ├── plugin.py        # 插件核心类，管理WebSocket连接
│   │   ├── timer.py         # 定时器功能
│   │   ├── logger.py        # 日志管理
│   │   └── action_factory.py # 动作工厂类
│   └── actions/       # 具体动作实现
├── requirements.txt   # 项目依赖
├── main.py           # 主程序入口
├── main.spec         # PyInstaller配置文件
└── README.md         # 项目说明
```

## 开发环境设置

1. 创建虚拟环境：
```bash
python -m venv venv
```

2. 激活虚拟环境：
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 插件开发指南

### 创建自定义动作

1. 在`src/actions`目录下创建新的动作类：

```python
from src.core.action import Action

class Custom(Action):
    def __init__(self, action, context, settings, plugin):
        super().__init__(action, context, settings, plugin)
    
    def on_key_up(self, payload):
        # 处理按钮点击事件
        self.set_title("按钮被点击")
        self.set_state(0)
```

2. 使用定时器功能：

```python
def update_display(self):
    # 更新显示内容
    current_time = time.strftime("%H:%M:%S")
    self.set_title(current_time)

# 设置1秒间隔的定时器
self.plugin.timer.set_interval(self.context, 1000, self.update_display)
```

### 日志记录

```python
from src.core.logger import Logger

# 记录信息
Logger.info("操作成功")
# 记录错误
Logger.error("发生错误")
```

## 打包发布

使用PyInstaller打包成可执行文件：

```bash
pyinstaller main.spec
```

打包后的文件将生成在`dist`目录下。

## 注意

如果您遇到了模块没有找到的错误，这个是因为`action_factory.py`里面用到了`importlib.import_module`来动态加载`actions`下的类，而`PyInstaller`在打包的时候是静态分析代码，仅在`action`里面使用的模块`PyInstaller`会认为没有使用这些模块，也就不会把模块打包到exe里面，我们直接把相关模块手动添加到`hiddenimports`里面就可以了

<img src="./hiddenimports.png">

## 开发规范

- 使用类型注解确保代码类型安全
- 遵循PEP 8编码规范
- 编写单元测试确保代码质量
- 使用内置的日志系统记录关键信息

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。