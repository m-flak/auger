import lxml.html

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

    append_me = lxml.html.Element(append_tag)
    append_me.text = append_content

    document.body.append(append_me)

    return lxml.html.tostring(document, method='html', encoding='unicode')
