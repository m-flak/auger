# pylint: disable=no-name-in-module
from PyQt5 import uic
from PyQt5.QtCore import Qt, QDir, QTimer, QVariant
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QFileDialog, QMainWindow, QMessageBox
)
from ..app import get_app_instance
from ..commands import TextOverwriteCommand, TextAppendCommand
from ..document import ImageDocument, TextDocument
from ..utils.html import QuickTag
from .resource import Resource, Resources, Ui, ToolIcon
from .settingsdialog import SettingsDialog
from .aboutdialog import AboutDialog

class MainWindow(QMainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags(Qt.Window)):
        super().__init__(parent, flags)

        self._settings_dialog = None
        self._about_dialog = None
        self._append_text = False

        # timer for resize events
        self.resize_timer = QTimer(self)
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.slot_resize_timeout)

        # Create the text document for textSide
        get_app_instance().text_document = TextDocument()

        # get the welcome message
        with open(Resources().resource(Resource.ResourceWelcomeHTML), 'r') as f:
            welcome_msg = f.read()

        # load the welcome message into the document
        get_app_instance().text_document.contents.setHtml(welcome_msg)

        # Widgets will be in this class named as in QtDesigner
        # use CamelCase in QtDesigner and snake_case here
        uic.loadUi(Resources().resource(Resource.ResourceUi, which=Ui.UiMainWindow),
                   self)

        # now that ui components are loaded, set the edits to the contents of document
        self.textSide_textEdit.setHtml(get_app_instance().text_document.contents.toHtml())
        self.textSide_htmlEdit.setPlainText(get_app_instance().text_document.contents.toHtml())

        # Set Icon
        self.setWindowIcon(QIcon(Resources().resource(Resource.ResourceIcon)))

        # Set Icons for the zoom buttons
        self.imageSide_ZoomIn.setIcon(
            QIcon(Resources().resource(Resource.ResourceToolIcon, which=ToolIcon.ToolIconZoomIn))
        )
        self.imageSide_ZoomOut.setIcon(
            QIcon(Resources().resource(Resource.ResourceToolIcon, which=ToolIcon.ToolIconZoomOut))
        )

        # Set Icons for select languages button
        self.imageSide_UseLanguage.setIcon(
            QIcon(Resources().resource(Resource.ResourceToolIcon, which=ToolIcon.ToolIconLanguages))
        )

        # File Menu signals to slots
        self.actionOpen.triggered.connect(self.slot_file_open)
        self.actionSave_Output.triggered.connect(self.slot_file_save_output)
        self.actionQuit.triggered.connect(self.slot_file_quit)

        # Edit Menu signals to slots
        self.actionSettings.triggered.connect(self.slot_edit_settings)

        # Help Menu signals to slots
        self.actionAbout_Auger.triggered.connect(self.slot_help_about)

        # Setup for `imageSide_Image`
        get_app_instance().image_document = ImageDocument(self.imageSide_Image)
        self.imageSide_Image.setScene(get_app_instance().image_document.contents)
        # Assign Slots to `imageSide_Image`
        self.imageSide_Image.sig_select_start.connect(self.slot_select_start)
        self.imageSide_Image.sig_select_end.connect(self.slot_select_end)

        # Zoom In / Zoom Out of the Image
        self.imageSide_ZoomIn.clicked.connect(self.slot_zoom_in_click)
        self.imageSide_ZoomOut.clicked.connect(self.slot_zoom_out_click)

        # Process Selected button
        self.imageSide_SelectText.clicked.connect(self.slot_process_selected_click)

        # Text Tabs Clicked
        self.textSide_tabView.tabBarClicked.connect(self.slot_tab_clicked)

        # Text Edit Changed
        self.textSide_textEdit.textChanged.connect(self.slot_textedit_changed)

        # Text Edit Font Changed / Size Changed
        self.textSide_toolBar.sig_font_changed.connect(
            self.textSide_textEdit.setFontFamily
        )
        self.textSide_toolBar.sig_font_changed.connect(self.slot_update_font_fam)
        self.textSide_toolBar.sig_size_changed.connect(
            self.textSide_textEdit.setFontPointSize
        )
        self.textSide_toolBar.sig_size_changed.connect(self.slot_update_font_sz)

        # Text Edit toggle append or overwrite
        self.textSide_toolBar.sig_ao_toggle.connect(self.slot_toggle_append)

        # HTML Edit Font Changed / Size Changed
        self.textSide_toolBar.sig_font_changed.connect(
            self.textSide_htmlEdit.setFontFamily
        )
        self.textSide_toolBar.sig_size_changed.connect(
            self.textSide_htmlEdit.setFontPointSize
        )

        # Connect OCR perform signal
        get_app_instance().ocr.sig_performed.connect(self.slot_ocr_performed)

        # Connect OCR use language change signal
        get_app_instance().ocr.sig_change_lang.connect(self.slot_ocr_change_lang)

        # Connect OCR error handler
        get_app_instance().ocr.sig_ocr_error.connect(self.slot_ocr_error_handle)

    @property
    def window_size(self):
        return (self.size().width(), self.size().height())

    @property
    def append_text(self):
        return self._append_text

    @append_text.setter
    def append_text(self, value):
        self._append_text = bool(value)

    # Override method
    def closeEvent(self, close_event): # pylint: disable=invalid-name
        was_maximized = False

        if self.isMaximized() or self.windowState() & Qt.WindowMaximized == Qt.WindowMaximized:
            was_maximized = True

        get_app_instance().settings.setValue('was_maximized', was_maximized)

        return super().closeEvent(close_event)

    # Override method
    def resizeEvent(self, resize_event): # pylint: disable=invalid-name
        self.resize_timer.stop()
        self.resize_timer.start(175)
        return super().resizeEvent(resize_event)

    # Override method
    def show(self): # pylint: disable=invalid-name
        # get font & size from before
        auger_cfg = get_app_instance().settings
        editor_font = auger_cfg.value('font_family', type=str)
        editor_szfont = auger_cfg.value('font_size', type=int)
        # get the 'use' & 'default' language from before
        use_lang = auger_cfg.value('use_language', type=str)
        def_lang = auger_cfg.value('default_language', type=str)

        if editor_font and editor_szfont > 0:
            self.textSide_toolBar.set_font_properties(editor_font, editor_szfont)

        if use_lang or def_lang:
            lang = use_lang if use_lang else def_lang
            self.imageSide_UseLanguage.mark_active_language(lang)

        return super().show()

    ########### SLOTS ############## SLOTS ############# SLOTS ##############

    def slot_resize_timeout(self):
        self.resize_timer.stop()
        width, height = self.window_size
        menu_height = self.menubar.height()
        status_height = self.statusbar.height()
        # The HBox's width needs to be 5px less than window
        # The HBox's height is that of without the menubar & statusbar
        self.horizontalLayoutWidget.resize(width-5,
                                           height-menu_height-status_height)

        # resize the text edits to tab size
        edit_tabs = [
            self.textSide_textEdit.parent(),
            self.textSide_htmlEdit.parent()
        ]
        # the 2nd tab is not the same size as the 1st tab. why??
        # this keeps both the text edits in both tabs of the same size
        for index, tab in enumerate(edit_tabs):
            if tab is self.textSide_tabView.currentWidget():
                other = index ^ 1
                tab.children()[0].resize(tab.size())
                edit_tabs[other].children()[0].resize(tab.size())
                break

        # preserve the new window size persistently
        auger_cfg = get_app_instance().settings
        auger_cfg.setValue('window_width', width)
        auger_cfg.setValue('window_height', height)

    def slot_file_open(self):
        # prompt if an image already loaded
        if self.property('imageHasBeenLoaded') is True:
            discard_quest = QMessageBox.\
                            question(self, 'Discard Current Image?',
                                     'Do you wish to discard the current image?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

            if discard_quest == QMessageBox.No:
                return

            # remove anything leftover in the scene
            get_app_instance().image_document.reset_document()

            # reset state for scene & window
            self.imageSide_Image.resetTransform()
            self.setProperty('imageHasBeenLoaded', QVariant(False))
        # # # #
        # show open file dialog from user's home folder
        open_from_here = QDir.toNativeSeparators(QDir.homePath())
        image_to_open = QFileDialog.getOpenFileName(self, 'Open an Image...',
                                                    open_from_here,
                                                    'Images (*.bmp *.png *.jpg *.jpeg)')
        # fix & retrieve the returned path
        image_to_open = QDir.toNativeSeparators(image_to_open[0])
        # dialog was closed
        if not image_to_open:
            return

        # Attempt to load the image
        if not get_app_instance().image_document.load_document(lambda p: p.load(image_to_open, None)):
            QMessageBox.critical(self, 'Error Loading Image!',
                                 'Auger was unable to load the chosen image.',
                                 QMessageBox.Ok, QMessageBox.Ok)
            return

        # Fit the image into the view control
        self.imageSide_Image.fitInView(
            get_app_instance().image_document.contents.sceneRect(),
            Qt.KeepAspectRatio
        )

        self.statusbar.showMessage('Image Loaded. Select region with text...')
        self.setProperty('imageHasBeenLoaded', QVariant(True))

    def slot_file_save_output(self):
        open_from_here = QDir.toNativeSeparators(QDir.homePath())
        output_file, output_extension = QFileDialog.getSaveFileName(
            self,
            'Save Output Text...',
            open_from_here,
            'Text Files (*.txt);;HTML Files (*.html *.htm)'
        )

        output_format = 'html' if 'htm' in output_extension else 'text'
        with open(output_file, 'w') as f:
            get_app_instance().text_document.save_document(f, output_format)

    def slot_file_quit(self):
        self.close()

    def slot_edit_settings(self):
        if self._settings_dialog is not None:
            self._settings_dialog = None

        self._settings_dialog = SettingsDialog(self)
        self._settings_dialog.open()

    def slot_help_about(self):
        if self._about_dialog is not None:
            self._about_dialog = None

        self._about_dialog = AboutDialog(self)
        self._about_dialog.open()

    def slot_select_start(self, start):
        x, y = start
        self.statusbar.showMessage('Selection Started: ({}, {})'.format(x, y))

    def slot_select_end(self, start, end):
        x1, y1 = start
        x2, y2 = end

        self.statusbar.showMessage('Selection Ended: ({}, {})'.\
                                   format(x2, y2),
                                   500
                                  )
        get_app_instance().image_document.selection = (x1, y1, x2-x1, y2-y1)

    def slot_zoom_in_click(self):
        if self.property('imageHasBeenLoaded') is True:
            self.imageSide_Image.scale(1.2, 1.2)

    def slot_zoom_out_click(self):
        if self.property('imageHasBeenLoaded') is True:
            self.imageSide_Image.scale(1/1.2, 1/1.2)

    def slot_process_selected_click(self):
        if self.property('imageHasBeenLoaded') is not True:
            self.statusbar.showMessage('Please load an image first.')
            return

        if not get_app_instance().image_document.has_selection:
            self.statusbar.showMessage('Select the region to process first...',
                                       500
                                      )
            return

        if not get_app_instance().ocr.tools:
            QMessageBox.critical(
                self,
                'No suitable OCR tool found on system!',
                'Auger was unable to find an OCR backend.\nPlease install an OCR backend such as Tesseract.',
                QMessageBox.Ok,
                QMessageBox.Ok
            )
            return

        # Perform OCR :)
        get_app_instance().ocr.perform_ocr(
            get_app_instance().image_document.get_selection_as_image()
        )

    def slot_tab_clicked(self, index):
        if index > -1 and index != self.textSide_tabView.currentIndex():
            # clicking 'Text' from 'HTML'
            if index == 0:
                try:
                    self.textSide_htmlEdit.transfer_text_to_other_html(
                        self.textSide_textEdit
                    )
                    self.textSide_htmlEdit.setProperty('augerActiveTextEdit', False)
                    self.textSide_textEdit.setProperty('augerActiveTextEdit', True)
                except TypeError:
                    return
            # clicking 'HTML' from 'Text'
            elif index == 1:
                try:
                    self.textSide_textEdit.transfer_html_to_other_text(
                        self.textSide_htmlEdit
                    )
                    self.textSide_htmlEdit.setProperty('augerActiveTextEdit', True)
                    self.textSide_textEdit.setProperty('augerActiveTextEdit', False)
                except TypeError:
                    return

    def slot_textedit_changed(self):
        self.textSide_textEdit.setReadOnly(False)
        self.actionSave_Output.setEnabled(True)
        self.textSide_toolBar.setEnabled(True)

    def slot_ocr_performed(self, ocr_text):
        # empty string has resulted :(
        if not ocr_text:
            self.statusbar.showMessage('Unable to recognize text. Try again.', 500)
            return

        if not self.append_text:
            get_app_instance().cmd_mgr.execute_new_command(
                TextOverwriteCommand(
                    #currentWidget returns a pointer which python will store by
                    #value and we don't f***ing want that...
                    tab_ref=lambda t=self.textSide_tabView.currentWidget: t(),
                    tabs={
                        'text_tab': self.textSide_textEdit,
                        'html_tab': self.textSide_htmlEdit,
                    },
                    data=ocr_text
                )
            )
        else:
            get_app_instance().cmd_mgr.execute_new_command(
                TextAppendCommand(
                    tab_ref=lambda t=self.textSide_tabView.currentWidget: t(),
                    tabs={
                        'text_tab': self.textSide_textEdit,
                        'html_tab': self.textSide_htmlEdit,
                    },
                    data=QuickTag(ocr_text, 'p')
                )
            )

        self.statusbar.showMessage('Text recognized. OCR successful.', 500)

    def slot_update_font_fam(self, family): # pylint: disable=no-self-use
        get_app_instance().settings.setValue('font_family', family)

    def slot_update_font_sz(self, size): # pylint: disable=no-self-use
        get_app_instance().settings.setValue('font_size', size)

    def slot_ocr_change_lang(self, lang):
        self.statusbar.showMessage('OCR Language changed to: {}.'.format(lang), 500)

    def slot_ocr_error_handle(self, error):
        QMessageBox.critical(
            self,
            'OCR Error Occurred!',
            'An error was encountered when attempting to perform OCR:\n\n{}'.format(error),
            QMessageBox.Ok,
            QMessageBox.Ok
        )

    def slot_toggle_append(self, yes_or_no):
        self.append_text = yes_or_no
