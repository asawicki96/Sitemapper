# Sitemapper

A console tool designed to create **xml sitemap** containing all website's urls. Program uses Python **Requests** library to send HTTP requests and **BeautifulSoup 4** to find all hrefs in HTML code of each site, then it evokes crawl method recursively to find next urls. It also checks if an url wasn't visited before and if url is absolute or relative. Arguments are passed to application by means **Argparse** library.

Steps to run program:

- install pipenv,
- get the repo,
- cd into repo directory,
- run pipenv --python 3.8,
- run pipenv shell,
- run "pipenv install" command or install all dependencies mentioned in Pipfile manually in virtualenv,
- cd sitemapper,
- run python main.py --url [ website url ] --exclude [ excludes reqex pattern for example /example ]

Program allows to exclude any regex pattern or files from sitemap for example:

python main.py --url www.example.com --exclude ".gif" --exclude "/about"

will exclude all .gif urls containing ".gif" and "/about".

