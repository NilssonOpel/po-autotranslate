#!/usr/bin/env python3
#
#----------------------------------------------------------------------

import argparse
import googletrans
import io
import json
import os
from   pathlib import Path
import polib
import sys
import textwrap
import time
import colorama


RED=colorama.Fore.RED
GREEN=colorama.Fore.GREEN
RST=colorama.Style.RESET_ALL

_my_name = os.path.basename(__file__)
_my_input_default = 'my_strings.po'
_my_output_default = 'auto_strings.po'
_my_json_error_default = 'translate_errors.json'

DESCRIPTION = """
You may need to install googletrans
>  pip install googletrans==4.0.0rc1

Opens the INFILE
and google-translates to the language selected
Replace all (-r), or just fill in the missing (-f), 'msgstr',
insert translations from TRANSFILE
and save to OUTFILE
"""
USAGE_EXAMPLE = f"""
Examples:
> ./{_my_name} -i test.po -l danish --replace -o test.da.po

In case you did not get them all, or already have most of them:
> ./{_my_name} -i test.da.po -l danish --fill -o test.da.po
"""

#-------------------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(_my_name,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(DESCRIPTION),
        epilog=textwrap.dedent(USAGE_EXAMPLE))
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--replace', action='store_true',
        help='replace all translations')
    group.add_argument('-f', '--fill', action='store_true',
        help='insert only the missing translations')

    add = parser.add_argument
    add('-q', '--quiet', action='store_true',
        help='be more quiet')
    add('-v', '--verbose', action='store_true',
        help='be more verbose')
    add('-l', '--language', metavar='LANGUAGE',
        help='select language')
    add('-i', '--input', metavar='INFILE',
        required=True,
        help='.po or .pot file for extraction')
    add('-o', '--output', metavar='OUTFILE',
        default=_my_output_default,
        help='output file (.po or .pot) with results')

    return parser.parse_args()


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def has_valid_text(the_string):
    if the_string.isspace():
        return False
    if len(the_string):
        return True
    return False

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def translate_gettext_file(file_name, language, options):
    '''
    Look for msgid's then translate their msgstr to language,
    note that these files are (expected to be) coded as UTF-8
    '''
    pofile = polib.pofile(file_name)

    translator = googletrans.Translator()

    available_languages = googletrans.LANGUAGES
    if not language in available_languages.values():
        print(f'Sorry, google do not speak {language}')
        print(f'but they know')
        for language in available_languages.values():
            print('  ' +language)
        return

    translations = 0
    fails = 0
    result = 'FAIL'
    for entry in pofile:
        source = entry.msgid
        if options.verbose:
            print(f'In: "{source}"')
        else:
            print('.', end="")
        if not source:
            continue
        if not has_valid_text(source):
            result = source
        else:
            if not options.replace:
                if has_valid_text(entry.msgstr):
                    result = entry.msgstr
                    if options.verbose:
                        print(f'Keeping: {result}\n')
                    continue
            retries = 5
            untranslated = True
            while retries:
                try:
                    proposal = translator.translate(source, src='english', dest=language)
                    result = proposal.text
                except:
                    retries -= 1
                    print(f'Exception, will try {retries} more after sleeping')
                    time.sleep(1)
                    result = ""
                else:
                    untranslated = False
                    translations += 1

                    retries = 0
            if options.verbose:
                print(f'Got: {result}\n')

            if untranslated:
                fails += 1
        entry.msgstr = result

    if not options.verbose:
        print()

    print(f'Did {translations} translations')
    if fails:
        print(f'Left {fails} translations empty, rerun with -f')
    else:
        print('Everything is translated')
    if translations:
        pofile.save(options.output)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def main(options):
    ret_val = 0
    # To be able to make debug-printout
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
    colorama.init()

    input_file_name = options.input
    if not os.path.exists(input_file_name):
        print(RED)
        print(f'{options.input}, from the -i option, does not exist - giving up')
        print(RST)
        exit(3)

    translate_gettext_file(input_file_name, options.language, options)
    return ret_val

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    sys.exit(main(parse_arguments()))
