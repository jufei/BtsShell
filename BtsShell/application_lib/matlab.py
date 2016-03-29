import re
from BtsShell import connections

def run_matlab_script(script_name):
    """This keyword runs Matlab script.
    
    | Input Parameters | Man. | Description |
    | script_name      | Yes  | Matlab script name |
    
    Example
    | Run Matlab Script | doa |
    """

    ret = connections.execute_shell_command_without_check('matlab -nodesktop -nosplash -r %s' % script_name)
    
def modify_matlab_script(script_template, datas, output_dir):
    """This keyword modifies Matlab script.

    | Input Parameters | Man. | Description |
    | script_template  | Yes  | Matlab script directory |
    | datas            | Yes  | Data needs to be modified |
    | output_dir       | Yes  | Output script directory |

    Example
    | Modify Matlab Script | |
    """
    try:
        template_file_handle = open(script_template, 'r')
    except:
        raise Exception, 'script template %s open failed' % script_template
    
    try:
        output_file_handle = open(output_dir, 'w')
    except:
        raise Exception, 'output file %s open failed' % output_dir
    
    try:
        lines = template_file_handle.readlines()
        for line in lines:
            for data in datas:
                (key, value) = data.split('=', 1)
                if re.match('^%s%s%s$' % ('%', key, '%'), line):
                    line = value + '\n'
            output_file_handle.write(line)
    finally:
        template_file_handle.close()
        output_file_handle.close()

if __name__ == '__main__':
    modify_matlab_script('d:\\liepixie\\desktop\\doa_1.m',
                         ["DATA=data=[1+j2, -3+j4];", "PRINT=print('-dpng', ['test.png']);"],
                         'd:\\liepixie\\desktop\\matlab.m')
            
