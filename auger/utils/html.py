import lxml.html

class QuickTag:
    """ Callable to quickly create lxml element and access it.
    """
    def __init__(self, content, tag):
        self._tag = tag
        self._content = content
        self._element = lxml.html.Element(tag)
        self._element.text = content

    def __call__(self, as_element=True):
        """If `as_element` is `False`, return tuple of content, tag.
        Otherwise, lxml.html.Element class is returned.
        """
        if as_element:
            return self._element

        return self._content, self._tag

def clear_body_and_insert(html, insert_content, insert_tag):
    """Clears the body of an HTML string.
    Appends <insert_tag>insert_content</insert_tag> to the body.
    """
    document = lxml.html.fromstring(html)

    for kid in document.body.getchildren():
        document.body.remove(kid)

    return append_to_body(document, insert_content, insert_tag)

def append_to_body(html, append_content, append_tag):
    """Appends <append_tag>append_content</append_tag> to an HTML string or
    an lxml document.
    """
    if isinstance(html, lxml.html.HtmlElement):
        document = html
    else:
        document = lxml.html.fromstring(html)

    append_me = QuickTag(append_content, append_tag)

    document.body.append(append_me())

    return lxml.html.tostring(document, method='html', encoding='unicode')
