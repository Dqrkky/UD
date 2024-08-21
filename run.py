import subprocess
import re
import sys
import tempfile
import os

def strip_whitespace(code):
    return '\n'.join(line.strip() for line in code.strip().splitlines())

def openProccesss(args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        print(f"{args[1].upper()} Error:", stderr.decode())
    string = stdout.decode()
    if string:
        if string[-1] == "\n":
            string = string[0:-1]
        return string

def execute_php(code):
    args = ['php', '-r', strip_whitespace(code)]
    return openProccesss(args)

def execute_python(code):
    args = ['python', '-c', strip_whitespace(code)]
    return openProccesss(args)

def execute_js(code):
    args = ['node', '-e', strip_whitespace(code)]
    return openProccesss(args)

def execute_java(code):
      with tempfile.TemporaryDirectory() as temp_dir:
          java_file_path = os.path.join(temp_dir, "Main.java")
          with open(java_file_path, 'w') as java_file:
              java_file.write((code))
          compile_process = subprocess.run(['javac', java_file_path], capture_output=True, text=True)
          if compile_process.returncode != 0:
              print(f"Compilation failed: {compile_process.stderr}")
              return
          args = ['java', '-cp', temp_dir, 'Main']
          return openProccesss(args)

def parse_mylang(script):
    php_code = re.findall(r'<php>(.*?)</php>', script, re.DOTALL)
    for code in php_code:
        print(f"PHP Output: {execute_php(code)}")
    python_code = re.findall(r'<python>(.*?)</python>', script, re.DOTALL)
    for code in python_code:
        print(f"Python Output: {execute_python(code)}")
    js_code = re.findall(r'<script>(.*?)</script>', script, re.DOTALL)
    for code in js_code:
        print(f"JavaScript Output: {execute_js(code)}")
    java_code = re.findall(r'<java>(.*?)</java>', script, re.DOTALL)
    for code in java_code:
        print(f"Java Output: {execute_java(code)}")

def main():
    with open(sys.argv[1], 'r') as file:
        script = file.read()
    parse_mylang(script)

if __name__ == "__main__":
    main()