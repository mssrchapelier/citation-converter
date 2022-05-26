# citation-converter

## Scripts in this folder
* `build_citation_list.py`
* `convert_files.py`
* *`refobj.py` (auxiliary script)*

## What this does
These scripts convert in-text citations in an academic text from the **numeric** style (e. g. `[36]`) to the **author-date** style (e. g. `[Smith et al. 2015]`) and update the reference list accordingly.

The input consists of two files: 1) a file with the **text of the paper** itself, 2) a file that contains the **list of numbered references** cited in the text.
1. First, `build_citation_list.py` is run on the **references** to parse information about the authors and dates, which is written into an intermediary `.tsv` file (`citation-list.tsv` by default) that should be edited to correct any parsing errors.
2. After this, `convert_files.py` is run on the **text of the article**, which uses the edited `.tsv` file to create two new files — the text and the references — with numeric citations converted to author-date ones.

Example (the text and the references merged):

* source:

> Lorem ipsum dolor sit amet, consectetur adipisicing elit **[5]**. Modi, quod, dolorem molestiae...
>
> ...
>
> **[5]** Wondwossen Mulugeta, Michael Gasser, and Baye Yimam. Incremental learning of affix segmentation. In Proceedings ..., 2012.

* output:

> Lorem ipsum dolor sit amet, consectetur adipisicing elit **[Mulugeta et al. 2012]**. Modi, quod, dolorem molestiae...
>
> ...
>
> **Mulugeta et al. 2012** — Wondwossen Mulugeta, Michael Gasser, and Baye Yimam. Incremental learning of affix segmentation. In Proceedings ..., 2012.

## How to use
### 1. `build_citation_list.py`
Run `build_citation_list.py path_to_file_with_references`. This will create a `.tsv` file (`citation-list.tsv` by default) that you should edit manually to correct any parsing errors. Each line in the file corresponds to a single reference and contains three fields separated by tab characters:
* the citation number,
* the candidate author-date style citation which was parsed from the reference,
* the text of the reference itself.

Example:
* original file with references:

> [1] Jan A. Botha and Peter Blunsom. Adaptor Grammars for Learning Non-Concatenative Morphology. In Proceedings ..., 2013.
>
> [2] Tim Buckwalter. Buckwalter Arabic Morphological Analyzer Version 1.0. Linguistic Data Consortium ..., Philadelphia, 2002.
>
> [3] Sisay Fissaha and Johann Haller. Amharic verb lexicon in the context of machine translation. In Proceedings ..., 2003.

* running the script:
```
py build_citation_list.py examples/input/input-references.txt
Reading references from: examples/input/input-references.txt
Writing citation list to: ./citation-list.tsv
Completed!
IMPORTANT: Please manually edit the citation list: ./citation-list.tsv
```
* output:

> 1`\t\t`Jan A. Botha and Peter Blunsom. Adaptor Grammars for Learning Non-Concatenative Morphology. In Proceedings ..., 2013.
>
> 2`\t`Buckwalter 2002`\t`Tim Buckwalter. Buckwalter Arabic Morphological Analyzer Version 1.0. Linguistic Data Consortium ..., Philadelphia, 2002.
>
> 3`\t`Fissaha and Haller 2003`\t`Sisay Fissaha and Johann Haller. Amharic verb lexicon in the context of machine translation. In Proceedings ..., 2003.

(Here, you would need to add the author-date citation in the first line because the script could not parse this information.)

### 2. `convert_files.py`
After editing the `.tsv` file with citations, run `convert_files.py path_to_file_with_text`. This will convert the numeric citations to author-date citations and create two files (by default in the `output` folder):
1. the new text file (default: `text-new.txt`),
2. the new file with references (default: `references-new.txt`).

See example above in section ***What this does***.

## Regexps in `refobj.py`

`build_citation_list.py` uses the regular expressions specified in `refobj.py` in order to parse information about the author(s) and the date of publication from the reference. A great multitude of possible citation styles exist; the regexps used here were created to parse a specific file, so there are only three of them (for one; two; and three and more authors) in this file. You can add more by:
1. creating a new variable for the capturing pattern in the `patterns` section and adding that variable to the `PATTERNS` list;
2. doing the same for the replacement pattern in the `replacements` section (and adding the variable to the `REPLACEMENTS` list). 

## Full command-line syntax with all options:

### `build_citation_list.py`

`build_citation_list.py input_refs [--citation_tsv_output ...]`

Arguments:
* `input_refs`: the path to the original file with numbered references
* `--citation_tsv_output` *(optional)*: the path to the generated file with parsed author-date citations (default value: `citation-list.tsv`)

### `convert_files.py`

`convert_files.py input_text [--citation_tsv ...] [--output_text ...] [--output_references ...]`

Arguments:
* `input_text`: the path to the file with the original text
* `--citation_tsv` *(optional)*: the path to the .tsv file with parsed citations (default value: `citation-list.tsv`)
* `--output_text` *(optional)*: the path to the new file containing the converted text (default value: `./output/text-new.txt`)
* `--output_references` *(optional)*: the path to the new file containing the converted references (default value: `./output/references-new.txt`)
