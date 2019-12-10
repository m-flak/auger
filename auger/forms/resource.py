import os

__all__ = (
    'Resource',
    'Ui',
    'Resources',
)

class Resource:
    ResourceIcon = 1
    ResourceUi = 2

class Ui:
    UiMainWindow = 1

class Resources:
    def __init__(self):
        self._resources = {
            Resource.ResourceIcon: 'auger.png',
            Resource.ResourceUi: {
                Ui.UiMainWindow: 'mainwindow.ui',
            },
        }

        self._cwd = os.path.abspath(os.path.dirname(__file__))

        self._res_directory = 'res'
        self._ui_directory = 'ui'

    def resource(self, what_resource, **kwargs):
        if what_resource == Resource.ResourceUi:
            which = kwargs.get('which', None)
            if which is None:
                raise ValueError('Resource.ResourceUi requires kwarg: which.')
            return os.path.join(
                self._cwd,
                self._ui_directory,
                self._resources[what_resource][which]
            )

        return os.path.join(
            self._cwd,
            self._res_directory,
            self._resources[what_resource]
        )
