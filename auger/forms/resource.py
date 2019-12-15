import os

__all__ = (
    'Resource',
    'Ui',
    'Resources',
)

class Resource:
    ResourceIcon = 1
    ResourceUi = 2
    ResourceToolIcon = 3

class ToolIcon:
    ToolIconFontSize = 1

class Ui:
    UiMainWindow = 1
    UiSettingsDlg = 2

class Resources:
    def __init__(self):
        self._resources = {
            Resource.ResourceIcon: 'auger.png',
            Resource.ResourceUi: {
                Ui.UiMainWindow: 'mainwindow.ui',
                Ui.UiSettingsDlg: 'settingsdialog.ui',
            },
            Resource.ResourceToolIcon: {
                ToolIcon.ToolIconFontSize: 'tool_fontsize.png',
            },
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
