#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import sys
import argparse

crop_width_rate = 1
crop_height_rate = 1

if __name__ == u'__main__':

  parser = argparse.ArgumentParser(add_help=True)
  group = parser.add_argument_group("global optional arguments")
  group.add_argument('input', action='store', help="input pdf")
  group.add_argument('output', action='store', help="output pdf")
  group.add_argument('-b', "--begin", dest="page_begin", action='store', type=int, default=1 ,help="beginning page. start with 1")
  group.add_argument('-e', "--end", dest="page_end", action='store', type=int, default=0, help="end page including. 0 means the last page")
  args = parser.parse_args()
  input_fn = args.input
  output_fn = args.output
  page_begin = args.page_begin
  page_end = args.page_end

  pdf_file = open(input_fn, 'rb')
  pdf_reader = PyPDF2.PdfFileReader(pdf_file)

  if page_end == 0:
    page_end = pdf_reader.getNumPages()

  num_pages = page_end - page_begin + 1
  width_max = 0
  height_max = 0
  pages = []
  sys.stderr.write("[info] reading pages\n")
  for page_num in range(page_begin-1, page_end):
    page_n_orig = pdf_reader.getPage(page_num)
    rotate = page_n_orig.get('/Rotate')
    mbox_n = page_n_orig.mediaBox
    width_n = float(page_n_orig.mediaBox.getWidth())
    height_n = float(page_n_orig.mediaBox.getHeight())
    page_n_tr = PyPDF2.pdf.PageObject.createBlankPage(width=width_n, height=height_n)
    page_n_tr.mergeTranslatedPage(page_n_orig, -mbox_n.getLowerLeft_x(), -mbox_n.getLowerLeft_y(), expand=False)
    page_n_rot = PyPDF2.pdf.PageObject.createBlankPage(width=0, height=0)
    if rotate:
      page_n_rot.mergeRotatedPage(page_n_tr, -rotate, expand=True)
    else:
      page_n_rot = page_n_tr
    page_n = page_n_rot

    mbox_n = page_n.mediaBox
    center_x = ( float(mbox_n.getLowerLeft_x()) + float(mbox_n.getUpperRight_x()) ) *0.5
    center_y = ( float(mbox_n.getUpperRight_y()) + float(mbox_n.getLowerLeft_y()) ) *0.5
    width_n = float(page_n.mediaBox.getWidth())
    height_n = float(page_n.mediaBox.getHeight())

    mbox_n.setLowerLeft((center_x - width_n * crop_width_rate * 0.5, center_y - height_n * crop_height_rate * 0.5))
    mbox_n.setUpperRight((center_x + width_n * crop_width_rate * 0.5, center_y + height_n * crop_height_rate * 0.5))
    page_n.mediaBox = mbox_n
    width_n = page_n.mediaBox.getWidth()
    height_n = page_n.mediaBox.getHeight()
    if width_max < width_n:
      width_max = width_n
    if height_max < height_n:
      height_max = height_n
    pages.append(page_n)

  if 0!=(num_pages&7):
    for i in range(7):
      pages.append(PyPDF2.pdf.PageObject.createBlankPage(width=width_max, height=height_max))
    num_pages = ((num_pages+7)>>3)<<3

  num_pages_8in1 = num_pages>>3

  pdf_writer = PyPDF2.PdfFileWriter()

  pages_8in1 = []
  for page_num_8in1 in range(num_pages_8in1):
    pages_8in1.append(PyPDF2.pdf.PageObject.createBlankPage(width=width_max*4, height=height_max*2))

  for page_num in range(num_pages):
    page_num_8in1 = page_num>>3
    pos_num = page_num&7
    nx = pos_num>>1
    ny = 1-(pos_num&1)
    sys.stderr.write("[info] merging page %s\n" % page_num)
    pages_8in1[page_num_8in1].mergeTranslatedPage(pages[page_num], width_max*nx, height_max*ny)

  sys.stderr.write("[info] writing pdf\n")
  for page_num_8in1 in range(num_pages_8in1):
    pdf_writer.addPage(pages_8in1[page_num_8in1])

  pdf_output_file = open(output_fn, "wb")
  pdf_writer.write(pdf_output_file)
  pdf_output_file.close()

  pdf_file.close()