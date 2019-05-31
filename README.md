# Background

为了在 Linux i3wm 环境中使用微信，通过 wine 安装了微信。
但微信启动后窗体周围的黑框遮挡了其他 workspace 的同一区域，
解决方法是在新的 i3 实例中单独启动微信：
`LC_ALL=zh_CN.UTF-8 wine 'C:\Program Files (x86)\Tencent\WeChat\WeChat.exe'`.

但不同 i3 实例间无法共享剪贴板，本应用为了解决这个问题，
将主 i3 环境（简称为 i3主）剪贴板中的文字内容通过 [i3ipc](https://i3wm.org/docs/ipc.html)
机制发送到微信所在的 i3 实例（简称为 i3从）中，将 i3从 中微信内容传递到 i3主 中。

# Prerequisites

本应用只用于 i3wm 环境中，通过调用 `xsel` 获取剪贴板内容，
通过 `xdotool` 向微信写入文本。
以上三者必须预选安装好。

如果要打包为 standalone 文件（见下面的 *Packege* 一节），
需要系统中预先安装对应版本的 `libpython3.x` 包，
例如 Pipfile 中使用 Python 3.6，则需要安装 `libpython3.6`
（用 `dpkg -l|grep libpython3.6` 验证）。

# Develop and Debug

在 console #1 中使用 `xsel -bo` 获取当前剪贴板内容。

在开发环境中运行：
```
pipenv install -d
pipenv run python send2wechat.py
```

或者：
```
$ pipenv install -d
$ pipenv shell
$ ipython
>>> %load send2wechat.py
>>>
```

# Package

为了将 Python 脚本及依赖打包为一个独立的可执行程序，
执行 `pipenv run pyinstaller -F send2wechat.py`，或者：
```
pipenv shell
pyinstaller -F send2wechat.py
cp dist/send2wechat ~/.local/bin/
```

# Usage

在 Linux 的两个 console 中分别启动两个 i3wm 实例，
i3主（对应 console #1，快捷键：Ctrl-Alt-F1）作为主工作空间
和 i3从（对应 console #2, 快捷键：Ctrl-Alt-F2）专门运行微信，
并确保微信是活跃窗口，焦点在微信文字输入框中。

在 i3主 中将需要发送到微信的文字保存到系统剪贴板中，
执行本应用（命令行中运行 `send2wechat`），
切换到 console #2 中，点击微信的 发送 按钮发送文本。

或者反过来，确保 i3主 当前窗口能编辑文字，
切换到 i3从，在微信中拷贝文字，执行 `send2wechat`，
切换回 i3 主，当前窗口中应该有微信拷贝的文字了。

P.S.: 为了提高效率，可以使用 i3 config 将 `send2wechat` 定义为快捷键。
