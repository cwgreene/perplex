import subprocess
import argparse
import tempfile
import os

base_includes = ["stdio.h",
                 "sys/types.h",
                 "unistd.h",
                 "sys/socket.h",
                 "sys/stat.h",
                 "fcntl.h"]

def render_headers(includes):
    headers = []
    for include in includes:
        if include.startswith("/") or include.startswith("./") or include.startswith("../"):
            include = os.path.join(os.getcwd(), include)
            headers.append(f'#include "{include}"')
        else:
            headers.append(f'#include <{include}>')
    return "\n".join(headers)

def render_variables(variables):
    return "\n".join(f'printf("{variable}=%d\\n", {variable});' for variable in variables)
    
def process_body(body, start_line):
    with tempfile.NamedTemporaryFile() as temp:
        #print(body)
        temp.write(body.encode())
        temp.flush()
        result = subprocess.check_output(["gcc", "-x", "c", temp.name, "-o", f"{temp.name}.exe"], )
        result = subprocess.check_output([f"{temp.name}.exe"])
        print(result.decode(), end="")
        os.remove(f"{temp.name}.exe")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", dest="variables", action="append", default=[],
        help="specify a preprocessor variable")
    parser.add_argument("-i", dest="includes", action="append", default=[],
        help="include additional header. Use explicit relative paths for user includes.")
    options = parser.parse_args()

    if not options.variables:
        parser.print_help()
        return
    
    headers = base_includes[:]
    for i in options.includes:
        headers.append(i)
    body = render_headers(headers)
    start_line = len(headers) + 1

    variables = []
    for v in options.variables:
        variables.append(v)
    
    main_body = render_variables(variables)
    body += "\n" + "int main() {\n" + main_body + "\nreturn 0;\n}\n"
    process_body(body, start_line)

if __name__ == "main":
    main()
