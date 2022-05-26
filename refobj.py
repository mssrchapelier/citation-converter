"""
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
"""

import re

# --- classes ---

class RefObj:

    def __init__(self, input_str = ""):
        """
        Example:
            input_str == "[1] Tim Buckwalter. Buckwalter Arabic..., 2002."
            self.number == "37"
            self.intext == "Buckwalter 2002"
            self.reference == "Tim Buckwalter. Buckwalter Arabic ..., 2002."
        """
        
        if input_str == "":
            self.number = ""
            self.intext = ""
            self.reference = ""
        else:
            # If the reference number could not be determined, self.number == "".
            self.number, self.reference = detach_number(input_str)
            # If the in-text citation could not be parsed, self.intext == "".
            self.intext = extract_intext(self.reference)
    
    def get_output(self):
        # "Buckwalter 2002 — Tim Buckwalter. Buckwalter Arabic ..., 2002."
        return "{} — {}".format(self.intext, self.reference)

# --- helper functions for RefObj --

def detach_number(s):
    """
    Attempts to detach the reference's number.
    Arguments:
        s - the original (numbered) reference
    Returns:
        ("number", "non_numbered_ref"); number is "" if it was not found
    Examples:
        s == "[1] Tim Buckwalter. Buckwalter Arabic ..., 2002."
        returns: ("1", "Tim Buckwalter. Buckwalter Arabic ..., 2002.")
        -------
        s == "Invalidly formatted string"
        returns: ("", "Invalidly formatted string")
    """
    refpair = dict()
    r = r"^\[(?P<num>\d+)\] (?P<non_numbered_ref>.+)$"
    p = re.compile(r)
    m = p.match(s)
    num = (m.group("num") if m else "")
    non_numbered_ref = (m.group("non_numbered_ref") if m else s)
    return (num, non_numbered_ref)

def extract_intext(non_numbered_ref):
    """
    Attempts to extract in-text citations from the reference.
    Arguments:
        non_numbered_ref - the reference (without its number)
    Returns:
        the in-text citation (empty if non_numbered_ref does not match any
        of the patterns in CAPT_INTEXT)
    Examples:
        non_numbered_ref == "Tim Buckwalter. Buckwalter Arabic ..., 2002."
        returns: "Buckwalter 2002"
    """
    for sub_pair in SUB_PAIRS:
        intext, num_subs = re.subn(sub_pair["pattern"],
                                   sub_pair["replacement"],
                                   non_numbered_ref)
        if num_subs > 0:
            return intext
    # if no replacements were made:
    return ""

# --- patterns ---

# does not match non-ASCII characters; need to enumerate them explicitly
# or use PyPi regex

PATTERN_ONE_AUTHOR = r"""(?x)
        ^
        (?:[A-Z][a-z]+[ ])          # name
        (?:[A-Z][a-z]+[ ])*?        # any other names (0 or more)
        (?P<surname>[A-Z][a-z]+)    # surname
        \.
        (?:.+?\,[ ])                # the rest of the citation until the year
        (?P<year>\d{4})             # year
        \.
        $
    """

PATTERN_TWO_AUTHORS = r"""(?x)
        ^
        # --- author 1 ---
        (?:[A-Z][a-z]+[ ])          # name
        (?:[A-Z][a-z]+[ ])*?        # any other names (0 or more)
        (?P<surname1>[A-Z][a-z]+)   # surname
        
        [ ]and[ ]
        
        # --- author 2 ---
        (?:[A-Z][a-z]+[ ])          # name
        (?:[A-Z][a-z]+[ ])*?        # any other names (0 or more)
        (?P<surname2>[A-Z][a-z]+)   # surname
        
        \.
        
        (?:.+?\,[ ])                # the rest of the citation until the year
        (?P<year>\d{4})             # year
        \.
        $
    """

PATTERN_MULTIPLE_AUTHORS = r"""(?x)
        ^
        # --- author 1 ---
        (?:[A-Z][a-z]+[ ])          # name
        (?:[A-Z][a-z]+[ ])*?        # any other names (0 or more)
        (?P<surname>[A-Z][a-z]+)    # surname
        
        # --- authors 2 to n-1 ---
        (?:
            ,[ ]
            (?:[A-Z][a-z]+[ ])+     # names (1 or more)
            (?:[A-Z][a-z]+)         # surname
        )+?
        
        ,[ ]and[ ]
        
        # --- author n ---
        (?:[A-Z][a-z]+[ ])+     # names (1 or more)
        (?:[A-Z][a-z]+)         # surname
        
        \.
        
        (?:.+?\,[ ])        # the rest of the citation until the year
        (?P<year>\d{4})     # year
        \.
        $
    """

PATTERNS = [PATTERN_ONE_AUTHOR, PATTERN_TWO_AUTHORS,
            PATTERN_MULTIPLE_AUTHORS]

# --- replacements ---

# "Smith 2002"
REPL_ONE_AUTHOR = r"\g<surname> \g<year>"

# "Smith and Doe 2015"
REPL_TWO_AUTHORS = r"\g<surname1> and \g<surname2> \g<year>"

# "Smith et al. 2022"
REPL_MULTIPLE_AUTHORS = r"\g<surname> et al. \g<year>"

REPLACEMENTS = [REPL_ONE_AUTHOR, REPL_TWO_AUTHORS, REPL_MULTIPLE_AUTHORS]

# --- precompiled regex objects ---
SUB_PAIRS = [{"pattern": re.compile(pat), "replacement": repl}
             for pat, repl in zip(PATTERNS, REPLACEMENTS)]
