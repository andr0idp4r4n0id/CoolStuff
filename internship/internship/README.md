# Internship Ramblings

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris vel lacus
interdum, congue arcu eget, blandit massa. Nunc justo orci, sodales tincidunt
tellus non, facilisis varius nisi.

## How to Use

You can render my ramblings, using [mkdocs] to build and serve a static
websiste. See how to do it below.

### Mkdocs

1. `git clone https://repo.char49.com/gogs/francisco/internship`
2. `cd internship`
3. `mkdocs serve`
4. Visit http://localhost:8000

### Docker

1. `git clone https://repo.char49.com/gogs/francisco/internship`
2. `cd internship`
3. `docker run --rm -it -v "${PWD}":/docs -p 8000:8000 squidfunk/mkdocs-material`
4. Visit http://localhost:8000

[mkdocs]: https://www.mkdocs.org/

