import os
import pytest

import PyQt5.QtWidgets as QWid
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QImage

from auger.document import TextDocument

@pytest.fixture
def png_image():
    png_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'img',
        'test.png'
    )
    return QImage(png_path, None), png_path

@pytest.fixture
def jpeg_image():
    jpeg_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'img',
        'test.jpg'
    )
    return QImage(jpeg_path, None), jpeg_path

class TestImageOCR:
    def _trigger_menu_item(self, items, item_caption):
        for menu_item in items:
            if item_caption in menu_item.text():
                menu_item.trigger()
                break

    def _get_inside_click_pos(self, widget):
        click_1 = (widget.x()+1, widget.y()+1)
        click_2 = (widget.width()-2, widget.height()-2)
        return widget.mapToParent(QPoint(*click_1)), widget.mapToParent(QPoint(*click_2))

    def test_image_ocr_png(self, qtbot, qapp, monkeypatch, png_image, auger_window):
        img_class = png_image[0]
        img_path = png_image[1]

        monkeypatch.setattr(
            target=QWid.QFileDialog,
            name='getOpenFileName',
            value=lambda *args, **kwargs: (img_path, 'Images (*.bmp *.png *.jpg *.jpeg)')
        )

        self._trigger_menu_item(
            auger_window.menuBar().findChild(QWid.QMenu, 'menuFile').actions(),
            'Open...'
        )

        click_1, click_2 = self._get_inside_click_pos(auger_window.imageSide_Image)

        qapp.image_document.selection = (
            click_1.x(),
            click_1.y(),
            click_2.x(),
            click_2.y()
        )

        qtbot.mouseClick(auger_window.imageSide_SelectText, Qt.LeftButton)
        test_words = 'I AM A TEST IMAGE'.split()
        found_words = 0
        for word in test_words:
            if word in TextDocument.get_raw_text(qapp.text_document):
                found_words += 1
        assert found_words > 0

    def test_image_ocr_jpeg(self, qtbot, qapp, monkeypatch, jpeg_image, auger_window):
        img_class = jpeg_image[0]
        img_path = jpeg_image[1]

        monkeypatch.setattr(
            target=QWid.QFileDialog,
            name='getOpenFileName',
            value=lambda *args, **kwargs: (img_path, 'Images (*.bmp *.png *.jpg *.jpeg)')
        )

        self._trigger_menu_item(
            auger_window.menuBar().findChild(QWid.QMenu, 'menuFile').actions(),
            'Open...'
        )

        click_1, click_2 = self._get_inside_click_pos(auger_window.imageSide_Image)

        qapp.image_document.selection = (
            click_1.x(),
            click_1.y(),
            click_2.x(),
            click_2.y()
        )

        qtbot.mouseClick(auger_window.imageSide_SelectText, Qt.LeftButton)
        test_words = 'I AM A TEST IMAGE'.split()
        found_words = 0
        for word in test_words:
            if word in TextDocument.get_raw_text(qapp.text_document):
                found_words += 1
        assert found_words > 0
