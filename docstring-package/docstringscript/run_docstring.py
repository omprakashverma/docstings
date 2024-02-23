# The provided Python code is a script that scans a directory containing Python files and
# adds docstrings to methods that don't already have them. It utilizes the OpenAI Codex API
# to generate the docstrings based on a given prompt.
import multiprocessing
import os
import ast
import sys
import time
from inspect import getsource

import requests

# Specify the directory path to scan
directory_path = sys.argv[1]

def get_multiple_inputs():
    input_list = []
    while True:
        user_input = input("Enter module name for sphinx documentation generation (or 'done' to finish): ")
        if user_input.lower() == 'done':
            break
        input_list.append(directory_path +'/'+ user_input)
    return input_list

# Get inputs from the user and store in a variable
folder_paths_list = get_multiple_inputs()

#folder_paths_list = ['library-management-system/Controllers', 'library-management-system/App']
rst_file_path = directory_path+ '/source/package/api.rst'  # Output .rst file


# To generate and add docstring to methods and classes

def get_openapi_doc(method_definition):
    openapi_url = "https://api.openai.com/v2/engines/davinci-codex/completions"
    prompt = f"Generate missing docstring for the following method:\n\n{method_definition}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY"  # Replace YOUR_API_KEY with your actual API key
    }

    data = {
        "prompt": prompt,
        "max_tokens": 150
    }

    response = requests.post(openapi_url, headers=headers, json=data)

    if response.status_code != 200:
        # docstring = response.json()["choices"][0]["text"]
        return f"""
        Some description for the method.

        :param property1: value1
        :param property2: value2
        :param property3: value3
        :return: return_value
        """
    else:
        return "Failed to generate docstring. Please check your request."


def get_openapi_doc_for_class(class_definition):
    openapi_url = "https://api.openai.com/v2/engines/davinci-codex/completions"
    prompt = f"Generate missing docstring for the following method:\n\n{class_definition}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY"  # Replace YOUR_API_KEY with your actual API key
    }

    data = {
        "prompt": prompt,
        "max_tokens": 150
    }

    response = requests.post(openapi_url, headers=headers, json=data)

    if response.status_code != 200:
        # docstring = response.json()["choices"][0]["text"]
        return f"""
        Some description for the class definition
        """
    else:
        return "Failed to generate docstring. Please check your request."


def update_file_with_docstrings(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    tree = ast.parse(content)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Get the method definition as a string
            start_lineno = node.lineno
            end_lineno = node.end_lineno
            method_lines = content.split('\n')[start_lineno - 1:end_lineno]
            method_definition = '\n'.join(method_lines)

            if not ast.get_docstring(node):
                # Preserve the existing structure by adding docstrings appropriately
                docstring = get_openapi_doc(method_definition)
                if docstring:
                    # Insert the docstring as the first element in the function body
                    node.body.insert(0, ast.Expr(ast.Constant(docstring)))
        if isinstance(node, ast.ClassDef):
            # Get the method definition as a string
            start_lineno = node.lineno
            end_lineno = node.end_lineno
            class_lines = content.split('\n')[start_lineno - 1:end_lineno]
            class_definition = '\n'.join(class_lines)

            if not ast.get_docstring(node):
                # Preserve the existing structure by adding docstrings appropriately
                docstring = get_openapi_doc_for_class(class_definition)
                if docstring:
                    # Insert the docstring as the first element in the function body
                    node.body.insert(0, ast.Expr(ast.Constant(docstring)))

    with open(file_path, 'w') as file:
        # Preserve the tree structure by using ast.unparse to write the AST back to the file
        file.write(ast.unparse(tree))


def scan_directory_for_adding_docstring(directory):
    s = time.time()
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                # threading.Thread(target=update_file_with_docstrings, args=(file_path,)).start()
                multiprocessing.Process(target=update_file_with_docstrings, args=(file_path,)).start()
    print(f'Added Docstring to {directory} ')


scan_directory_for_adding_docstring(directory_path)


# To generate API for Sphinx documentation


def generate_rst(folder_path, file_name):
    rst_content = f"........................................\n{file_name}\n........................................\n\n.. automodule:: {file_name}\n   :members:\n\n"
    return rst_content

from pathlib import Path

def find_immediate_folder(rootpath):
    path = Path(rootpath)
    if path.is_dir():
        folders = [p.name for p in path.iterdir() if p.is_dir()]
        return folders
    else:
        return False

def traverse_folders_for_sphinx_api(folder_paths, output_file,base_path):
    folder_path = os.path.dirname(output_file)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(output_file, 'a') as rst_file:

        for folder_path in folder_paths:
            for root, _, files in os.walk(folder_path):
                folder_name = os.path.basename(root)

                if root in folder_paths and folder_name != "__pycache__":
                    immediate_folders = find_immediate_folder(base_path)
                    if folder_name in immediate_folders:
                        rst_file.write(f"============================\n{folder_name}\n============================\n\n")
                for file in files:
                    if file.endswith('.py'):
                        file_name = os.path.splitext(file)[0]
                        if root in folder_paths and folder_name != "__pycache__":
                            rst_file.write(generate_rst(folder_name, f"{folder_name}.{file_name}"))
                for folder in os.listdir(root):
                    subfolder_path = os.path.join(root, folder)
                    if os.path.isdir(subfolder_path) and folder != "__pycache__":
                        rst_file.write(
                            f"============================\n{folder_name}.{folder}\n============================\n\n")
                        for sub_root, _, sub_files in os.walk(subfolder_path):
                            for sub_file in sub_files:
                                if sub_file.endswith('.py'):
                                    sub_file_name = os.path.splitext(sub_file)[0]
                                    if root in folder_paths and folder_name != "__pycache__":
                                        rst_file.write(generate_rst(f"{folder_name}.{folder}",
                                                                f"{folder_name}.{folder}.{sub_file_name}"))
    print("Generated API for sphinx documentation")


traverse_folders_for_sphinx_api(folder_paths_list, rst_file_path,directory_path)

