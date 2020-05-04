# Test .py to generate C code based on a template

from pathlib import Path
import re
from shutil import copyfile

'''
    Replace occurrances of 'find_str' with 'repl_str' from file fin_name to fout_name.
    This is a simple replace, as opposed to the 'user' replace that retains user code (similar to CubeMX templates).    
'''
def replace_file_symbol_simple(fin_name, fout_name, find_str, repl_str):
    with open(fin_name, "rt") as fin:
        with open(fout_name, "wt") as fout:
            summary_str = '# Edit carefully. This is a generated file.\n# {0}\n# was used to generate this\n# {1}\n# where {2} became {3}\n\n\n'.format(
                template_file_str,
                new_file_str,
                template_symbol_str,
                new_symbol_str
            )
            fout.write(summary_str)
            #  https://stackoverflow.com/a/37585463/101252
            occurrances = 0

            for line in fin:
                # occurrances += line.count(find_str)
                # fout.write(line.replace(find_str, repl_str))
                (result, qty) = re.subn(find_str, repl_str, line)
                occurrances += qty
                fout.write(result)

            return occurrances

'''
def merge_file_excerpt( source_str, dest_str, symbol_str: str) => str :
    with open(source_str, "rt") as fin:
        # search for /* USER CODE BEGIN Includes */
        re_search_exp = '\/\* USER CODE BEGING .* \*\/'
        if 'blabla' in fin.read():
            print("true")
'''


'''
    Replace occurrances of 'find_str' with 'repl_str' from file fin_name to fout_name.
    This is a simple replace, as opposed to the 'user' replace that retains user code (similar to CubeMX templates).    
'''
def replace_file_symbol_user(fin_name, fout_name, find_str, repl_str):
    bak_name = str(Path(fout_name).with_suffix('.bak'))
    copyfile(fout_name, bak_name)
    with open(fin_name, "rt") as fin:
        with open(fout_name, "wt") as fout:
            summary_str = '# Edit carefully. This is a generated file.\n# {0}\n# was used to generate this\n# {1}\n# where {2} became {3}\n\n\n'.format(
                template_file_str,
                new_file_str,
                template_symbol_str,
                new_symbol_str
            )
            fout.write(summary_str)
            #  https://stackoverflow.com/a/37585463/101252
            occurrances = 0

            for line in fin:
                # occurrances += line.count(find_str)
                # fout.write(line.replace(find_str, repl_str))
                (result, qty) = re.subn(find_str, repl_str, line)
                occurrances += qty
                fout.write(result)

            return occurrances

if __name__ == "__main__":
    new_file_str = str(Path(__file__).with_suffix('.c'))
    template_file_str = str(Path(__file__).with_suffix('.c_template'))
    template_symbol_str = '<NAME>'
    new_symbol_str = "Elephant"

    occurances = replace_file_symbol_simple(template_file_str, new_file_str, template_symbol_str, new_symbol_str)
    assert (occurances > 0)
    print('{0} occurances'.format(occurances))



