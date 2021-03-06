#!/usr/bin/env python

import os, time, sys, re, inspect
import pdfMaker
import argparse
import urllib.request

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


"""
sample url = 
http://kissmanga.com/Manga/Sensei-Lock-On
http://kissmanga.com/Manga/Dragon-Ball
"""
class ClassName(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg
        

class  DriverX(object):
    """docstring for  driverX"""
    def __init__(self):
        super(DriverX, self).__init__()
        self.driver = init_driver()

    def __enter__(self):
        return self.driver

    def __exit__(self, type, value, traceback):
        pass    


def init_driver():
    """
    Returns a driver object.
    """

    # Setting the user agent to a human browser
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53")
    
    chrome_init = inspect.getfullargspec(webdriver.Chrome)

    if 'options' in chrome_init.args:
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Chrome(chrome_options=options)

    return driver


def get_title_and_chapter_links(driver, url_to_series):
    """
    Supply the main page of the manga and get the title, and list of URLs
    of the chapters available
    """
    driver.get(url_to_series)

    try:
        title_tag = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"bigChar")))
        title_text = title_tag.text
    except TimeoutException:
        print("Exception Occured:    TimeoutException")
        sys.exit("Couldn't get title!")

    list_of_a_tags = driver.find_elements_by_xpath("//tbody/tr/td/a")

    # Reversing to get ascending list,
    # since it is originally in descending order
    list_of_a_tags = list_of_a_tags[::-1]

    list_of_href = []
    for a_tag in list_of_a_tags:
        list_of_href.append(a_tag.get_attribute('href'))

    return title_text, list_of_href


def download_pages_of_one_chapter(driver, url_to_chapter, delay=0):
    """
    Goes through the chapter and downloads each page it encounters
    """

    # Going to first page
    driver.get(url_to_chapter)

    try:
        drop_down_list = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID,"selectReadType")))
    except TimeoutException:
        print("Exception Occured:    TimeoutException")
        sys.exit("Couldn't load chapter!")
 
    select = Select(drop_down_list)

    # Selecting the 'All Pages' option
    select.select_by_value('1')

    list_of_page_img = driver.find_elements_by_xpath('//div[@id="divImage"]/p/img')

    # Get all chapter image locations
    img_urls = []
    for page_img in list_of_page_img:
        img_urls.append(page_img.get_attribute("src"))

    # Find out chapter name
    chapter_name = url_to_chapter[url_to_chapter.rfind('/') + 1 : url_to_chapter.rfind('?')]

    # Unify format by parsing number out of chapter_name
    chapter_folder_name = "Chapter-" + re.findall('\d+', chapter_name)[0]

    # Create folder for chapter , if it not exist
    if not os.path.exists(chapter_folder_name):
        os.makedirs(chapter_folder_name)

    print("Chapter "+ chapter_name + " -> " + chapter_folder_name + os.path.sep)
    
    page_num = 1
    for img_url in img_urls:
        
        page_num_pad = str(page_num).zfill(3)
        filepath = os.path.join(chapter_folder_name, page_num_pad + ".jpg")

        # Current folder
        pwd = os.path.dirname(os.path.realpath(__file__))
        #Creating full file name
        fullfilename = os.path.join(pwd, filepath)
        
        if os.path.exists(fullfilename):
            print(" " + page_num_pad + "(exists)", end="")
        else:
            print(" " + page_num_pad, end="")
            try:
                req = urllib.request.Request(img_url, headers={'User-Agent' : "Magic Browser"})
                con = urllib.request.urlopen(req)
                with open(fullfilename, mode="wb") as d:
                    d.write(con.read())
                if delay > 0:
                    time.sleep(delay)
            except:
                # Skip, not available
                print("(ERROR)", end="")
            
        sys.stdout.flush()
        page_num += 1

    print()
    print()
    
    pass
    
def dequote(s):
    """
    If a string has single or double quotes around it, remove them.
    Make sure the pair of quotes match.
    If a matching pair of quotes is not found, return the string unchanged.
    """
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s

def process(driver):
    base_url = "https://kissmanga.com/Manga/"
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Batch-download chapters and series from Kissmanga")
    parser.add_argument('-o', '--output', type=str, help="Output folder path where the series folder will be created. Defaults to the current path from which this script is run")
    parser.add_argument('-u', '--url', required=True, type=str, help="Name of the series, no need to include the base kissmanga URL, so for 'https://kissmanga.com/Manga/Dragon-Ball' use'Dragon-Ball)")
    parser.add_argument('-i', '--ini', required=True, type=int, help="Initial chapter number to download, in [1..n]")
    parser.add_argument('-e', '--end', required=True, type=int, help="Final chapter number to download, included")
    parser.add_argument('--pdf', required=False, action='store_true', help="Generate a PDF file for each chapter")
    parser.add_argument('--pdf_series', required=False, action='store_true', help="Generate a huge PDF file with all chapters")
    parser.add_argument('--chapter_page', required=False, action='store_true', help="Render a chapter page and put it in front of the PDDF of each chapter")
    parser.add_argument('--delay', required=False, type=float, help="Add a delay (in seconds) between page downloads to avoid overloading the server")
    parser.add_argument('--ow', required=False, action='store_true', help="Overwrite existing PDF files")

    args = parser.parse_args()


    print("Initialising kissmanga-downloader")

    # Get main page of the series
    url = args.url if 'kissmanga.com' in dequote(args.url) else base_url + dequote(args.url)

    # Output folder
    output_folder = os.getcwd() if args.output is None else args.output
    
    # Delay between page downloads
    delay = 0 if args.delay is None or args.delay < 0 else args.delay
    if delay > 0:
        print("Using a delay of %.1f seconds" % delay)

    # Chapter page
    chapter_page = args.chapter_page

    # Create chapter PDFs?
    pdf = args.pdf

    # Create series PDF?
    pdf_series = args.pdf_series

    # Overwrite PDF files if they exist
    overwrite = args.ow

    # Fetch list of URLs
    print("Getting server URLs...", end="")
    title, list_of_hrefs = get_title_and_chapter_links(driver, url)
    print(" Done! (%d URLs)" % len(list_of_hrefs))

    # Series folder
    series_folder = os.path.join(output_folder, title)

    print("Preparing output folder: %s" % series_folder)
    # Create folder for the series, if it doesn't exist
    if not os.path.exists(series_folder):
        os.makedirs(series_folder)

    # Starting folder
    start_folder = os.getcwd()

    # Navigate inside the series folder
    os.chdir(series_folder)

    low_index = args.ini
    high_index = args.end

    if low_index < 1:
        print("--ini must be larger than 0: " + low_index)
        exit(0)

    if high_index < low_index:
        print("--end must be greater or equal than --ini: [%d <= %d]" % (low_index, high_index))
        exit(0)

    required_list = list_of_hrefs[low_index - 1: high_index]

    print("Starting chapter download: %d to %d\n" % (low_index, high_index))

    # Iterate over the list_of_hrefs for the requested chapters
    for href in required_list:
        # Download a chapter
        download_pages_of_one_chapter(driver, href, delay)

    print("%d chapters downloaded successfully" % (high_index - low_index + 1))
    driver.quit()

    print("Starting creatinon of PDF files: %d to %d\n" % (low_index, high_index))

    if pdf:
        # Active directory is inside the series folder:
        # Create the PDF, from the chapters inside
        mypath = os.getcwd()
        for root, dirs, files in os.walk(mypath):
            dirs.sort()
            for single_dir in dirs:
                pdfMaker.create_pdf(imageDirectory=single_dir,
                                    bool_page0=chapter_page,
                                    overwriteExisting=overwrite)


    if pdf_series:
        # Current folder has all the .pdf of the chapter folders
        pdfMaker.merge_pdfs(os.getcwd())

    # Go back to start_folder
    os.chdir(start_folder)

    print("Done!")
    

if __name__ == '__main__':
    with DriverX() as driver:
        process(driver)
