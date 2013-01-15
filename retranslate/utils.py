#!/bin/env python
# encoding=utf-8

from __future__ import print_function

import polib
import sys, os
import re
import codecs

from models import String


U_LITERAL_RE = re.compile(r"u['\"](.*?)['\"]")
_RESULT = [None, None]
_LN = 1
_SEEN = {}


def crawl_folder(path):
    file_count = 0
    for folder, subfolders, files in os.walk('path'):
        for file_path in files:
            file_base, file_extension = os.path.splitext(file_path)
            if file_extension == 'py':
                file_count += 1
                extract_from_file(file_path)
    return file_count

def extract_from_file(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as fh:
        ln = 0
        for line in fh:
            for match in U_LITERAL_RE.finditer(line):
                handle_token(match, file_path, ln)
        ln += 1

def handle_token(match, file_path, line):
    try:
        string_obj = String.objects.get(original=match.group())
    except String.DoesNotExist:
        location = ':'.join([line, match.start()])
        string_obj = String(file=file_path, location=location, original=match.group(),
            context=match.string)
        string_obj.save()

def string_replace(matchobj):
    original = matchobj.group(1)
    if original in _SEEN:
        return _SEEN[original]
    print(u'{}: {}'.format(_LN, matchobj.string.rstrip()))
    substitute = raw_input('{}\n--> '.format(original.encode('utf-8')))
    if not substitute:
        return '\'{}\''.format(original)
    _RESULT[:] = substitute, original
    _SEEN[original] = "_('{}')".format(substitute)
    return _SEEN[original]

if __name__ == '__main__':
    file_path = sys.argv[1]
    file_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    trans_file_path = os.path.join(file_dir, 'trans.{}'.format(file_name))
    po_file_name = '{}/locale/ru/LC_MESSAGES/django.po'.format(file_dir)
    try:
        with open(po_file_name) as f:
            pass
    except IOError as e:
        raise e
        exit()
    pofile = polib.pofile(po_file_name, check_for_duplicates=True)

    if os.path.isfile(trans_file_path):
        start_from = os.path.getsize(trans_file_path)
    else:
        start_from = 0
    with codecs.open(trans_file_path, 'a', 'utf-8') as out:
        _LN = 1
        fh_source = codecs.open(file_path, 'r', 'utf-8')
        fh_source.seek(start_from)
        for line in fh_source:
            try:
                repl = U_LITERAL_RE.sub(string_replace, line)
                if repl != line:
                    entry = polib.POEntry(
                        msgid=_RESULT[0],
                        msgstr=_RESULT[1],
                        occurrences=[(file_name, str(_LN))]
                    )
                    try:
                        pofile.append(entry)
                    except ValueError:
                        pass
                out.write(repl)
                _LN += 1
            except (EOFError, KeyboardInterrupt):
                print('\n-- Aborted --')
                out.flush()
                break
    pofile.save('{}/locale/ru/LC_MESSAGES/django.po'.format(file_dir))