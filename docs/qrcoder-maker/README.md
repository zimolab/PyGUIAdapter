# QRCode Maker：使用PyGUIAdapter从零开始构建应用程序

接下来，我们将使用`PyGUIAdapter`从零开始构建一个GUI应用程序。

应用程序的名称为`QRCode Maker`，主要功能是为用户提供二维码生成功能，支持将生成的二维码保存为本地图片文件，支持调整二维码大小、码元颜色、背景色、
容错率等参数。

## 零、开始之前

> Tip: 在正式开始前，假定读者已经了解`PyGUIAdapter`的基本用法。

在`QRCode Maker`项目中，我们将使用`poetry`进行依赖管理，并选择`PySide2`作为qt绑定库。

该项目被存储在这个仓库中：[https://github.com/zimolab/QRCode-Maker](https://github.com/zimolab/QRCode-Maker)。你可以将项目克隆到本地，
并尝试运行它，看看效果如何，可以参考如下步骤：

> Tip: `QRCode Maker`项目使用poetry作为依赖管理工具，请确保已安装poetry。

1. 将项目仓库克隆到本地。
```shell
git clone https://github.com/zimolab/QRCodeMaker.git
```

2. 进入项目目录，安装依赖。
```shell
cd QRCode-Makder/
poetry install
```

3. 激活虚拟环境
```shell
poetry shell
```

4. 运行项目
```shell
python main.py
```

## 一、从无到有：构建一个“能用”的应用程序

### （一）完成核心功能开发
`PyGUIAdapter`允许开发者以一种自然的方式进行思考和编写代码，换言之，在完成核心功能编写前，开发者可以不必考虑GUI相关的任何细节。所以，让我们先专注
核心功能的开发，也就是实现二维码的生成功能。

### （二）完成GUI的初步适配


## 二、从能用到好用之一：改变控件类型

## 三、从能用到好用之二：配置控件属性

## 四、从能用到好用之三：配置窗口属性

## 五、从能用到好用之四：添加窗口菜单与工具栏

## 六、从能用到好用之五：界面美化

## 七、从能用到好用之六：添加新功能

## 八、从能用到好用之七：打包和分发