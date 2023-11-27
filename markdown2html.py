#!/usr/bin/python3
"""
Write a script markdown2html.py that takes an argument 2 strings:

First argument is the name of the Markdown file
Second argument is the output file name
"""
import sys
import os


def b(line):
    """This function returns bold and emphasis in the markdown"""
    line = line.strip()
    words = line.split()
    content = ''
    bold_status = False
    em_status = False

    for wd in words:
        if wd.startswith('**') and wd.endswith('**') or '**' in wd:
            re_wd = wd.replace('**', '<b>', 1).replace('**', '</b>', 1)
        else:
            if wd.startswith('**') and not bold_status:
                re_wd = wd.replace('**', '<b>', 1)
                bold_status = True
            elif wd.endswith('**') and bold_status:
                re_wd = wd.replace('**', '</b>', 1)
                bold_status = False
            else:
                re_wd = wd

        if re_wd.startswith('__') and re_wd.endswith('__'):
            re_wd = re_wd.replace('__', '<em>', 1).replace('__', '</em>', 1)
        else:
            if re_wd.startswith('__') and not em_status:
                re_wd = re_wd.replace('__', '<em>', 1)
                em_status = True
            elif re_wd.endswith('__') and em_status:
                re_wd = re_wd.replace('__', '</em>', 1)
                em_status = False

        content += re_wd + " "

    return content.strip()


def markdown(*args):
    """This function returns the markdown"""
    unordered_status = False
    ordered_status = False
    paragraph_status = False

    with open(args[0], 'r') as f:
        input_f = f.readlines()

    with open(args[1], 'w') as html_f:
        for index, line in enumerate(input_f):
            line = b(line)
            if line.startswith('#'):
                line_r = line.split()
                h_num = line_r[0].count('#')
                if h_num > 6:
                    html_f.write(line)
                word_bank = f'<h{h_num}>{line.strip("#").strip()}</h{h_num}>\n'
                html_f.write(word_bank)

            elif line.startswith('- '):
                if unordered_status is False:
                    html_f.write('<ul>\n')
                    unordered_status = True
                html_f.write(f'<li>{line[2:].strip()}</li>\n')
                if index + 1 == len(input_f) or not input_f[index + 1].startswith('- '):
                    html_f.write('</ul>\n')
                    unordered_status = False

            elif line.startswith('* '):
                if ordered_status is False:
                    html_f.write('<ol>\n')
                    ordered_status = True
                html_f.write(f'<li>{line[2:].strip()}</li>\n')
                if index + 1 == len(input_f) or not input_f[index + 1].startswith('* '):
                    html_f.write('</ol>\n')
                    ordered_status = False

            else:
                if line.isspace() is False:
                    if not paragraph_status:
                        html_f.write('<p>\n')
                        paragraph_status = True
                    html_f.write(f'\t{line}')

                    if index < len(input_f) - 1 and input_f[index + 1].strip() and \
                            not (input_f[index + 1].strip().startswith("#") or
                                 input_f[index + 1].strip().startswith("-") or
                                 input_f[index + 1].strip().startswith("*")):
                        html_f.write('<br>\n')
                    else:
                        html_f.write('</p>\n')
                        paragraph_status = False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        sys.stderr.write(f'Missing {sys.argv[1]}\n')
        sys.exit(1)

    markdown(sys.argv[1], sys.argv[2])

    sys.exit(0)