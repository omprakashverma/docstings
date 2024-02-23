import os
import sys
sys.path.insert(0, os.path.abspath('../'))
add_module_names = False
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.intersphinx', 'sphinx.ext.todo', 'sphinx.ext.coverage', 'sphinx.ext.mathjax', 'sphinx.ext.ifconfig', 'sphinx.ext.viewcode', 'sphinx.ext.githubpages']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = 'En-en'
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = True
html_theme = 'sphinx_rtd_theme'
html_theme_options = {}
html_context = {'favicon': 'img/favicon.ico', 'logo': 'img/logo.jpg', 'theme_logo_only': True, 'display_github': True, 'github_user': 'flyingfrog81', 'github_repo': 'developer.skatelescope.org', 'github_version': 'master', 'conf_py_path': '/src/'}
latex_elements = {}
epub_exclude_files = ['search.html']