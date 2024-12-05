import PyPDF2
import os

directory = '.'
rawWhitePapers = directory + "/rawWhitePapers"
txtWhitePapers = directory + "/txtWhitePapers"
for filename in os.listdir(rawWhitePapers):
    print(filename)
    if filename == ".DS_Store":
        pass
    else:
        pdffileobj = open(directory + "/rawWhitePapers" + "/" + filename, 'rb')
        # create reader variable that will read the pdffileobj
        pdfreader = PyPDF2.PdfReader(pdffileobj)
        # This will store the number of pages of this pdf file
        x = pdfreader.pages
        for page in x:
            # pageobj = pdfreader.pages(page)
            # text = pageobj.extractText()
            text = page.extract_text()
            file1 = open(txtWhitePapers + "/" + filename + ".txt", "a")
            file1.writelines(text)
            file1.close()
