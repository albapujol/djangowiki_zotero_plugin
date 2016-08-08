# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .zotero import zotero_port

import markdown
from pprint import pprint

ZOTERO_RE = r'\[zotero\:(?P<ref>[A-Z0-9]*)\]'

class ZoteroPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        data = zotero_port.get_element(m.group(2))
        innertext = """
                Reference: <a href='%(url)s'>%(url)s</a> <br />
                <a role='button' data-toggle='collapse' href='#%(key)s_abstract' aria-expanded='false'
                    aria-controls='%(key)s_abstract'>
                        Abstract
                </a>
                <div class='collapse' id='%(key)s_abstract'>
                    <pre><code>%(abstract)s</code></pre>
                </div> <br />
                <a role='button' data-toggle='collapse' href='#%(key)s_bibtex' aria-expanded='false'
                    aria-controls='%(key)s_bibtex'>
                        Bibtex
                </a>
                <div class='collapse' id='%(key)s_bibtex'>
                    <pre><code>%(bibtex)s</code></pre>
                </div>
            """ % data
        el = markdown.util.etree.Element("span")
        # el.attrib["href"] = "#"
        el.attrib["id"] = m.group(2)
        el.attrib["class"] = "zotero-span"
        el.attrib["data-toggle"] = "popover"
        el.attrib["title"] = data['citation']
        el.attrib["data-placement"] = "bottom"
        el.attrib["style"] = "width:100%; color:darkcyan"
        el.attrib["data-content"] = innertext
            # "<a  role='button' data-toggle='collapse' " \
            #                         "href='#collapseExample' aria-expanded='false' " \
            #                         "aria-controls='collapseExample'> Link with href </a>" \
            #                         "<div class='collapse' id='collapseExample'>" + \
            #                         data['url'] + data['abstract'] + \
            #                         "</div>"
        el.text = "[" + data['bibtex_key'] + "]"
        return el

class ZoteroTreeProcessor(markdown.treeprocessors.Treeprocessor):
    def run(self, tree):
        # Get all tags
        zotero_tags = []
        for el in tree.iter():
            try:
                if el.attrib["class"] == "zotero-span":
                    if el.attrib["id"] not in zotero_tags:
                        zotero_tags.append(el.attrib["id"])
            except KeyError:
                pass
        # Append something

           #
           #  <div class="panel panel-default">
           #     <div class="panel-heading">
           #         <h4 class="panel-title">
           #             <a class="collapsed" href="#zotero_bibtex" role="button" data-toggle="collapse">
           #                 Collapsible Group Item #1
           #             </a>
           #         </h4>
           #     </div>
           #     <div style="height: 0px;" aria-expanded="false" class="panel-collapse collapse"
           #          role="tabpanel" id="zotero_bibtex">
           #         <div class="panel-body">
           #             Booody.
           #         </div>
           #     </div>
           # </div>
           #

        if zotero_tags:
            main_div = markdown.util.etree.Element("div", {"class": "panel panel-default"})
            nested = markdown.util.etree.SubElement(main_div, "div", {"class": "panel-heading"})
            nested = markdown.util.etree.SubElement(nested, "h4", {"class": "panel-title"})
            nested = markdown.util.etree.SubElement(nested, "a", {"class": "collapsed",
                                                                  "href": "#zotero-bibtex",
                                                                  "role": "button",
                                                                  "data-toggle": "collapse"})
            nested.text = "Bibtex references"
            nested = markdown.util.etree.SubElement(main_div, "div", {"style": "height: 0px;",
                                                                      "aria-expanded": "false",
                                                                      "class": "panel-collapse collapse",
                                                                      "role": "tabpanel",
                                                                      "id": "zotero-bibtex"})
            nested = markdown.util.etree.SubElement(nested, "h4", {"class": "panel-body"})
            nested = markdown.util.etree.SubElement(nested, "div", {})
            nested = markdown.util.etree.SubElement(nested, "pre", {"style": "max-width:100%; max-height:100%;"})
            nested = markdown.util.etree.SubElement(nested, "code", {})
            nested.text = ""
            for tag in zotero_tags:
                data = zotero_port.get_element(tag)
                # parsed = markdown.util.etree.fromstring(data["bibtex"])
                # nested.append(parsed)
                nested.text += data["bibtex"] + '\n'
            tree.append(main_div)
        return tree


class ZoteroExtension(markdown.Extension):

    """ Images plugin markdown extension for django-wiki. """

    def extendMarkdown(self, md, md_globals):
        """ Insert ImagePreprocessor before ReferencePreprocessor. """
        # md.preprocessors.add('dw-zotero', ZoteroPreprocessor(md), '>html_block')
        zot_pattern = ZoteroPattern(ZOTERO_RE, markdown_instance=md)
        zot_pattern.md = md
        md.inlinePatterns.add('dw-zotero-pattern', zot_pattern, "<reference")
        print("extension loaded")
        zot_tree = ZoteroTreeProcessor(md)
        md.treeprocessors.add("dw-zotero-bibtex", zot_tree, "_end")
        # md.postprocessors.add('dw-zotero-summary', ZoteroPostprocessor(md), '>raw_html')


def makeExtension():
    return ZoteroExtension()

# class ZoteroPostprocessor(markdown.postprocessors.Postprocessor):
#
#     def run(self, text):
#         return text
