"""
----- copyright notice -----
Copyright (c) 2022 mssrchapelier (Kirill Karpenko)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

----- description -----

Attempts to extract parenthetical in-text citations
from numbered references in the input file.
Outputs a .tsv file with number, citation and the original
reference for each line.
The output file is meant to be edited manually (it is likely
that not all of the lines have been parsed successfully).

Example:
- input:
    "[1] Tim Buckwalter. Buckwalter Arabic ..., 2002."
- output:
    1[\t]Buckwalter 2002[\t]Tim Buckwalter. Buckwalter Arabic..., 2002.
"""

import argparse, os
from refobj import RefObj

def read_references(input_path):
    with open(input_path, "r", encoding="utf8") as fin:
        return [RefObj(line) for line in fin.readlines()]

def write_to_citation_list(refobjs, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf8") as fout:
        for refobj in refobjs:
            fout.write("\t".join([refobj.number,
                                  refobj.intext,
                                  refobj.reference]) + "\n")

def main(args):
    print("Reading references from: {}".format(args.input_refs))
    refobjs = read_references(args.input_refs)
    
    print("Writing citation list to: {}".format(args.citation_tsv_output))
    write_to_citation_list(refobjs, args.citation_tsv_output)
    
    print(("Completed!\n"
           "IMPORTANT: Please manually "
           "edit the citation list: {}").format(args.citation_tsv_output))

if __name__ == "__main__":
    # --- parse command line arguments ---
    parser = argparse.ArgumentParser()
    parser.add_argument("input_refs",
                        help=("the path to the original file that"
                              "contains the references"))
    parser.add_argument("--citation_tsv_output",
                        help=("the output path for the .tsv file with"
                              "citations and references"),
                        default="./citation-list.tsv")
    args = parser.parse_args()
    
    main(args)
