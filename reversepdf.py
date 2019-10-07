#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PyPDF2
import sys

input_fn = sys.argv[1]
output_fn = sys.argv[2]



def reverse_pdf(input_fn, output_fn):
  pdf_file = open(input_fn, 'rb')
  pdf_reader = PyPDF2.PdfFileReader(pdf_file)
  pdf_writer = PyPDF2.PdfFileWriter()

  num_pages = pdf_reader.getNumPages()
  for page_num in reversed(range(num_pages)):
    page_n = pdf_reader.getPage(page_num)
    pdf_writer.addPage(page_n)

  pdf_output_file = open(output_fn, "wb")
  pdf_writer.write(pdf_output_file)
  pdf_output_file.close()
  
  pdf_file.close()

reverse_pdf(input_fn, output_fn)
