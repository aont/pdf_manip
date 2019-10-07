#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import sys

input_fn = sys.argv[1]
output_fn = sys.argv[2]

if __name__ == u'__main__':
  pdf_file = open(input_fn, 'rb')
  pdf_reader = PyPDF2.PdfFileReader(pdf_file)

  num_pages = pdf_reader.getNumPages()
  width_max = 0
  height_max = 0
  pages = []
  sys.stderr.write("[info] reading pages\n")
  for page_num in range(num_pages):
    page_n = pdf_reader.getPage(page_num)
    mbox_n = page_n.mediaBox
    width_n = float(mbox_n.getWidth())
    height_n = float(mbox_n.getHeight())
    if width_max < width_n:
      width_max = width_n
    if height_max < height_n:
      height_max = height_n
    pages.append(page_n)
  if 1==(num_pages&1):
    pages.append(PyPDF2.pdf.PageObject.createBlankPage(width=width_max, height=height_max))
    num_pages += 1

  pdf_writer = PyPDF2.PdfFileWriter()
  num_pages_sasshi = int(num_pages/2)

  for page_num in range(num_pages_sasshi):
    page_n = PyPDF2.pdf.PageObject.createBlankPage(width=width_max*2, height=height_max)
    page_num_fwd = page_num
    sys.stderr.write("[info] merging page %s\n" % page_num_fwd)
    page_fwd = pages[page_num_fwd]
    page_n.mergeTranslatedPage(page_fwd, (1-page_num&1)*width_max, 0)

    page_num_bwd = num_pages - 1 - page_num
    sys.stderr.write("[info] merging page %s\n" % page_num_bwd)
    page_bwd = pages[page_num_bwd]
    page_n.mergeTranslatedPage(page_bwd, (page_num&1)*width_max, 0)

    pdf_writer.addPage(page_n)

  pdf_writer.removeLinks()
  pdf_output_file = open(output_fn, "wb")
  pdf_writer.write(pdf_output_file)
  pdf_output_file.close()
  
  pdf_file.close()