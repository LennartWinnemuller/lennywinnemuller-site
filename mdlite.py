"""Small Markdown and front-matter reader, so the Netlify build needs no extra packages."""
import html, re


def parse_front_matter(text):
    """Reads simple YAML front matter as written by Decap CMS (strings, dates, folded blocks)."""
    _, fm, body = text.split('---', 2)
    data, lines, i = {}, fm.strip('\n').split('\n'), 0
    while i < len(lines):
        line = lines[i]
        i += 1
        m = re.match(r'^([A-Za-z_][\w-]*):\s?(.*)$', line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in ('>', '>-', '|', '|-', '>+', '|+'):
            block = []
            while i < len(lines) and (lines[i].startswith(' ') or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            val = ('\n' if val.startswith('|') else ' ').join(block).strip()
        elif len(val) >= 2 and val[0] == val[-1] == "'":
            val = val[1:-1].replace("''", "'")
        elif len(val) >= 2 and val[0] == val[-1] == '"':
            val = val[1:-1].encode().decode('unicode_escape') if '\\' in val else val[1:-1]
        data[key] = val
    return data, body


def _inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', r'<img src="\2" alt="\1">', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'__(.+?)__', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    t = re.sub(r'(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])', r'<em>\1</em>', t)
    return t


def markdown(text):
    out, para, lst, quote = [], [], None, []

    def flush():
        nonlocal para, lst, quote
        if para:
            out.append('<p>' + _inline(' '.join(para)) + '</p>')
            para = []
        if lst:
            tag, items, start = lst
            attr = f' start="{start}"' if tag == 'ol' and start != 1 else ''
            out.append(f'<{tag}{attr}>' + ''.join(f'<li>{_inline(x)}</li>' for x in items) + f'</{tag}>')
            lst = None
        if quote:
            out.append('<blockquote><p>' + _inline(' '.join(quote)) + '</p></blockquote>')
            quote = []

    for raw in text.replace('\r\n', '\n').split('\n'):
        line = raw.rstrip()
        s = line.strip()
        if not s:
            # A blank line between list items keeps the list going (Decap writes loose lists).
            if not lst:
                flush()
            continue
        h = re.match(r'^(#{1,6})\s+(.*)$', s)
        ul = re.match(r'^[-*+]\s+(.*)$', s)
        ol = re.match(r'^(\d+)[.)]\s+(.*)$', s)
        if h:
            flush()
            n = len(h.group(1))
            out.append(f'<h{n}>{_inline(h.group(2).strip())}</h{n}>')
        elif ul or ol:
            tag = 'ul' if ul else 'ol'
            if para or quote or (lst and lst[0] != tag):
                flush()
            if not lst:
                lst = (tag, [], int(ol.group(1)) if ol else 1)
            lst[1].append(ul.group(1) if ul else ol.group(2))
        elif s.startswith('>'):
            if para or lst:
                flush()
            quote.append(s.lstrip('>').strip())
        elif lst and raw.startswith((' ', '\t')):
            lst[1][-1] += ' ' + s
        else:
            if lst or quote:
                flush()
            para.append(s)
    flush()
    return '\n'.join(out)
