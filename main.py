import subprocess
from exif import Image
from PIL import Image
import os.path
from PyPDF2 import PdfFileReader, PdfFileWriter

fileToStrip = " "
exe = "exiftool"
image_without_exif = ""
substring = '.jpg'
cleanImage = ""


def displayMetadata(fileToStrip):
    process = subprocess.Popen([exe, fileToStrip], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               universal_newlines=True)
    metadata = []
    for output in process.stdout:
        info = {}
        line = output.strip().split(":")
        info[line[0].strip()] = line[1].strip()
        metadata.append(info)

    for data in metadata:
        print(data)


def eraseMetadata(fileToStrip):
    # next 3 lines strip exif
    # Add if conditions for pdf and images
    fileName = fileToStrip[6:]
    if ".pdf" in fileToStrip:
        print("\n\n.............................................")
        print("Deleting your metaData information.......")
        fin = open(fileToStrip, 'rb')
        reader = PdfFileReader(fin)
        writer = PdfFileWriter()
        writer.appendPagesFromReader(reader)
        metadata = reader.getDocumentInfo()
        writer.addMetadata(metadata)
        # Write your custom metadata here:
        # '/CreationDate': "", '/ModDate': "",
        writer.addMetadata({
            '/Creator': "", '/Producer': "", '/Author': "", '/InstanceId': "", '/DocumentId': ""
        })
        newFile = "no_PDF_Meta_Data_"+fileName
        fout = open("strippedPDFFiles/"+newFile, 'wb')  # ab is append binary; if you do wb, the file will append blank pages
        writer.write(fout)
        stripped_PDF_File = "strippedPDFFiles/"+newFile
        fin.close()
        fout.close()
        return stripped_PDF_File
    else:
        print("\n\n.............................................")
        print("Deleting your metaData information.......")
        image = Image.open(fileToStrip).convert('RGB')
        # image.save(fileToStrip, 'jpeg')
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        print("Saving your deleted metaDatafile........")
        # Save stripped file (throw stripped files into another folder to track)
        noDataImage = "no_Meta_Data_"+fileName
        image_without_exif.save("strippedFiles/" + noDataImage)
        strippedFile = "strippedFiles/" + noDataImage
        return strippedFile


# While loop until user quits
while True:
    fileToStrip = input("Enter your desired metaData file (or enter 'quit' to stop):")
    if fileToStrip.strip() == 'quit':
        break
    if not os.path.exists("files/" + fileToStrip):
        print("the file you entered does not exist, please check the file name and try again:")
    else:
        fileToStrip = "files/" + fileToStrip
        print(displayMetadata(fileToStrip))
        noData = eraseMetadata(fileToStrip)
        print(displayMetadata(noData))
