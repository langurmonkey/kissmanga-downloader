import os
from os.path import join, getsize
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica
import PIL
from PIL import ImageDraw
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth 
from PyPDF2 import PdfFileReader, PdfFileWriter


def get_width_height(imagePath):
	im = PIL.Image.open(imagePath)
	return im.width, im.height


def get_list_image_paths(imageDirectory):
	"""
	Returns a list of image paths present in the input directory
	"""
	mypath = imageDirectory

	list_full_names = []
	for root, dirs, files in os.walk(mypath):
		for single_file in files:
			if ".jpg" in single_file:
				full_path = join(root, single_file)
				# print(full_path)
				list_full_names.append(full_path)

		# print (root, "consumes", end=' ')
		# print(sum(getsize(join(root,name)) for name in files), end=' ')
		# print("bytes in", len(files), "non-directory files")
	# print(list_full_names)
	return list_full_names

def pixel_to_mm(pixel):
	"""Converts input pixel to mm"""
	return int(pixel * 0.26458333)

def pdf_from_images(imageDirectory, outputPDFName=None):
	"""
	Creates a single PDF from a folder full of images.
	"""
	WIDTH = HEIGHT = int( 500 )
	page0_size = (WIDTH, HEIGHT)

	if outputPDFName is None:
		namePDF = str(imageDirectory) + ".pdf"
	else:
		namePDF = outputPDFName

	c = canvas.Canvas(namePDF, page0_size)

	# Creating page 000
	white = (255, 255, 255, 255)
	black = (0, 0, 0, 255)

	page0 = PIL.Image.new('RGBA', page0_size, white)

	# Colored Rectangle
	im = ImageDraw.Draw(page0)
	whiteMargin = 20
	blackOutline = 3
	im.rectangle([whiteMargin, whiteMargin, WIDTH - whiteMargin, HEIGHT - whiteMargin], fill=black)
	im.rectangle([whiteMargin + blackOutline, whiteMargin + blackOutline,
	 WIDTH - (whiteMargin + blackOutline), HEIGHT - (whiteMargin + blackOutline)],
	 fill=white)

	im = ImageReader(page0)
	c.drawImage(im, 0 , 0)
	font_size = 37
	c.setFont("Helvetica", font_size)

	if True: # For clarity
		# METHOD 2
		# Not centred perfectly
		title = os.path.basename(imageDirectory)
		n = 12

		correct_title = []
		for i in range(0, len(title), n):
			correct_title.append(title[i:i+n])
		
		textObject = c.beginText( WIDTH/2 - WIDTH/4, HEIGHT/2 )
		
		for line in correct_title:
			textObject.textLine(line)
		c.drawText(textObject)
	c.showPage()

	"""
	# single page code
	page2_path = "E:\Vinay\Python\Web Driver\Chapter-001\\002.jpg"
	w, h = get_width_height(page2_path)

	c.setPageSize((w,h))
	c.drawImage(page2_path, 0, 0)
	c.showPage()
	"""
	for page_path in get_list_image_paths(imageDirectory):
		w, h = get_width_height(page_path)
		c.setPageSize((w,h))
		c.drawImage(page_path, 0, 0)
		c.showPage()


	c.save()




def create_test_pdf(title):
	# title = "Dragon Ball"
	WIDTH = int(pixel_to_mm(500) * mm)
	HEIGHT = int(pixel_to_mm(500) * mm)

	WIDTH = HEIGHT = int( 500 )

	page_size = ( WIDTH, HEIGHT)
	c = canvas.Canvas("test.pdf", page_size)

	w, h =page_size
	#print(w,h)

	# Creating image for first page
	page0 = PIL.Image.new('RGBA', (w, h), (255, 255, 255, 255))

	# Color bound rectangle
	im = ImageDraw.Draw(page0)
	black_r = im.rectangle([20, 20, w - 20, h - 20], fill=(0, 0, 0, 255))
	white_r = im.rectangle([20 + 3, 20 + 3, w - (20 + 3), h - (20 + 3)], fill=(255, 255, 255, 255))

	im = ImageReader(page0)
	
	c.drawImage(im, 0 , 0)



	font_size = 37
	c.setFont("Helvetica", font_size)

	# """
	# METHOD 2
	# Not centred perfectly
	line = title
	n = 12

	correct_title = []
	for i in range(0, len(title), n):
		correct_title.append(title[i:i+n])
	
	textObject = c.beginText( WIDTH/2 - WIDTH/4, HEIGHT/2 )
	
	for line in correct_title:
		textObject.textLine(line)
	c.drawText(textObject)
	# """

	"""
	# METHOD 1
	# Can't handle long names
	c.drawCentredString(w/2, h/2 - font_size/4, text=title)
	"""


	
	# c.drawString(x=0, y=0, text="Maaayybeee")
	# c.drawRightString(x=100, y=0, text="Nooo")

	c.showPage()

	page1_path = "E:\Vinay\Python\Web Driver\Chapter-001\\001.jpg"
	w, h = get_width_height(page1_path)

	c.setPageSize((w, h))
	c.drawImage(page1_path, 0, 0 )#, width=865, height=1300)#get_width_height(page1))
	c.showPage()

	page2_path = "E:\Vinay\Python\Web Driver\Chapter-001\\002.jpg"
	w, h = get_width_height(page2_path)

	c.setPageSize((w,h))
	c.drawImage(page2_path, 0, 0)
	c.showPage()

	c.save()


def merge_pdfs(folder_with_pdfs, outputPDFName=None):
	"""
	Merges the *.pdf files into one single .pdf file
	"""
	output = PdfFileWriter()

	if outputPDFName is None:
		outputPDFName = str(folder_with_pdfs) + ".pdf"
	
	mypath = folder_with_pdfs

	for root, dirs, files in os.walk(mypath):
		for single_file in files:
			if ".pdf" in single_file:
				pdfOne = PdfFileReader(open(  join(root,single_file) , "rb"))
				
				for pageIndex in range(0, pdfOne.getNumPages()):
					output.addPage(pdfOne.getPage(pageIndex))

				# output.addPage(pdfOne.getPage(0))

	outputStream = open( join(root, outputPDFName) , "wb")
	output.write(outputStream)
	outputStream.close()

if __name__ == '__main__':
	# Works
	# get_list_image_paths('Vol-001-Ch-000--Prologue')

	# Gives list of image file paths
	# get_list_image_paths("E:\Vinay\Python\Web Driver")

	
	"""
	for one_image in get_list_image_paths("E:\Vinay\Python\Web Driver\Chapter-001"):
		print(os.path.basename(one_image) ,get_width_height(one_image))
	"""
	# create_test_pdf("Dragon Ball Chapter-001")

	# Creates a single PDF from images
	# pdf_from_images("E:\Vinay\Python\Web Driver\Vol-001-Ch-000--Prologue")

	# Merges present *.pdf files into a single PDF
	# merge_pdfs("E:\Vinay\Python\Web Driver\Sensei Lock-On! Volume 1")