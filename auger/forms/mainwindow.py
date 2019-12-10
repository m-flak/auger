# pylint: disable=no-name-in-module
from PyQt5 import uic
from PyQt5.QtCore import Qt, QDir, QTimer, QVariant
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (
    QFileDialog, QGraphicsScene, QMainWindow, QMessageBox
)
from ..app import get_app_instance
from .resource import Resource, Resources, Ui

class MainWindow(QMainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags(Qt.Window)):
        super().__init__(parent, flags)

        self._area_to_process = tuple()

        # timer for resize events
        self.resize_timer = QTimer(self)
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.slot_resize_timeout)

        # pixmap for the loaded image
        self.pixmap_of_image = QPixmap()

        # Widgets will be in this class named as in QtDesigner
        # use CamelCase in QtDesigner and snake_case here
        uic.loadUi(Resources().resource(Resource.ResourceUi, which=Ui.UiMainWindow),
                   self)

        # Set Icon
        self.setWindowIcon(QIcon(Resources().resource(Resource.ResourceIcon)))

        # File Menu signals to slots
        self.actionOpen.triggered.connect(self.slot_file_open)
        self.actionSave_Output.triggered.connect(self.slot_file_save_output)
        self.actionQuit.triggered.connect(self.slot_file_quit)

        # Scene for `imageSide_Image`
        self.scene_for_image = QGraphicsScene(self.imageSide_Image)
        self.imageSide_Image.setScene(self.scene_for_image)
        # Assign Slots to `imageSide_Image`
        self.imageSide_Image.sig_select_start.connect(self.slot_select_start)
        self.imageSide_Image.sig_select_end.connect(self.slot_select_end)

        # Zoom In / Zoom Out of the Image
        self.imageSide_ZoomIn.clicked.connect(self.slot_zoom_in_click)
        self.imageSide_ZoomOut.clicked.connect(self.slot_zoom_out_click)

        # Process Selected button
        self.imageSide_SelectText.clicked.connect(self.slot_process_selected_click)

    @property
    def window_size(self):
        return (self.size().width(), self.size().height())

    @property
    def area_to_process(self):
        return self._area_to_process

    @area_to_process.setter
    def area_to_process(self, value):
        self._area_to_process = tuple(value)

    # Override method
    def resizeEvent(self, resize_event): # pylint: disable=invalid-name
        self.resize_timer.stop()
        self.resize_timer.start(175)
        return super().resizeEvent(resize_event)

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

    def slot_file_open(self):
        # prompt if an image already loaded
        if self.property('imageHasBeenLoaded') is True:
            discard_quest = QMessageBox.\
                            question(self, 'Discard Current Environment?',
                                     'Do you wish to discard any & all changes?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

            if discard_quest == QMessageBox.No:
                return

            # remove anything leftover in the scene
            self.imageSide_Image.scene().clear()

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

        # Attempt the load the image into a pixmap
        if not self.pixmap_of_image.load(image_to_open, None):
            QMessageBox.critical(self, 'Error Loading Image!',
                                 'Auger was unable to load the chosen image.',
                                 QMessageBox.Ok, QMessageBox.Ok)
            return

        # Add the Pixmap of the chosen image to the Image View
        # # Also fit it into the control.
        self.scene_for_image.addPixmap(self.pixmap_of_image)
        self.scene_for_image.setSceneRect(0, 0, self.pixmap_of_image.width(),
                                          self.pixmap_of_image.height())
        self.imageSide_Image.fitInView(self.scene_for_image.sceneRect(),
                                       Qt.KeepAspectRatio)

        self.statusbar.showMessage('Image Loaded. Select region with text...')
        self.setProperty('imageHasBeenLoaded', QVariant(True))

    def slot_file_save_output(self):
        print("Save Output Text...")

    def slot_file_quit(self):
        self.close()

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

        if not self.area_to_process:
            self.statusbar.showMessage('Select the region to process first...',
                                       500
                                      )
            return

        print("TODO: Process: {}".format(self.area_to_process))

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
        self.area_to_process = (x1, y1, x2-x1, y2-y1)
