# QRCode Maker：使用PyGUIAdapter从零开始构建应用程序

接下来，我们将使用`PyGUIAdapter`从零开始构建GUI应用程序，该应用程序的名称为`QRCode Maker`，主要的功能是生成二维码。

> 在正式开始前，假定读者已经了解`PyGUIAdapter`的基本用法。

在`QRCode Maker`项目中，我们将使用`poetry`进行依赖管理，并选择`PySide2`作为qt绑定库。

`QRCode Maker`项目地址为：[https://github.com/zimolab/QRCode-Maker](https://github.com/zimolab/QRCode-Maker)。可以将该项目克隆到本地，运行查看效果，具体步骤参考如下：

> `QRCode Maker`项目使用poetry作为依赖管理工具，请确保已安装poetry。

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