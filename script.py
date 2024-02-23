import subprocess
import os
import shutil

destination_repo = input("Please enter the repository path: ")

# Install Sphinx 5.2.2 using pip
subprocess.run(["pip", "install", "Sphinx==5.2.2"])



# Source folder path
docs_source_folder = 'docstring-package/docs'

# Destination Python repository path
#destination_repo = 'library-management-system'

# Copy source folder to Python repository
shutil.copytree(docs_source_folder, destination_repo,dirs_exist_ok=True)

# Docstring script
docs_script_folder = 'docstring-package/docstringscript'
destination_dir = os.getcwd()

shutil.copytree(docs_script_folder, destination_dir ,dirs_exist_ok=True)



python_file_path = "run_docstring.py"

subprocess.run(["python", python_file_path])

# Change directory to the Python repository
os.chdir(destination_repo)

# Run Sphinx build command to generate documentation
subprocess.run(["sphinx-build", "-b", "html", "source", "build"])


