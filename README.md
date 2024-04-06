# 一个基于Pix2Text的识别文字和数学公式的macOS菜单栏应用程序

### 注意该应用程序仅适用于macOS

### 更新

- 新增了[自动识别（仅支持数学公式识别）](#auto-ocr)功能，以解决在长时间，多次数识别数学公式的场景下，需要手动按识别按钮的问题
- 新增了纯文本识别的功能和按钮
- 应用程序启动后，不在dock栏显示应用图标
- 修正了在识别过程用时较长的情况下，程序卡住（实际上在等待识别完成）的问题
- 更换了ocr识别模型，加强了手写体数学公式的识别
- 新增了数学公式和文本文档混合识别的功能

### 效果图

- 测试效果
  ![test.png](assets%2Ftest.png)
- 菜单栏应用的效果图
  ![menu_bar_style_auto_off.png](assets%2Fmenu_bar_style_auto_off.png)
  ![menu_bar_style_auto_on.png](assets%2Fmenu_bar_style_auto_on.png)

### 如何安装

- 克隆库

```angular2html
git clone https://github.com/horennel/LaTex-OCR_for_macOS.git
```

- 安装依赖环境

```angular2html
pip3 install -r requirements.txt
```

- 打包应用程序

```angular2html
python3 setup.py py2app -A
```

- 在生成的dist文件夹中可以看到应用程序`MyLatexOCR.app`，将其移动到`应用程序文件夹`即可

### 如何使用

- 启动程序
    - 启动应用`MyLatexOCR`，可以看到应用程序的菜单栏图标
- 截图
    - 使用任意截图软件，例如`Snipaste`，截图并复制到剪切板
- 识别
    - 仅识别数学公式
        - 点击`Formula OCR`按钮
        - 识别成功后，会收到通知栏的通知
    - 识别数学公式和文字的混合
        - 点击`Mixed OCR`按钮
        - 识别成功后，会收到通知栏的通知
    - 仅识别文字
        - 点击`Text OCR`按钮
        - 识别成功后，会收到通知栏的通知
    - 如果不想接受通知可以在系统设置里关闭通知
    - 收到通知后，即可粘贴Latex公式和文字到任意地方
- 自动识别（仅支持数学公式识别）<span id="auto-ocr">
    - 启动和关闭自动识别
        - 点击`Auto On/Off`按钮，菜单栏图标`暗黑`为已启动自动识别功能，`明亮`为已关闭自动识别功能
    - 使用
        - 启动自动识别功能后，不需要再点击其他按钮，程序会自动读取剪切板的图片识别
    - 注意事项⚠️
        - 因为程序是自动读取剪切板中的图片，所以程序无法准确知道当前剪切板的图片是否需要识别
        - 如果开启自动识别功能后，复制了不需要识别的图片，会引起系统资源的浪费和刚复制到剪切板图片丢失
        - 鉴于以上两点，建议如果需要连续，长时间，多次识别数学公式时，可以开启自动识别功能

### 注意事项

- 第一次启动应用程序时会下载模型和配置文件，导致第一次启动时间过长，后续启动会恢复到正常速度
- 模型和配置文件下载后的存储路径位于`～/.cnstd`和`~/.cnocr`和`~/.pix2text`
- 应用程序依赖打包应用程序时的python环境，若python环境发成改变（例如：1.打包时使用的虚拟环境被删除 2.打包时使用的环境中的依赖库被删除修改
  3.电脑上的python环境被彻底卸载等情况），会导致应用程序无法正常使用，需重新打包

### 感谢开源图标作者

- [ELÍAS的个人主页](https://eliasruiz.com/)

### 如何二次开发

- [macOS菜单栏应用开发：rumps文档](https://rumps.readthedocs.org)
- [macOS应用程序构建：py2app文档](https://py2app.readthedocs.io)

### 感谢以下开源作者

- [Pix2Text公式和文字识别：Pix2Text](https://github.com/breezedeus/Pix2Text)
- [复制和粘贴剪贴板：pyperclip](https://github.com/asweigart/pyperclip)
- [macOS菜单栏应用程序：rumps](https://github.com/jaredks/rumps)
- [macOS应用程序构建：py2app](https://github.com/ronaldoussoren/py2app)
- [图像处理：pillow](https://github.com/python-pillow/Pillow)