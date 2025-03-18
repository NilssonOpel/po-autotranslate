# po-autotranslate
Translate .po file using googletrans

You may need to install googletrans 4.0.0rc1, e.g.
>  pip install googletrans==4.0.0rc1

and polib
>  pip install polib
~~~
usage: auto_translate.py [-h] [-r] [-q] [-v] [-l LANGUAGE] [-w WIDTH] -i INFILE [-o OUTFILE]

Opens the INFILE, assumed to be in 'english',
and google-translates to the language selected as --language
Replace all (-r), or just fill in the missing translations ('msgstr':s),
and save to OUTFILE

options:
  -h, --help            show this help message and exit
  -r, --replace         replace all translations (if using a .po file)
  -q, --quiet           be more quiet
  -v, --verbose         be more verbose
  -l LANGUAGE, --language LANGUAGE
                        select language
  -w WIDTH, --wrapwidth WIDTH
                        wrap column, 0 -> no wrap
  -i INFILE, --input INFILE
                        .po or .pot file for extraction
  -o OUTFILE, --output OUTFILE
                        output .po file with results

Examples:
> ./auto_translate.py -i input.pot -l danish -o output.da.po

> ./auto_translate.py -i input.po -l danish -o output.da.po --replace

In case you did not get them all, or already have most of them:
> ./auto_translate.py -i test.da.po -l danish -o test.da.po
~~~
