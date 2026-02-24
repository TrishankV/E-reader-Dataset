# PDF page cutter 

data_source = r"cloudops.pdf"

output = "cloudopscut.pdf"


from PyPDF2 import PdfReader, PdfWriter

pagestodelete = [i for i in range(1,7) ]

reader = PdfReader(data_source)
writer = PdfWriter()

for i in range(len(reader.pages)):
    if (i+1) not in pagestodelete : 
        writer.add_page(reader.pages[i])

with open(output , "wb") as f : 
    writer.write(f)

print(output , "completed")