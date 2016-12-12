import zipfile
import os
import csv


import tempfile
import zipfile
import shutil
import os

def RemoveFileAndCreateNewZip(zipfname, filenamesToRemove, _dir, NewFileName):
    try:
        tempname = os.path.join(_dir, NewFileName+ ".odt")
        with zipfile.ZipFile(zipfname, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenamesToRemove:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
    except:
        pass

if __name__ == "__main__":
    #Get current Directory
    fileDir = str(os.path.dirname(os.path.realpath('__file__')))
    fileDir = fileDir.replace("\\", "/")

    #Attempt to get a template using input from the user
    while(True):
        try:
            templateNumber = int(input("What Template Are We Using?"))
            TemplateName = "/Templates/" + str(templateNumber) + "_template.odt"
            TemplateZip = zipfile.ZipFile(fileDir + TemplateName, "r")
            break
        except:
            pass

    #Grab list of files inside FilesToConvert
    CSV_Files = []
    for root, dirs, files in os.walk('./FilesToConvert/', topdown=True):
        dirs.clear()  # with topdown true, this will prevent walk from going into subs
        for file in files:
            # do some stuff
            CSV_Files.append(file)


    #For each CSV file name in list. Go through each and put their word file in ConvertedFiles.
    for csvFileName in CSV_Files:

        #Get our Directory, Add our file name to it.
        fileWeWant = '/FilesToConvert/' + csvFileName
        filename = fileDir + fileWeWant
        print(filename)
        with open(filename) as f:
            linesFromCSV = f.readlines()

            dreader = csv.DictReader(linesFromCSV)
            print(dreader.fieldnames)

            #Add addresses and owners to a list full of dicts
            peoples = []
            for row in dreader:
                #print(row["Address"])
                #print(row["Owner(s) Name(s)"])
                tempbar = {"Address": row["Address"], "Owner": row["Owner(s) Name(s)"]}
                peoples.append(tempbar)


            #Open our zip file -- Find how many entries per page.
            #print(TemplateZip.filelist)
            #Get our content file
            OurFile = TemplateZip.read("content.xml")
            FileAsText = str(OurFile, 'utf-8')
            EntiesPerPage = FileAsText.count("Testing")
            print("Entries Per Page:" + str(EntiesPerPage))


            pesNum = 0  #What record we're on



            #Cycle through xml where testing is at. Replace testing0... all of them. with addresses. If no address is left.
            #Replace it with nothing.
            for i in range(EntiesPerPage):
                #Format our addresses here.
                try:
                    TestForAddress = peoples[i]["Owner"] + "\n" + peoples[i]["Address"]
                    FileAsText = FileAsText.replace("Testing"+str(i), TestForAddress)
                except:
                    FileAsText = FileAsText.replace("Testing"+str(i), "")

            ConvertedDir = fileDir+"/ConvertedFiles/"
            newFileName = "Another1"
            print(FileAsText)
            RemoveFileAndCreateNewZip(fileDir + TemplateName, ['content.xml'], fileDir+"/ConvertedFiles/", "Another1")
            OurNewZip = zipfile.ZipFile(ConvertedDir + newFileName + ".odt", "a")
            OurNewZip.writestr("content.xml", FileAsText)


        #Grab ODT File.
        #file = zipfile.ZipFile("Templates/One")
    #Open as zip.
    #Change Directory to xml
    #Grab xml file
    #Grab csv file. Organize as Dict.
    #Loop through Dict.
    #Insert into file as test_NUm
    #Save file as we reach limit.
    #Enumerate and continue.