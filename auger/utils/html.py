import lxml.html

def clear_body_and_insert(html, insert_content, insert_tag):
    """Clears the body of an HTML string.
    Appends <insert_tag>insert_content</insert_tag> to the body.
    """
    document = lxml.html.fromstring(html)
    insert_me = lxml.html.Element(insert_tag)

    insert_me.text = insert_content

    for kid in document.body.getchildren():
        document.body.remove(kid)

    document.body.append(insert_me)

    return lxml.html.tostring(document, method='html', encoding='unicode')
