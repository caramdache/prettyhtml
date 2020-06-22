#!/usr/bin/python3

import os
import sys
import textwrap

from html.parser import HTMLParser

class PrettyHTML(HTMLParser):
    def __init__(self, file):
        HTMLParser.__init__(self)

        self.file = file

        self.merged_cells = {}
        self.row = 0
        self.col = 0

        self.level = 0

    def indent(self):
        return '  ' * self.level

    def handle_starttag(self, tag, attrs):
        if tag in ['figure', 'p', 'mark', 'u', 'underline', 'b', 'strong', 'i', 'em', 's', 'strike', 'br', 'img']:
            return

        self.write_starttag(tag, attrs)

        self.level += 1

        if tag == 'tr':
            # Handle colspans from previous rows.
            self.skip_merged_cells('td')

    def handle_colspan(self, attrs):
        rowspan = colspan = None

        for name, value in attrs:
            rowspan = int(value) if name == 'rowspan' else rowspan
            colspan = int(value) if name == 'colspan' else colspan

        attrs = [(n,v) for n,v in attrs if n not in ["colspan", "rowspan"]]

        if rowspan:
            colspan = colspan or 1
        if colspan:
            rowspan = rowspan or 1

        if rowspan or colspan:
            for row in range(0, rowspan):
                for col in range(0, colspan):
                    self.merged_cells[(self.row + row, self.col + col)] = attrs

            del self.merged_cells[(self.row, self.col)]

        return attrs

    def skip_merged_cells(self, tag):
        attrs = []
        while attrs is not None:
            attrs = self.merged_cells.pop((self.row, self.col), None)

            if attrs is not None:
                self.write_starttag(tag, attrs)
                self.write_endtag(tag)

                self.col += 1

    def handle_entityref(self, name):
        self.write(name)

    def handle_charref(self, name):
        self.write(name)

    def handle_data(self, data):
        if data.strip():
            indent = self.indent()

            text = textwrap.fill(
                data,
                width=95,
                expand_tabs=True,
                replace_whitespace=False,
                drop_whitespace=False,
                initial_indent=indent,
                subsequent_indent=indent,
                fix_sentence_endings=False,
                break_long_words=False,
                break_on_hyphens=False,
            )

            self.write_data(text)

    def handle_endtag(self, tag):
        if tag in ['figure', 'p', 'mark', 'u', 'underline', 'b', 'strong', 'i', 'em', 's', 'strike']:
            return

        self.level -= 1

        if tag == 'tr':
            # Handle colspans followed immediately by </tr>.
            self.skip_merged_cells(tag)

            self.write_endtag(tag)

            self.row += 1
            self.col = 0

        elif tag in ['td', 'th']:
            self.write_endtag(tag)

            self.col += 1

            self.skip_merged_cells(tag)

        else:
            self.write_endtag(tag)

    # Write methods

    def write_starttag(self, tag, attrs):
        self.write(self.indent())
        self.write(f"<{tag}")

        if tag in ['th', 'td']:
            attrs = self.handle_colspan(attrs)

        if tag not in ['mark']:
            for name, value in attrs:
                self.write(f" {name}=\"{value}\"")

        self.write(">\n")

    def write_data(self, data):
        self.write(data)
        self.write("\n")

    def write_endtag(self, tag):
        self.write(self.indent())
        self.write(f"</{tag}>\n")

    def write(self, data):
        self.file.write(data)


def main(input, output):
    with open(input, 'rb') as f:
        html = f.read().decode('utf-8')

    with open(os.open(output, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o666), 'wb') as f:
        PrettyHTML(f).feed(html)


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1], sys.argv[2])

