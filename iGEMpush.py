from iGEMconf import TEMPLATES_DIR, PAGES_DIR, iGEM_url
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


def upload_dir(DIR, s, template=False):
    """ Upload files from DIR directory Path to iGEM server. template=True if
        all files in directory are templates."""

    for page_path in DIR.glob('*'):
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


def main():
    with Session() as s:

        # Log into iGEM
        authenticate(s)

        # Upload pages
        upload_dir(TEMPLATES_DIR, s, True)
        upload_dir(PAGES_DIR, s)


if __name__ == '__main__':
    main()
