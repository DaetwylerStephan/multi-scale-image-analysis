# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import os
import sys

#sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../multiScaleAnalysis"))

# -- Project information -----------------------------------------------------

project = 'Self-driving, multi-scale image analysis'
copyright = '2024, Daetwyler Stephan'
author = 'Stephan Daetwyler, Felix Y. Zhou, Hanieh Mazloom-Farisbaf, Reto Fiolka'
release = '1.0'

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    'sphinx_rtd_theme'
]

def skip(app, what, name, obj, would_skip, options):
    if name == "__init__":
        return False
    return would_skip

def setup(app):
    app.connect("autodoc-skip-member", skip)

autosectionlabel_prefix_document = True

# Boolean indicating whether to scan all found documents for
# autosummary directives, and to generate stub pages for each
# (http://sphinx-doc.org/latest/ext/autosummary.html)
autosummary_generate = True

# Both the class’ and the __init__ method’s docstring are concatenated
# and inserted.
autoclass_content = "class"  # "both"

# inheritance_graph_attrs = {'rankdir': "TB",
#                           'clusterrank': 'local'}
# inheritance_node_attrs  = {'style': 'filled'}

# This value selects how automatically documented members are sorted
# (http://sphinx-doc.org/latest/ext/autodoc.html)
autodoc_member_order = "groupwise"

# This value is a list of autodoc directive flags that should be
# automatically applied to all autodoc
# directives. (http://sphinx-doc.org/latest/ext/autodoc.html)
autodoc_default_flags = [
    "members",
    "inherited-members",
    "show-inheritance",
]

autodoc_inherit_docstrings = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["./_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# If true, the current module name will be prepended to all
# description unit titles (such as .. function::).
add_module_names = True

# The default language to highlight source code
highlight_language = "python"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'setup.py', 'setup.cfg']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
#html_theme_options = {'sticky_navigation': True,}

html_logo = "./multi_scale_analysis_logo.jpg"

pygments_style = "sphinx"
