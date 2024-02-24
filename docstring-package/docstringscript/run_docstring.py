# The provided Python code is a script that scans a directory containing Python files and
# adds docstrings to methods that don't already have them. It utilizes the OpenAI Codex API
# to generate the docstrings based on a given prompt.
import multiprocessing
import os
import ast
import sys
import time
from inspect import getsource
from typing import Literal

import requests
from llama_index.llms import OpenAI, ChatMessage, LLMMetadata

model="gpt-4-turbo"

### Enter your Credentials
semicolons_gateway_api_key = "sk-PKh0KGK8XEYngx19_Zmipg" # Insert the provided API key
semicolons_gateway_base_url = "https://4veynppxjm.us-east-1.awsapprunner.com"


# Specify the directory path to scan
directory_path = sys.argv[1]
def get_multiple_inputs():
    user_input = input("Enter module name for sphinx documentation generation with comma separated values: ")
    splited_value = user_input.split(",")
    result_list = [directory_path +'/'+ user_input for user_input in splited_value]
    return result_list

# Get inputs from the user and store in a variable
folder_paths_list = get_multiple_inputs()

#folder_paths_list = ['library-management-system/Controllers', 'library-management-system/App']
rst_file_path = directory_path+ '/source/package/api.rst'  # Output .rst file



def get_llm_object_for_train_data():


    llm = OpenAI(
        model=model,
        api_key=semicolons_gateway_api_key,
        api_base=semicolons_gateway_base_url,
        # api_base represents the endpoint the Llama-Index object will make a call to when invoked
        temperature=0.1
    )

    # Adjust the below parameters as per the model you've chosen
    llm.__class__.metadata = LLMMetadata(
        context_window=4000,
        num_output=1000,
        is_chat_model=True,
        is_function_calling_model=False,
        model_name=model,
    )
    return llm

# To generate and add docstring to methods and classes
def genai_response_generator(string_definition:str,call_for=Literal["function_doc_string", "class_doc_string"]):
    function_doc_string_prompt = f'''
                    For a given function string return doc string in following manner:

                    ```
                    """def temp1(lenght:float,width:float)->list[float]  \n return [2*(lenght+width)] """

                    ```


                    This is the output strictly expected:
                    ```
                        """
                        Calculates the perimeter of a rectangle and returns it as a list with a single float element.


                        :param: lenght (float): The length of the rectangle.
                        :param: width (float) : The width of the rectangle.

                        return: list[float]: A list containing a single float value representing the perimeter of the rectangle.
                        """
                      ```

                       Similarly give me for (give me only doc string ignoring function code and no explanation):

                        {string_definition}

                '''

    class_doc_string_prompt = f'''
                For a given Class in string format 

                    ```
                    class Rectangle:

                        def __init__(self, length: float = None, width: float = None):
                            self.length = length
                            self.width = width

                        def set_dimensions(self, length: float, width: float):

                            self.length = length
                            self.width = width

                        def calculate_perimeter(self) -> float:

                            if self.length is None or self.width is None:
                                raise ValueError("Length and width must be set before calculating the perimeter.")
                            return 2 * (self.length + self.width)

                        def calculate_area(self) -> float:
                            """
                            Calculates the area of the rectangle and returns it as a float.

                            return: float: The area of the rectangle.
                            """
                            if self.length is None or self.width is None:
                                raise ValueError("Length and width must be set before calculating the area.")
                            return self.length * self.width

                    ```
                    I want only doc string to be generated strictly in this manner

                    ```
                       """
                        A class used to represent a Rectangle and perform calculations related to it.

                        Attributes:
                            length (float): The length of the rectangle. Defaults to None.
                            width (float): The width of the rectangle. Defaults to None.

                        Methods:
                            set_dimensions(length: float, width: float)
                                Sets the dimensions of the rectangle.

                            calculate_perimeter() -> float
                                Calculates the perimeter of the rectangle and returns it as a float.

                            calculate_area() -> float
                                Calculates the area of the rectangle and returns it as a float.
                        """
                    ```

                    Similarly give me only for below class:
                    {string_definition}
              '''
    llm_object = get_llm_object_for_train_data()
    prompt_response = llm_object.chat([ChatMessage(role="user",
                                            content=function_doc_string_prompt if call_for == "function_doc_string" else class_doc_string_prompt)])
    return prompt_response.message.content

def get_openapi_doc(method_definition):
    method_responce = genai_response_generator(string_definition=method_definition,call_for="function_doc_string")[3:-3]
    method_responce = method_responce[4:-4]

    return method_responce



def get_openapi_doc_for_class(class_definition):
    class_responce = genai_response_generator(string_definition=class_definition, call_for="class_doc_string")[3:-3]
    class_responce = class_responce[4:-4]
    return  class_responce


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
                    docstring = f'{docstring}'
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
                    docstring = f'{docstring}'
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

print('Path to access project documentation:', directory_path + '/build/index.html')

