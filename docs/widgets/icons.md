## 关于图标

在`PyGUIAdapter`中，很多地方都会用到图标，绝大多数需要提供图标的地方，都会要求开发者传入一个类型为`utils.IconType`的对象。 



实际上，`utils.IconType`是`str | tuple[str, list | dict] | QIcon | QPixmap | None`的别名。`PyGUIAdapter`内部将通过`utils.get_icon()`函数从开发者传入的值中获取实际的`QIcon`对象。

> ```python
> IconType = Union[str, Tuple[str, Union[list, dict]], QIcon, QPixmap, type(None)]
> ```



为了方便开发者快速利用现有图标库，`PyGUIAdapter`集成了[`qtawesome`](https://github.com/spyder-ide/qtawesome)库。当传入值为`str`类型时，可以传入一个[`qtawesome`](https://github.com/spyder-ide/qtawesome)支持的图标名称。

> 可以通过[`qtawesome`](https://github.com/spyder-ide/qtawesome)提供的图标浏览工具`qta-browser`来浏览并复制图标的名称，如果安装了`qtawesome`，那么应当可以通过输入以下命令来启动`qta-browser`工具
>
> ```bash
> qta-browser
> ```
>
> <img src="../images/qta-browser.png" />
>
> 



当传入值为`Tuple[str, list|tuple]`类型时，第一个元素应当是[`qtawesome`](https://github.com/spyder-ide/qtawesome)支持的图标名称，第二个元素则是[`qtawesome.icon()`](https://qtawesome.readthedocs.io/en/latest/_generate/qtawesome.icon.html#qtawesome.icon)函数第一个参数之后的剩余参数。例如对于下面示例中的`my_icon`

```pytho
icon_options = {
	"color": "blue",
	"color_active": "orange"
}
my_icon = ("fa5s.music", icon_options)
```

`utils.get_icon()`将按照如下方式进行处理：

```python
import qtawesome as qta

def get_icon(src: IconType, *args, **kwargs) -> QIcon | None:
 ...
 if isinstance(src, tuple):
     assert len(src) >= 2
     assert isinstance(src[0], str) and isinstance(src[1], (dict, list))
     if isinstance(src[1], dict):
         return qta.icon(src[0], **src[1])
     else:
         return qta.icon(src[0], *src[1])
 else:
     raise ValueError(f"invalid icon type: {type(src)}")
```

`utils.get_icon()`函数的完整代码如下：

```python
import qtawesome as qta
def get_icon(src: IconType, *args, **kwargs) -> Optional[QIcon]:
    if src is None:
        return None
    if isinstance(src, QIcon):
        return src
    if isinstance(src, QPixmap):
        return QIcon(src)
    if isinstance(src, str):
        if os.path.isfile(src) or src.startswith(":/"):
            return QIcon(src)
        return qta.icon(src, *args, **kwargs)
    if isinstance(src, tuple):
        assert len(src) >= 2
        assert isinstance(src[0], str) and isinstance(src[1], (dict, list))
        if isinstance(src[1], dict):
            return qta.icon(src[0], **src[1])
        else:
            return qta.icon(src[0], *src[1])
    else:
        raise ValueError(f"invalid icon type: {type(src)}")
```



