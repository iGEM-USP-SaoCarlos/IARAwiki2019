from pathlib import Path
TEAM_NAME = 'USP_SaoCarlos-Brazil'
# if page, must append 'Team:', if template, 'Template'
URL_PREFIX = 'https://2019.igem.org/wiki/index.php?title='
TEMPLATES_DIR = Path('templates')
PAGES_DIR = Path('pages')


def iGEM_url(page_name, template=False, action='raw'):
    """ Generates iGEM URL of page named template_name. template says if it's a
    template. action is commonly 'raw' or 'submit'. """
    flag = ['Team:', 'Template:'][template]

    if page_name == 'main':
        page_name = ''
        slash = ''
    else:
        slash = '/'

    return URL_PREFIX + flag + TEAM_NAME + slash + page_name + '&action=' + action
