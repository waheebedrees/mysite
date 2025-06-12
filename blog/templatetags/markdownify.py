import markdown
import os
from mistune import HTMLRenderer
from django import template
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from html import escape
import markdown as md
from django.template.defaultfilters import stringfilter
import re


class HighlightRenderer(HTMLRenderer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_was_heading = False
        self.in_section = False
        self.in_references = False  

    def heading(self, text, level):
        # Close previous section if needed
        output = ''
        if self.in_section:
            output += self.thematic_break()

        slug = text.lower().replace(" ", "-")
        self.last_was_heading = True
        self.in_section = True
        return output + f'''
        <h{level} id="{slug}" class="text-{level}xl font-bold scroll-mt-24">
          {text} :
        </h{level}>
        '''

    def paragraph(self, text, last=False):
        # Add bottom margin and padding to paragraph
        content = f'<p class="px-4  leading-7">{text}</p>'
        # If last paragraph in section, add a divider after it
        if last:
            content += '<hr class="border-t border-gray-600 my-6" />'
        return content

    def thematic_break(self):
        return '''
        <hr class="my-2 border-gray-300 section-divider"/>
        '''

    def render(self, blocks):
        content = super().render(blocks)
        # Add final divider if section was open
        if self.in_section:
            content += self.thematic_break()
        return content

    def inline_code(self, text):
     
        return f'<code class=" text-sm px-1 rounded text-pink-600">{escape(text)}</code>'

    def block_quote(self, text):
        return f'<blockquote class="border-l-4 border-blue-500 pl-4 italic mb-4">{text}</blockquote>'


    def references(self, text):
        return f'<div class="references">{text}</div>'

    def list(self, text, ordered, depth):
        # Track reference list state
        self.in_references = ordered and depth == 0
        if self.in_references:
            return f'<ol class="reference-list">{text}</ol>'
        
        tag = "ol" if ordered else "ul"
        indent_class = f"ml-{depth * 4}"
        list_style = "list-decimal" if ordered else "list-disc"
        return f'<{tag} class="{indent_class} {list_style} mb-4">{text}</{tag}>'

    def list_item(self, text):
        if self.in_references:
            return f'<li class="reference-item">{text}</li>'
        return f'<li class="text-sm leading-snug ">{text}</li>'

    def link(self, text, url, title=None):
        return f'<a href="{escape(url)}" class="citation-link" target="_blank" rel="noopener">{text}</a>'
    
    def table(self, text: str) -> str:
        return (
            '<div class="p-4 overflow-x-auto block">'
            '<table class="table-auto w-auto text-xs border border-gray-500 border-collapse">\n'
            + text +
            '</table></div>\n'
        )

    def table_head(self, text: str) -> str:
        return '<thead class=" text-left text-sm">\n' + text + '</thead>\n'

    def table_body(self, text: str) -> str:
        return '<tbody class="divide-y">\n' + text + '</tbody>\n'

    def table_row(self, content: str) -> str:
        return '<tr class="hover:bg-gray-800 transition-colors duration-150">' + content + '</tr>\n'

    def table_cell(self, content: str, align='center', head: bool = False) -> str:
        tag = 'th' if head else 'td'
        align_attr = f' align="{align}"' if align else ''
        classes = "border border-gray-600 px-1 py-0.5 text-xs text-center"
        return f'<{tag}{align_attr} class="{classes}">{content}</{tag}>'

    def image(self, alt: str, url: str, title: str = None) -> str:
        html = f'<img src="{escape(url)}" alt="{escape(alt)}"'
        title = "waheeb"
        if title:
            html += f' title="{escape(title)}"'
        html += ' class="my-4 rounded-lg shadow-lg" />'
        return f'''
        <div class="my-6 max-w-3xl mx-auto hover:scale-105 transition-transform duration-200">
          <img 
            src="{escape(url)}" 
            alt="{escape(alt)}" 
            class="rounded-lg shadow-lg w-full h-auto"
            {f'title="{escape(title)}"' if title else 'waheeb'}
          >
        </div>
        '''



register = template.Library()

@register.filter
@stringfilter
def markdown_func(value):
    renderer = HighlightRenderer()
    markdown = mistune.create_markdown(renderer=renderer, plugins=[
                                       "strikethrough", "footnotes", "table", "speedup"])
    return markdown(value)


@register.filter
@stringfilter
def render_markdown(value):
    return markdown.markdown(value, extensions=['fenced_code', 'nl2br', 'attr_list', 'tables'])


def remove_toc(contents):
    pattern = re.compile(
        r"(## Table of Contents.*?)(?=^##\s|\Z)", re.DOTALL | re.MULTILINE)
    match = pattern.search(contents)
    if match:
        toc_md = match.group(1).strip()
        body_md = contents.replace(toc_md, '', 1).lstrip()
        return toc_md, body_md
        
    else:
        toc = extract_toc(contents)
        list_item = ""
        for level, title in toc:
            indent = "  " * (level- 1)
            list_item += f"{indent} - [{title}](#{str(title).replace(' ', '-').lower()})\n"
        return list_item, contents


def parse_markdown(value):
    markdown = md.Markdown(
        extensions=['toc', 'codehilite', 'fenced_code', 'tables'])
    toc_md, body_md = remove_toc(value)
    html_toc = markdown.convert(toc_md) if toc_md else ''
    return html_toc, body_md


def extract_toc(markdown_text):
    toc = []
    for line in markdown_text.split('\n'):
        # Match headers (level 1 or 2)
        if re.match(r'^#+\s+', line):
            # Determine header level
            level = line.count('#', 0, line.find(' '))
            if level in (1, 2):  # Only include level 1 & 2 headers
                title = line.strip('# ').strip()
                toc.append((level, title))
    
    return toc
