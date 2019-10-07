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
  if 0 != (num_pages&3):
    pages.append(PyPDF2.pdf.PageObject.createBlankPage(width=width_max, height=height_max))
    pages.append(PyPDF2.pdf.PageObject.createBlankPage(width=width_max, height=height_max))
    pages.append(PyPDF2.pdf.PageObject.createBlankPage(width=width_max, height=height_max))
    num_pages = 4*int((num_pages+3)/4)

  num_pages_2in1 = int(num_pages/2)

  pages_2in1 = []
  for page_num in range(num_pages_2in1):
    page_n = PyPDF2.pdf.PageObject.createBlankPage(width=width_max, height=height_max*2)
    pages_2in1.append(page_n)

  for page_num in range(num_pages):
    sys.stderr.write("[info] merging page %s\n" % page_num)
    merge_target_group = page_num >> 2
    merge_target_subgroup = page_num & 3
    merge_target_page_num = 2 * merge_target_group + (merge_target_subgroup & 1)
    merge_target_pos = 1 - (merge_target_subgroup >> 1)
    pages_2in1[merge_target_page_num].mergeTranslatedPage(pages[page_num], 0, height_max * merge_target_pos)
  pages = None

  sys.stderr.write("[info] writing pdf\n")
  pdf_writer = PyPDF2.PdfFileWriter()
  for page_num in range(num_pages_2in1):
    pdf_writer.addPage(pages_2in1[page_num])
  pages_2in1 = None

  pdf_writer.removeLinks()
  pdf_output_file = open(output_fn, "wb")
  pdf_writer.write(pdf_output_file)
  pdf_output_file.close()
  
  pdf_file.close()