# Auger
>Auger is a GUI OCR tool for extracting text from images.

Have a screenshot but need it as a text file? Then, **_Auger_** is the tool for you!

You can select multiple regions of text within an image and format the results yourself.

* [Features](#features)
* [Installation](#installation)
* [Requirements](#requirements)
* [Screenshots](#screenshots)

## Features

#### Formatting
Auger offers you two ways of formatting your output within the program:
- HTML, with both a WYSIWYG and raw code view
- Text, with font and font size customizable

#### Images
Any image format compatible with the Qt library is compatible with Auger.

#### Languages
Languages supported by your OCR backend _(e.g.: Tesseract)_ are supported by Auger. Pick the language, select part of the image, and boom! It's that simple.

#### Output
Auger supports output into the following formats:
- Plain Text
- HTML

## Installation

Installing **_Auger_** is easy...

#### From Source Directory:
```bash
git clone https://github.com/m-flak/auger auger
cd auger
pip install -r requirements.txt
python auger.py
```

#### Using _setuptools_:
```bash
git clone https://github.com/m-flak/auger auger
cd auger
python setup.py build # YOU CAN USE ANY COMMAND SUPPORTED BY SETUPTOOLS
cd build/lib; python -m auger
```

## Requirements

* PyQt5
* Pillow
* pyocr
* lxml
* iso-language-codes

## Screenshots

**_December 24th, 2019:_**
![Screenshot_12-24-2019](https://user-images.githubusercontent.com/35634280/71423369-9fe34e00-264e-11ea-9fe3-b1dc6ea0e562.png)

**_December 16th, 2019:_**
![Screenshot_12-16-2019](https://user-images.githubusercontent.com/35634280/70937998-f3c8b400-200a-11ea-896e-8f84952cb84a.png)

**_December 14th, 2019:_**
![Screenshot_12-14-2019](https://user-images.githubusercontent.com/35634280/70853103-29d13100-1e6f-11ea-9285-4275c810d8d7.png)
