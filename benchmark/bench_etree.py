import sys, copy
from itertools import *
from StringIO import StringIO

import benchbase
from benchbase import with_attributes, with_text, onlylib, serialized

############################################################
# Benchmarks
############################################################

class BenchMark(benchbase.BenchMarkBase):
    def bench_iter_children(self, root):
        for child in root:
            pass

    def bench_iter_children_reversed(self, root):
        for child in reversed(root):
            pass

    @with_attributes(True, False)
    @with_text(text=True, utext=True)
    def bench_tostring_utf8(self, root):
        self.etree.tostring(root, 'UTF-8')

    @with_attributes(True, False)
    @with_text(text=True, utext=True)
    def bench_tostring_utf16(self, root):
        self.etree.tostring(root, 'UTF-16')

    @with_attributes(True, False)
    @with_text(text=True, utext=True)
    def bench_tostring_utf8_unicode_XML(self, root):
        xml = unicode(self.etree.tostring(root, 'UTF-8'), 'UTF-8')
        self.etree.XML(xml)

    @with_attributes(True, False)
    @with_text(text=True, utext=True)
    def bench_write_utf8_parse_stringIO(self, root):
        f = StringIO()
        self.etree.ElementTree(root).write(f, 'UTF-8')
        f.seek(0)
        self.etree.parse(f)

    @with_attributes(True, False)
    @with_text(text=True, utext=True)
    @serialized
    def bench_parse_stringIO(self, root_xml):
        f = StringIO(root_xml)
        self.etree.parse(f)

    @with_attributes(True, False)
    @with_text(text=True, utext=True)
    @serialized
    def bench_XML(self, root_xml):
        self.etree.XML(root_xml)

    @with_attributes(True, False)
    @with_text(text=True, utext=True)
    @serialized
    def bench_iterparse_stringIO(self, root_xml):
        f = StringIO(root_xml)
        for event, element in self.etree.iterparse(f):
            pass

    @with_attributes(True, False)
    @with_text(text=True, utext=True)
    @serialized
    def bench_iterparse_stringIO_clear(self, root_xml):
        f = StringIO(root_xml)
        for event, element in self.etree.iterparse(f):
            element.clear()

    def bench_append_from_document(self, root1, root2):
        # == "1,2 2,3 1,3 3,1 3,2 2,1" # trees 1 and 2, or 2 and 3, or ...
        for el in root2:
            root1.append(el)

    def bench_insert_from_document(self, root1, root2):
        for el in root2:
            root1.insert(len(root1)/2, el)

    def bench_rotate_children(self, root):
        # == "1 2 3" # runs on any single tree independently
        for i in range(100):
            el = root[0]
            del root[0]
            root.append(el)

    def bench_reorder(self, root):
        for i in range(1,len(root)/2):
            el = root[0]
            del root[0]
            root[-i:-i] = [ el ]

    def bench_reorder_slice(self, root):
        for i in range(1,len(root)/2):
            els = root[0:1]
            del root[0]
            root[-i:-i] = els

    def bench_clear(self, root):
        root.clear()

    def bench_has_children(self, root):
        for child in root:
            if child and child and child and child and child:
                pass

    def bench_len(self, root):
        for child in root:
            map(len, repeat(child, 20))

    def bench_create_subelements(self, root):
        SubElement = self.etree.SubElement
        for child in root:
            SubElement(child, '{test}test')

    def bench_append_elements(self, root):
        Element = self.etree.Element
        for child in root:
            el = Element('{test}test')
            child.append(el)

    def bench_makeelement(self, root):
        empty_attrib = {}
        for child in root:
            child.makeelement('{test}test', empty_attrib)

    def bench_create_elements(self, root):
        Element = self.etree.Element
        for child in root:
            Element('{test}test')

    def bench_replace_children_element(self, root):
        Element = self.etree.Element
        for child in root:
            el = Element('{test}test')
            child[:] = [el]

    def bench_replace_children(self, root):
        Element = self.etree.Element
        for child in root:
            child[:] = [ child[0] ]

    def bench_remove_children(self, root):
        for child in root:
            root.remove(child)

    def bench_remove_children_reversed(self, root):
        for child in reversed(root[:]):
            root.remove(child)

    def bench_set_attributes(self, root):
        for child in root:
            child.set('a', 'bla')

    @with_attributes(True)
    def bench_get_attributes(self, root):
        for child in root:
            child.get('bla1')
            child.get('{attr}test1')

    def bench_setget_attributes(self, root):
        for child in root:
            child.set('a', 'bla')
        for child in root:
            child.get('a')

    def bench_root_getchildren(self, root):
        root.getchildren()

    def bench_getchildren(self, root):
        for child in root:
            child.getchildren()

    def bench_get_children_slice(self, root):
        for child in root:
            child[:]

    def bench_get_children_slice_2x(self, root):
        for child in root:
            children = child[:]
            child[:]

    def bench_deepcopy(self, root):
        for child in root:
            copy.deepcopy(child)

    def bench_deepcopy_all(self, root):
        copy.deepcopy(root)

    def bench_tag(self, root):
        for child in root:
            child.tag

    def bench_tag_repeat(self, root):
        for child in root:
            for i in repeat(0, 100):
                child.tag

    @with_text(utext=True, text=True, no_text=True)
    def bench_text(self, root):
        for child in root:
            child.text

    @with_text(utext=True, text=True, no_text=True)
    def bench_text_repeat(self, root):
        repeat = range(500)
        for child in root:
            for i in repeat:
                child.text

    def bench_set_text(self, root):
        text = TEXT
        for child in root:
            child.text = text

    def bench_set_utext(self, root):
        text = UTEXT
        for child in root:
            child.text = text

    @onlylib('lxe')
    def bench_index(self, root):
        for child in root:
            root.index(child)

    @onlylib('lxe')
    def bench_index_slice(self, root):
        for child in root[5:100]:
            root.index(child, 5, 100)

    @onlylib('lxe')
    def bench_index_slice_neg(self, root):
        for child in root[-100:-5]:
            root.index(child, start=-100, stop=-5)

    def bench_getiterator_all(self, root):
        list(root.getiterator())

    def bench_getiterator_islice(self, root):
        list(islice(root.getiterator(), 10, 110))

    def bench_getiterator_tag(self, root):
        list(islice(root.getiterator(self.SEARCH_TAG), 3, 10))

    def bench_getiterator_tag_all(self, root):
        list(root.getiterator(self.SEARCH_TAG))

    def bench_getiterator_tag_text(self, root):
        [ e.text for e in root.getiterator(self.SEARCH_TAG) ]

    def bench_findall(self, root):
        root.findall(".//*")

    def bench_findall_tag(self, root):
        root.findall(".//" + self.SEARCH_TAG)

if __name__ == '__main__':
    benchbase.main(BenchMark)