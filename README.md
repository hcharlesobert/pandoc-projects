# pandoc-projects

Consolidate a bunch of old DOCX and ODT files as Markdown.

## Initial import

Use `import-writings.py` to recursively export DOCX and ODT files to Markdown.

Initially, perform a dry run (without passing arguments):

```sh
python3 ../import-writings.py
```


If it looks good, pass `--convert` to export to Markdown:

```sh
python3 ../import-writings.py --convert
```
