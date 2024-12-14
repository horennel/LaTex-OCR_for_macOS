# A macOS Menu Bar Application for Text and Math Formula Recognition Based on Pix2Text

[简体中文](README_cn.md)

### Note: This application is for macOS only

### Updates

- 2024-04-26 Added [Auto Recognition (supports three modes)](#auto-ocr) feature to solve the issue of manually clicking recognition button in long-term, multiple recognition scenarios
- Added [Auto Recognition (math formula recognition only)](#auto-ocr) feature
- Added text-only recognition function and button
- Application icon no longer shows in dock after launch
- Fixed program freezing issue during long recognition processes
- Updated OCR recognition model to enhance handwritten math formula recognition
- Added mixed recognition for math formulas and text documents

### Screenshots

- Test Results
  ![test.png](assets%2Ftest.png)
- Menu Bar Application Interface
  ![menu_bar_style_auto_off.png](assets%2Fmenu_bar_style_auto_off.png)
  ![menu_bar_style_auto_on.png](assets%2Fmenu_bar_style_auto_on.png)

### Installation

- Clone Repository

```angular2html
git clone https://github.com/horennel/LaTex-OCR_for_macOS.git
```

- Install Dependencies

```angular2html
pip3 install -r requirements.txt
```

- Package Application

```angular2html
python3 setup.py py2app -A
```

- Move the generated `MyLatexOCR.app` from the dist folder to your Applications folder

### Usage

- Launch
    - Start `MyLatexOCR`, you'll see the application icon in the menu bar
- Screenshot
    - Use any screenshot tool (e.g., `Snipaste`) to capture and copy to clipboard
- Recognition
    - Math Formula Only
        - Click `Formula OCR` button
        - You'll receive a notification upon successful recognition
    - Mixed Math Formula and Text
        - Click `Mixed OCR` button
        - You'll receive a notification upon successful recognition
    - Text Only
        - Click `Text OCR` button
        - You'll receive a notification upon successful recognition
    - Notifications can be disabled in system settings
    - After receiving notification, you can paste the LaTeX formula and text anywhere
- <span id="auto-ocr">Auto Recognition (supports `Math Formula Mode`, `Mixed Mode`, `Text-Only Mode`)
    - Enable/Disable Auto Recognition
        - Click `Auto On/Off` button to toggle auto recognition
        - Dark menu bar icon indicates auto recognition is enabled
        - Light menu bar icon indicates auto recognition is disabled
    - Usage
        - After enabling auto recognition (defaults to `Math Formula Mode`), click the corresponding mode button
        - Selected mode button becomes unclickable with a `√` prefix
        - No further clicks needed, program automatically recognizes clipboard images
    - Important Notes ⚠️
        - Program automatically processes clipboard images but cannot determine if recognition is needed
        - Copying unneeded images with auto recognition enabled wastes system resources
        - Recommended to enable auto recognition only when continuous recognition is needed

### Important Notes

- First launch will download models and configuration files, causing longer initial startup time
- Model and config files are stored in `～/.cnstd`, `~/.cnocr`, and `~/.pix2text`
- Application depends on Python environment used during packaging. Repackaging needed if environment changes

### Credits for Icon

- [ELÍAS Homepage](https://eliasruiz.com/)

### Development Resources

- [macOS Menu Bar App Development: rumps Documentation](https://rumps.readthedocs.org)
- [macOS Application Building: py2app Documentation](https://py2app.readthedocs.io)

### Thanks to Open Source Projects

- [Formula and Text Recognition: Pix2Text](https://github.com/breezedeus/Pix2Text)
- [Clipboard Operations: pyperclip](https://github.com/asweigart/pyperclip)
- [macOS Menu Bar Application: rumps](https://github.com/jaredks/rumps)
- [macOS Application Building: py2app](https://github.com/ronaldoussoren/py2app)
- [Image Processing: pillow](https://github.com/python-pillow/Pillow)