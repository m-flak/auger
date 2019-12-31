import os

__all__ = (
    'Resource',
    'ToolIcon',
    'Ui',
    'Resources',
)

class Resource:
    ResourceIcon = 1
    ResourceUi = 2
    ResourceToolIcon = 3
    ResourceStyleSheet = 4

class ToolIcon:
    ToolIconFontSize = 1
    ToolIconZoomIn = 2
    ToolIconZoomOut = 3
    ToolIconLanguages = 4
    ToolIconAppendOn = 5
    ToolIconAppendOff = 6
    ToolIconUndo = 7
    ToolIconRedo = 8

class Ui:
    UiMainWindow = 1
    UiSettingsDlg = 2
    UiAboutDlg = 3

class Resources:
    def __init__(self):
        self._resources = {
            Resource.ResourceIcon: 'auger.png',
            Resource.ResourceUi: {
                Ui.UiMainWindow: 'mainwindow.ui',
                Ui.UiSettingsDlg: 'settingsdialog.ui',
                Ui.UiAboutDlg: 'aboutdialog.ui',
            },
            Resource.ResourceToolIcon: {
                ToolIcon.ToolIconFontSize: 'tool_fontsize.png',
                ToolIcon.ToolIconZoomIn: 'tool_zoomin.png',
                ToolIcon.ToolIconZoomOut: 'tool_zoomout.png',
                ToolIcon.ToolIconLanguages: 'tool_languages.png',
                ToolIcon.ToolIconAppendOn: 'tool_append_on.png',
                ToolIcon.ToolIconAppendOff: 'tool_append_off.png',
                ToolIcon.ToolIconUndo: 'tool_undo.png',
                ToolIcon.ToolIconRedo: 'tool_redo.png',
            },
            Resource.ResourceStyleSheet: 'stylesheet.qss',
        }

        self._cwd = os.path.abspath(os.path.dirname(__file__))

        self._res_directory = 'res'
        self._ui_directory = 'ui'

    def resource(self, what_resource, **kwargs):
        which = kwargs.get('which', None)

        if what_resource in (Resource.ResourceUi, Resource.ResourceToolIcon):
            if which is None:
                raise ValueError('{} requires kwarg: which.'.format(what_resource))

        if what_resource == Resource.ResourceUi:
            return os.path.join(
                self._cwd,
                self._ui_directory,
                self._resources[what_resource][which]
            )

        # If the `which` parameter is needed, then do it
        try:
            return os.path.join(
                self._cwd,
                self._res_directory,
                self._resources[what_resource]
            )
        except TypeError:
            return os.path.join(
                self._cwd,
                self._res_directory,
                self._resources[what_resource][which]
            )
