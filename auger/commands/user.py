from ..utils.html import clear_body_and_insert, append_to_body
from .command import Command

class TextCommand(Command):
    """Base class for commands mucking about with our tabbed text views.

    `tab_ref` MUST be a reference. Use a lambda because Python sees pointers as
    values.

    `tabs` MUST CONTAIN THESE KEYS: 'html_tab' and 'text_tab' tied to the widgets.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tab_ref = kwargs.get('tab_ref', None)
        self.tab_dict = kwargs.get('tabs', dict())

        assert self.tab_ref is not None
        # Lambda must be used for the tab reference or Python will store it by value >:{ ):<
        assert isinstance(self.tab_ref, type(lambda: 0))
        assert 'html_tab' in self.tab_dict.keys() and 'text_tab' in self.tab_dict.keys()

    def _set_target_by_tab(self):
        if 'tabHtmlEdit' in self.tab_ref().objectName():
            self.target = self.tab_dict['html_tab']
        elif 'tabTextEdit' in self.tab_ref().objectName():
            self.target = self.tab_dict['text_tab']
        else:
            raise AttributeError('Tab reference objectName() returned \'\'!')

    def operation(self):
        self._set_target_by_tab()

    def reverse_operation(self):
        self._set_target_by_tab()

########################################
# TEXT COMMANDS
########################################
class TextOverwriteCommand(TextCommand):
    def operation(self):
        super().operation()
        is_rich_text = False

        if 'text' in self.target.property('augerTextEditType'):
            if self.old_data is None:
                self.old_data = self.target.toHtml()
            is_rich_text = True
        elif 'html' in self.target.property('augerTextEditType'):
            if self.old_data is None:
                self.old_data = self.target.toPlainText()
        else:
            raise AttributeError('Meta property: \'augerTextEditType\' required!')

        new_contents = clear_body_and_insert(
            self.old_data,
            self.data,
            'p'
        )

        if is_rich_text:
            self.target.setHtml(new_contents)
        else:
            self.target.setPlainText(new_contents)

    def reverse_operation(self):
        super().reverse_operation()

        if 'text' in self.target.property('augerTextEditType'):
            self.target.setHtml(self.old_data)
        elif 'html' in self.target.property('augerTextEditType'):
            self.target.setPlainText(self.old_data)
        else:
            raise AttributeError('Meta property: \'augerTextEditType\' required!')

class TextAppendCommand(TextCommand):
    def operation(self):
        super().operation()
        is_rich_text = False

        if 'text' in self.target.property('augerTextEditType'):
            if self.old_data is None:
                self.old_data = self.target.toHtml()
            is_rich_text = True
        elif 'html' in self.target.property('augerTextEditType'):
            if self.old_data is None:
                self.old_data = self.target.toPlainText()
        else:
            raise AttributeError('Meta property: \'augerTextEditType\' required!')

        new_contents = append_to_body(
            self.old_data,
            *self.data(False) # is a QuickTag, unpack it as tuple
        )

        if is_rich_text:
            self.target.setHtml(new_contents)
        else:
            self.target.setPlainText(new_contents)

    def reverse_operation(self):
        super().reverse_operation()

        if 'text' in self.target.property('augerTextEditType'):
            self.target.setHtml(self.old_data)
        elif 'html' in self.target.property('augerTextEditType'):
            self.target.setPlainText(self.old_data)
        else:
            raise AttributeError('Meta property: \'augerTextEditType\' required!')
