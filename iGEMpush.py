from iGEMconf import TEMPLATES_DIR, PAGES_DIR, iGEM_url
from sys import argv
from requests import Session
from getpass import getpass
from pathlib import Path
import pickle
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
MATCH_INPUTS = re.compile(r'<input[^>]+value="([^"]*)"[^>]+name="([^"]+)"|<input[^>]+name="([^"]+)"[^>]+value="([^"]*)"')

# Sucessful login message
sucLogMsg = 'You have successfully logged into the iGEM web sites.'
loginUrl = "https://igem.org/Login2"

pardir = Path(__file__).parent
credentials_path = pardir/'.credentials.dict.pickle'


def getInputs(html):
    """ Return name:value pairs of input tags with both attributes."""
    ret = {}
    matches = re.findall(MATCH_INPUTS, html)

    for value1, name1, name2, value2 in matches:
        ret.update({name1: value1, name2: value2})

    del ret['']
    return ret


def getCredentials():
    if credentials_path.exists():
        with credentials_path.open('rb') as cf:
            return pickle.load(cf)

    else:
        credentials = {'username': input('Username: '),
                       'password': getpass(),
                       'Login': 'Login'}

        if input('Save to future sessions? (Y/n)') != 'n':
            with credentials_path.open('wb') as cf:
                pickle.dump(credentials, cf)

        return credentials


def authenticate(s):
    """ Log into iGEM server within session s. """

    print('Logging into iGEM...')
    loginResp = s.post(loginUrl, data=getCredentials())

    if sucLogMsg in loginResp.text:
        print(sucLogMsg)
    else:
        print('Login failed.')
        exit()


def upload(page_path, s, template=False):
    page_path = Path(page_path)
    page_name = page_path.stem
    print(f'Uploading page "{page_name}"...', end='\r')
    pageUrl = iGEM_url(page_name, template, action='submit')

    # Get page's hidden inputs
    pageText = s.get(pageUrl).text
    pageInputs = getInputs(pageText)

    del pageInputs['wpDiff']
    del pageInputs['wpPreview']

    # Read new content from file
    with page_path.open('r') as page_file:
        newContent = page_file.read()

    # Add new content to inputs
    pageInputs.update({'wpTextbox1': newContent})

    # Send form!
    s.post(pageUrl, pageInputs)
    print(f'Uploaded page "{page_name}".' + ' ' * 3)


def upload_dir(DIR, s, template=False):
    """ Upload files from DIR directory Path to iGEM server. template=True if
        all files in directory are templates."""

    for page_path in DIR.glob('*'):
        upload(page_path)


def upload_list(path_list, s, template=False):
    for p in path_list:
        upload(p, s, template)


def upload_argv(argv, s):
    # Drop script name
    argv = argv[1:]

    tflags_indexes = [i for i, p in enumerate(argv)
                      if p in ('--template', '-T')]

    template_indexes = [i+1 for i in tflags_indexes]
    template_paths = [argv[i] for i in template_indexes]
    page_paths = [p for i, p in enumerate(argv)
                  if i not in tflags_indexes + template_indexes]

    upload_list(template_paths, s, template=True)
    upload_list(page_paths, s)


def main():
    with Session() as s:

        # Log into iGEM
        authenticate(s)

        if '--help' in argv or '-h' in argv:
            print('Upload multiple files to the iGEM server. Usage:')
            print('iGEMpush.py [page file] -T [template file]')
            print('\n--template/-T\tFollowing file is template')
            print('--all\t\tUpload all files in pages an template folders.')
            print('--help/-h\tPrints this message and exits.')
            exit()

        # Upload pages
        elif '--all' in argv:
            upload_dir(TEMPLATES_DIR, s, True)
            upload_dir(PAGES_DIR, s)

        else:
            upload_argv(argv, s)


if __name__ == '__main__':
    main()
