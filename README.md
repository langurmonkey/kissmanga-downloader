# kissmanga-downloader

Python script to batch-download images from [Kissmanga](https://kissmanga.com) and optionally convert them to PDF.
Forked from [Astrames/kissmanga-downloader](https://github.com/Astrames/kissmanga-downloader) and improved upon.

## Dependencies

You need Python 3.6+. Then, install the dependencies:

```bash
$  pip install -r requirements.txt
```

### Windows

Download chromedriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and put it somewhere in your path (probably the same folder where you cloned this repo would be best).

### Linux

Get chromium or chromedriver from your distro repository. For example:

```bash
$  # Ubuntu&co
$  apt install chromium-chromedriver
$  # Arch&co - On arch, chromedriver is provided by chromium
$  pacman -S chromium
```
At the end of the day, whatever distro you use make sure `chromedriver` is in your `$PATH`.

### macOS

No idea, just get and install chromedriver by whatever means you can.


## Usage

To use the script, you have to run the following command:

`python kissmanga-download.py`

and then pass the applicable arguments.

Linux/Mac users: The script has a shebang, so you may run it as `./kissmanga-downloader`

Here is the output of the `python kissmanga-download.py -h`:

```
usage: kissmanga-downloader.py [-h] [-o OUTPUT] -u URL -i INI -e END [--pdf]
                            [--pdf_series] [--chapter_page] [--delay DELAY]
                            [--ow]

Batch-download chapters and series from Kissmanga

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output folder path where the series folder will be
                        created. Defaults to the current path from which this
                        script is run
  -u URL, --url URL     Name of the series, no need to include the base
                        kissmanga URL, so for
                        'https://kissmanga.com/Manga/Dragon-Ball' use'Dragon-
                        Ball)
  -i INI, --ini INI     Initial chapter number to download, in [1..n]
  -e END, --end END     Final chapter number to download, included
  --pdf                 Generate a PDF file for each chapter
  --pdf_series          Generate a huge PDF file with all chapters
  --chapter_page        Render a chapter page and put it in front of the PDDF
                        of each chapter
  --delay DELAY         Add a delay (in seconds) between page downloads to
                        avoid overloading the server
  --ow                  Overwrite existing PDF files
```

For instance, to get the first 100 chapters of Dragon Ball, generating only chapter PDFs and adding a title page to each chapter, with `/output/folder/path` as the output folder:

```
python kissmanga-downloader.py -u Dragon-Ball -o /output/folder/path -i 1 -e 100 --pdf --chapter_page --ow
```


## Features

*  Download all images/pages of a chapter and tidily organise them into folders with sane names.
*  Optionally create PDF files for each chapter and a PDF for the entire series, for convenience.

## Future Features

* Archiving the chapters into individual `.zip`,`.cbr` or `.cbz` files, depending on the user.
* More websites.

