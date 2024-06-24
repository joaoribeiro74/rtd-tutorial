# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'rtd-tutorial'
copyright = '2024, João Vitor Ribeiro'
author = 'João Vitor Ribeiro'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import recommonmark
from recommonmark.transform import AutoStructify

extensions = [
    'recommonmark',
    'sphinx_markdown_tables',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

def setup(app):
    app.add_config_value('recommonmark_config', {
            'url_resolver': lambda url: github_doc_root + url,
            'auto_toc_tree_section': 'Contents',
        }, True)
    app.add_transform(AutoStructify)

templates_path = ['_templates']
exclude_patterns = []

language = 'pt'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
