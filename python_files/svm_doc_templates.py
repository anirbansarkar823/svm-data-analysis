""" file: svm_doc_gen.py
A python script to convert the SVM data files (csv), to latex documents.


The program will read accept as arguments the input csv file, output file latex
file name. The program assumes that the data is properly formatted for the
operation.
"""


LATEX_DOC_HEAD = '''\\documentclass[oneside,twocolumn]{{article}}
\\usepackage{{mathtools}}

%% ADD PACKAGES %%

\\title{{Attributes tagging for {asset}}}
\\author{{Kipa Tachak}}
\\date{{{date}}}

\\setcounter{{secnumdepth}}{{3}}
\\newcommand{{\\tsub}}[2]{{\\text{{#1}}_{{\\text{{#2}}}}}}
\\newcommand{{\\tsubb}}[2]{{#1_{{\\text{{#2}}}}}}
\\newcommand{{\\dsub}}[2]{{\\dfrac{{\\text{{#1}}}}{{\\text{{#2}}}}}}
\\newcommand{{\\multsel}}[1]
{{
	\\[
		\\tsub{{Score}}{{#1}} = \\dsub{{Sum of selected}}{{Sum of ranks}}
	\\]
}}
\\newcommand{{\\singsel}}[1]
{{
	\\[
		\\tsub{{Score}}{{#1}} = \\dsub{{Rank of selected}}{{Max. rank}}.
	\\]
}}
\\newenvironment{{ttable}}
{{
\\begin{{center}}
\\begin{{tabular}}{{c|c}}
\\hline
}}
{{
\\\\ \\hline
\\end{{tabular}}
\\end{{center}}
}}

\\begin{{document}}
\\maketitle

%% BODY %%
\\section{{About the document}}
This file documents the process of asset tagging for the asset '{asset}' in the
vertical '{vertical}'.

{doc_body}

\end{{document}}
'''

LATEX_UNORDERED_LIST = '''\\begin{{itemize}}
{items}
\\end{{itemize}}
'''

LATEX_ORDERED_LIST = '''\\begin{{enumerate}}
{items}
\\end{{enumerate}}
'''

LATEX_TABLE_SINGLE_SEL = '''\\begin{{ttable}}
{header} \\hline
{items}
\\hline
Max. rank & {maxrank}
\\end{{ttable}}
'''

LATEX_TABLE_MULTI_SEL = '''\\begin{{ttable}}
{headers} \\hline
{items}
\\hline
Sum of ranks & {sumrank}
\\end{{ttable}}
'''

LATEX_SECTION = '''\\section{{{secname}}}
{secbody}
'''

LATEX_SECTION_ATTR_QUES = '''\\section{{Attributes and questions}}
The list of sections, variables, and questions are:
    \\begin{{itemize}}
    \\item Observation
    \\item General
    \\item Asset Specific
    {var_list}
    \\end{{itemize}}'''

LATEX_SECTION_OVERALL_SCOR = '''\\section{Overall scoring}
The overall scoring of the asset is given as,
\\begin{align*}
	\\tsub{Score}{asset} &= \\tsubb{W}{observation} \\times \\tsub{Score}{observation} \\\\
	&+ \\tsubb{W}{general} \\times \\tsub{Score}{general} \\\\
	&+ \\tsubb{W}{specific} \\times \\tsub{Score}{specific}.
\\end{align*}

The score of a section or a variable is given as,
\\[
	\\tsub{Score}{var} = \\sum_{l \in P} \\tsubb{W}{l} \\times \\tsub{Score}{l}.
\\]
where,
\\[
	P = \\text{Set of sub-parameter labels.}
\\]'''

LATEX_SECTION_ATTR_SCOR_PROC = '''\\section{{Attribute scoring and the
process}}
\\subsection{{Asset Specific}}
{var_analysis}'''

LATEX_SUB_SUB_SECTION = '''\\subsubsection{{{subsubsecname}}}
'''

LATEX_PARAGRAPH = '''\\paragraph{{{par_name}}}
'''

LATEX_ALPA_NUM = '''The score is given as,
\\begin{{align*}}
\\tsub{{Score}}{{{par}}} &= 1, \\tsubb{{N}}{{{par}}} \\ge \\text{{Threshold}} \\\\
        &=
\\Big(\\dfrac{{\\tsubb{{N}}{{{par}}}}}{{\\text{{Threshold}}}}\\Big)^{{2}}
\\text{{Otherwise}}.
\\end{{align*}}'''

LATEX_BINARY = '''The score is given as,
\\begin{{align*}}
\\tsub{{Score}}{{{par}}} &= 0, \\text{{If no}} \\\\
        &= 1, \\text{{If yes}}.
\\end{{align*}}'''


LATEX_MULTIPLE = '''The options given are,
\\begin{{ttable}}
Options & Rank \\\\ \\hline
{items}
\\end{{ttable}}
The score is given as,
{eqn}'''

LATEX_PAR_PARTS = {
    'Text Box': {
        'Text-Number': LATEX_ALPA_NUM,
        'Text-Alphanumeric': 'Classified as variable for "Information and \
        clarity"',
    },
    'Binary': {
        'Single Select': LATEX_BINARY
    },
    'Multiple Choice': {
        'Single Select': LATEX_MULTIPLE,
        'Multiple Select': LATEX_MULTIPLE
    }
}

