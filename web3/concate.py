import os

directory = '.'
txtWhitePapers = directory + "/txtWhitePapers"
final_filename = 'web3'
for filename in os.listdir(txtWhitePapers):
    print(filename)
    if filename == ".DS_Store":
        pass
    else:
        pdffileobj = open(directory + "/txtWhitePapers" + "/" + filename, 'rb')
        for text in pdffileobj:
            file1 = open("./" + final_filename + ".txt", "a")
            file1.writelines(text.decode('utf-8'))
            file1.close()