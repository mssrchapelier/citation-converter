# citation-converter

## Scripts in this folder
* `build_citation_list.py`
* `convert_files.py`
* *`refobj.py`, `unicode_chars.py` (auxiliary scripts)*

## What this does
These scripts convert in-text citations in an academic text from the **numeric** style (e. g. `[36]`) to the **author-date** style (e. g. `[Smith et al. 2015]`) and update the reference list accordingly.

The input consists of two files: 1) a file with the **text of the paper** itself, 2) a file that contains the **list of numbered references** cited in the text.
1. First, `build_citation_list.py` is run on the **references** to parse information about the authors and dates, which is written into an intermediary `.tsv` file (`citation-list.tsv` by default) that should be edited to correct any parsing errors.
2. After this, `convert_files.py` is run on the **text of the article**, which uses the edited `.tsv` file to create two new files — the text and the references — with numeric citations converted to author-date ones.

## Example

### Input

Using examples from `/examples`, let's suppose we have two files:

* `/examples/input/input-text.txt` with the source text of the paper:

>... крупнейшие неразмеченные включают корпус Walta Information Center – WIC (описан в **\[4\]**)... и корпус An Crúbadán **\[30\]** в 17 миллионов слов...

* `/examples/input/input-ref.txt` with the list of references:


>**\[4\]** Atelach Alemu Argaw and Lars Asker. An Amharic stemmer: Reducing words to their citation forms. In Proceedings of the Workshop on Computational Approaches to Semitic Languages: Common Issues and Resources – ACL 2007, pages 104—110, 2007.
>
>...
>
>**\[30\]** Kevin P. Scannell. The Crúbadán project: Corpus building for under-resourced languages. In C. Fairon, H. Naets, A. Kilgarriff, G.-M. de Schryver (Eds.), Building and Exploring Web Corpora: Proceedings of the 3rd Web as Corpus Workshop, volume 4, pages 5–15, 2007.


### Steps

1. `py build_citation_list.py examples/input/input-ref.txt`:

```
Reading references from: examples/input/input-ref.txt
Writing citation list to: ./citation-list.tsv
Completed!
IMPORTANT: Please manually edit the citation list: ./citation-list.tsv
```

2. Edit `citation-list.tsv` manually to correct any parsing errors:


>4`\t`**Argaw and Asker 2007**`\t`Atelach Alemu Argaw and Lars Asker. An Amharic stemmer..., pages 104—110, 2007.
>
> ...
>
>30`\t`**Scannell 2007**`\t`Kevin P. Scannell. The Crúbadán project..., pages 5–15, 2007.


3. `py convert_files.py examples/input/input-text.txt`:

```
Reading citation list from: citation-list.tsv
Converting citations in the text from: examples/input/input-text.txt
Writing the new reference file to: ./output/references-new.txt
Completed!
Converted text written to: ./output/text-new.txt
Converted references written to: ./output/text-new.txt
```

### Results

* `/output/text-new.txt`:

>... крупнейшие неразмеченные включают корпус Walta Information Center – WIC (описан в **[Argaw and Asker 2007]**)... и корпус An Crúbadán **[Scannell 2007]** в 17 миллионов слов...

* `/output/references-new.txt`:

>**Argaw and Asker 2007** — Atelach Alemu Argaw and Lars Asker. An Amharic stemmer: Reducing words to their citation forms. In Proceedings of the Workshop on Computational Approaches to Semitic Languages: Common Issues and Resources – ACL 2007, pages 104—110, 2007.
>
>...
>
>**Scannell 2007** — Kevin P. Scannell. The Crúbadán project: Corpus building for under-resourced languages. In C. Fairon, H. Naets, A. Kilgarriff, G.-M. de Schryver (Eds.), Building and Exploring Web Corpora: Proceedings of the 3rd Web as Corpus Workshop, volume 4, pages 5–15, 2007.

## Details on use

### `build_citation_list.py`
`build_citation_list.py path_to_file_with_references` creates a `.tsv` file (`citation-list.tsv` by default) that you should edit manually to correct any parsing errors. Each line in the file corresponds to a single reference and contains three fields separated by tab characters:
* the citation number,
* the candidate author-date style citation which was parsed from the reference,
* the text of the reference itself.

Full syntax:

`build_citation_list.py input_refs [--citation_tsv_output ...]`

Arguments:
* `input_refs`: the path to the original file with numbered references
* `--citation_tsv_output` *(optional)*: the path to the generated file with parsed author-date citations (default value: `citation-list.tsv`)

### `convert_files.py`
`convert_files.py path_to_file_with_text` converts the numeric citations to author-date citations and creates two files (by default in the `output` folder):
1. the new text file (default: `text-new.txt`),
2. the new file with references (default: `references-new.txt`).

Full syntax:

`convert_files.py input_text [--citation_tsv ...] [--output_text ...] [--output_references ...]`

Arguments:
* `input_text`: the path to the file with the original text
* `--citation_tsv` *(optional)*: the path to the .tsv file with parsed citations (default value: `citation-list.tsv`)
* `--output_text` *(optional)*: the path to the new file containing the converted text (default value: `./output/text-new.txt`)
* `--output_references` *(optional)*: the path to the new file containing the converted references (default value: `./output/references-new.txt`)

### Regexps in `refobj.py`

`build_citation_list.py` uses the regular expressions specified in `refobj.py` in order to parse information about the author(s) and the date of publication from the reference. A great multitude of possible citation styles exist; the regexps used here were created to parse a specific file, so there are only three of them (for one; two; and three and more authors) in this file. You can add more by:
1. creating a new variable for the capturing pattern in the `patterns` section and adding that variable to the `PATTERNS` list;
2. doing the same for the replacement pattern in the `replacements` section (and adding the variable to the `REPLACEMENTS` list).

This script loads Unicode uppercase and lowercase character codes from `unicode_chars.py` (`regex` from Python's standard library does not support Unicode categories, which the regexps in this script use).
