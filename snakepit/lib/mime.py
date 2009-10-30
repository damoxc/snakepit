import re
import os

KNOWN_MIME_TYPES = {
    'application/pdf':        ['pdf'],
    'application/postscript': ['ps'],
    'application/rtf':        ['rtf'],
    'application/x-aspx':     ['aspx'],
    'application/x-sh':       ['sh'],
    'application/x-csh':      ['csh'],
    'application/x-troff':    ['nroff', 'roff', 'troff'],
    'application/x-yaml':     ['yml', 'yaml'],
    'application/x-ms-msf':   ['pdb'],
    
    'application/rss+xml':    ['rss'],
    'application/xsl+xml':    ['xsl'],
    'application/xslt+xml':   ['xslt'],
    'text/html+mako':         ['mao', 'mako'],
    
    'image/x-icon':           ['ico'],
    'image/svg+xml':          ['svg'],
    
    'model/vrml':             ['vrml', 'wrl'],
    
    'text/css':               ['css'],
    'text/html':              ['html'],
    'text/plain':             ['txt', 'TXT', 'text', 'README', 'INSTALL',
                               'AUTHORS', 'COPYING', 'ChangeLog', 'RELEASE', 'ini'],
    'text/xml':               ['xml'],
    'text/x-batch':           ['bat'],
    'text/x-csrc':            ['c', 'xs'],
    'text/x-chdr':            ['h'],
    'text/x-c++src':          ['cc', 'CC', 'cpp', 'C'],
    'text/x-c++hdr':          ['hh', 'HH', 'hpp', 'H'],
    'text/x-config':          ['cf', 'conf'],
    'text/x-csharp':          ['cs'],
    'text/x-md-project':      ['mdp'],
    'text/x-md-solution':     ['mds'],
    'text/x-vs-project':      ['csproj'],
    'text/x-diff':            ['diff', 'patch'],
    'text/x-eiffel':          ['e'],
    'text/x-elisp':           ['el'],
    'text/x-fortran':         ['f'],
    'text/x-haskell':         ['hs'],
    'text/x-javascript':      ['js'],
    'text/x-objc':            ['m', 'mm'],
    'text/x-ocaml':           ['ml', 'mli'],
    'text/x-makefile':        ['make', 'mk',
                               'Makefile', 'makefile', 'GNUMakefile'],
    'text/x-pascal':          ['pas'],
    'text/x-perl':            ['pl', 'pm', 'PL', 'perl'],
    'text/x-php':             ['php', 'php3', 'php4'],
    'text/x-python':          ['py', 'python'],
    'text/x-pyrex':           ['pyx'],
    'text/x-ruby':            ['rb', 'ruby'],
    'text/x-scheme':          ['scm'],
    'text/x-sql':             ['sql'],
    'text/x-textile':         ['txtl', 'textile'],
    'text/x-vba':             ['vb', 'vba', 'bas', 'frm'],
    'text/x-verilog':         ['v', 'verilog'],
    'text/x-vhdl':            ['vhd'],
}

KNOWN_MIME_ICONS = {
    'archive.png':            [],
    'audio.png':              [],
    'binary.png':             [],
    'document.png':           ['application/pdf', 'application/postscript', 'application/rtf'],
    'empty.png':              [],
    'exec.png':               [],
    'font.png':               [],
    'image.png':              ['image/x-icon', 'image/svg+xml', 'image/gif', 'image/jpeg', 'image/png'],
    'text.png':               ['text/plain', 'text/x-diff'],
    'text-x-authors.png':     [],
    'text-x-changelog.png':   [],
    'text-x-copying.png':     [],
    'text-x-install.png':     [],
    'text-x-source.png':      ['application/x-sh','application/x-csh', 'text/x-csrc', 'text/x-chdr', 'text/x-c++src', 'text/x-c++hdr', 'text/x-csharp', 'text/x-makefile', 'text/x-pascal', 'text/x-perl', 'text/x-python', 'text/x-pyrex', 'text/x-ruby'],
    'unknown.png':            [],
    'www.png':                ['application/x-aspx', 'text/x-asp', 'text/x-aspx', 'text/css', 'text/html', 'text/x-php', 'text/x-javascript'],
    
    'application/x-troff':    'nroff',
    'application/x-yaml':     'yml',
    
    'application/rss+xml':    'rss',
    'application/xsl+xml':    'xsl',
    'application/xslt+xml':   'xslt',
    
    'model/vrml':             'vrml',
    'text/xml':               'xml',
    'text/x-eiffel':          'e',
    'text/x-elisp':           'el',
    'text/x-fortran':         'f',
    'text/x-haskell':         'hs',
    'text/x-objc':            'm',
    'text/x-ocaml':           'ml',
    'text/x-scheme':          'scm',
    'text/x-textile':         'txtl',
    'text/x-vbnet':           'vb',
    'text/x-vb6':             'bas',
    'text/x-verilog':         'v',
    'text/x-vhdl':            'vhd'
}

MIME_RENDERERS = {}

MIME_RENDERERS['text'] = [x for x in KNOWN_MIME_TYPES.keys() if x.startswith('text')]
MIME_RENDERERS['text'].append('application/x-aspx')
MIME_RENDERERS['text'].append('application/xsl+xml')
MIME_RENDERERS['text'].append('application/xslt+xml')
MIME_RENDERERS['text'].append('application/xml')
MIME_RENDERERS['text'].append('application/x-sh')
MIME_RENDERERS['text'].append('application/x-csh')
MIME_RENDERERS['none'] = ['application/x-msdos-program', 'application/x-ms-msf']


# extend the above with simple (text/x-<something>: <something>) mappings

for x in ['ada', 'asm', 'asp', 'aspx', 'awk', 'bash', 'idl', 'inf', 'java', 'ksh', 'lua',
          'm4', 'mail', 'psp', 'rfc', 'rst', 'sql', 'tcl', 'tex', 'zsh']:
    KNOWN_MIME_TYPES.setdefault('text/x-%s' % x, []).append(x)


MIME_MAP = {}
for t, exts in KNOWN_MIME_TYPES.items():
    MIME_MAP[t] = t
    for e in exts:
        MIME_MAP[e] = t
        
MIME_ICON_MAP = {}
for icon, types in KNOWN_MIME_ICONS.items():
    MIME_ICON_MAP[icon] = icon
    for type in types:
        MIME_ICON_MAP[type] = icon

# Simple builtin autodetection from the content using a regexp
MODE_RE = re.compile(
    r"#!.+?env (\w+)|"                       # look for shebang with env
    r"#!(?:[/\w.-_]+/)?(\w+)|"               # look for regular shebang
    r"-\*-\s*(?:mode:\s*)?([\w+-]+)\s*-\*-|" # look for Emacs' -*- mode -*-
    r"vim:.*?(?:syntax|filetype|ft)=(\w+)"   # look for VIM's syntax=<n>
    )
    
def get_mimetype(filename, content=None, mimeMap=MIME_MAP):
    """Guess the most probable MIME type of a file with the given name.

    `filename` is either a filename (the lookup will then use the suffix)
    or some arbitrary keyword.
    
    `content` is either a `str` or an `unicode` string.
    """
    suffix = os.path.splitext(filename)[1][1:]
    if len(suffix) == 0:
        suffix = os.path.basename(filename)
    if suffix in mimeMap:
        # 1) mimetype from the suffix, using the `mime_map`
        return mimeMap[suffix]
    else:
        mimetype = None
        try:
            import mimetypes
            # 2) mimetype from the suffix, using the `mimetypes` module
            mimetype = mimetypes.guess_type(filename)[0]
        except:
            pass
        if not mimetype and content:
            match = re.search(MODE_RE, content[:1000] + content[-1000:])
            if match:
                mode = match.group(1) or match.group(2) or match.group(4) or \
                    match.group(3).lower()
                if mode in mimeMap:
                    # 3) mimetype from the content, using the `MODE_RE`
                    return mimeMap[mode]
            else:
                if is_binary(content):
                    # 4) mimetype from the content, using`is_binary`
                    return 'application/octet-stream'
        return mimetype

def is_binary(data):
    if isinstance(data, str) and detect_unicode(data):
        return False
    return '\0' in data[:1000]

def detect_unicode(data):
    if data.startswith('\xff\xfe'):
        return 'utf-16-le'
    elif data.startswith('\xfe\xff'):
        return 'utf-16-be'
    elif data.startswith('\xef\xbb\xbf'):
        return 'utf-8'
    else:
        return None
    
def get_mime_icon(filename):
    mimetype = get_mimetype(filename)
    return get_mime_icon_by_name(mimetype)

def get_mime_icon_by_name(mimetype):
    if mimetype in MIME_ICON_MAP:
        return "/images/icons/16/mimetypes/" + MIME_ICON_MAP[mimetype]
    else:
        return "/images/icons/16/mimetypes/empty.png"

def get_renderer(mimetype):
    mimetype = str(mimetype)
    for renderer, types in MIME_RENDERERS.iteritems():
        if mimetype in types:
            return renderer
    if mimetype.startswith('text'):
        return 'text'
    return ''

def guess_renderer(filename, contents):
    mimetype = get_mimetype(filename, contents)
    return get_renderer(mimetype)

__all__ = [
    'get_mimetype', 'get_mime_icon', 'get_mime_icon_by_name',
    'get_renderer', 'guess_renderer'
]