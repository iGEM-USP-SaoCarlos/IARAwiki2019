import requests
from iGEMconf import iGEM_url, TEMPLATES_DIR, PAGES_DIR


def fetch_pages_list():
    pass


def fetch_write(page_path, template=False):
    """ Takes a Path object and writes to it the iGEM page of same name.
    template=True means page is a template"""

    page_name = page_path.stem
    print(f'Fetching {["page", "template"][template]} "{page_name}"...', end='\r')

    url = iGEM_url(page_name, template)
    response = requests.get(url)

    if response:
        page_content = response.text

        with page_path.open('w') as page_file:
            page_file.write(page_content)

        print(f'Wrote "{page_name}" to file.'+' '*6)

    else:
        print(f'Failed to fetch URL "{url}".'+' '*9)


def main(DIR, template=False):
    for template_path in DIR.glob('*'):
        fetch_write(template_path, template)


if __name__ == '__main__':
    main(PAGES_DIR)
    main(TEMPLATES_DIR, True)
