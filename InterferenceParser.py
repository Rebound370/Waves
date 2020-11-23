import PyPDF2

#Extracts text from the pdf, removes lines that are purely numerical.
#Does not account for whitespace.
#Kinda dirty, sometimes drops characters.
#Does a lot of the work, but still needs to be formatted.

#opens Interference.pdf, writes all text into a txt file for easier maniplation
pdfReader = PyPDF2.PdfFileReader(open(r"C:\Users\Rebound\school\Code\Python\Interference.pdf", 'rb'))
pdfTxtConverter = open(r"C:\Users\Rebound\school\Code\Python\pdfRead.txt", "w")
pdfTxtConverter.write(pdfReader.getPage(0).extractText())
pdfTxtConverter.write(pdfReader.getPage(1).extractText())
pdfTxtConverter.write(pdfReader.getPage(2).extractText())
pdfTxtConverter.write(pdfReader.getPage(3).extractText())
pdfTxtConverter.write(pdfReader.getPage(4).extractText())
pdfTxtConverter.write(pdfReader.getPage(5).extractText())
print("Done reading PDF")
pdfTxtConverter.close()

#opens the recently created txt file and the output python file
TxtReader = open(r"C:\Users\Rebound\school\Code\Python\pdfRead.txt", "r")
PyWriter = open(r"C:\Users\Rebound\school\Code\Python\Interference.py", "w")

#parses the txt file line by line before writing to the output python file
i = 0
while True:
    line = TxtReader.readline()

    #if line is empty, end of file
    if not line:
        break
    
    #if any alphabetical characters are in the line, write line to python output
    if any(character.isalpha() for character in line):
        print("Line " + str(i) + ": alpha characters detected")
        PyWriter.write(line)
    
    #if no alphabetical characters are in the line, do nothing
    else:
        print("Line " + str(i) + ": no alpha characters detected")

    i += 1