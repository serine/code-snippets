#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import argparse, sys, os, csv

#creat optional arguments using argparse module
parser = argparse.ArgumentParser(description="learnign to use argparse")

#parser.add_argument('directory', help='directory to use', action='store')
parser.add_argument('--rootDir',  default=os.getcwd(), help="specify root directory")
parser.add_argument('--fileDir', nargs=1, default=argparse.SUPPRESS, help="specify files directory")
parser.add_argument('--gtfFile', help="specify path to the gtf file")
#parser.print_help()
args = parser.parse_args()
rootDir = args.rootDir
fileDir = args.fileDir[0]
gtfFile = args.gtfFile

#----------------------------------------------------------------------
# This section traverses the root directory and looks for the 
# strandedreverse directories that hold htseq-count report files
# It then appends all files from those stranded reverse directories
# to one list listOfFiles
#----------------------------------------------------------------------


def getIDhash(uniqueID, publicID, feature, lines2skip):

    f = open(gtfFile)
    testDict = {}

    for skip in range(lines2skip):
         f.next()
    for i in f:
         line = i.strip().split("\t")
         #testList = i.strip().split("\t")[8]
         geneTest = line[2] 
         if geneTest == feature:
             info = line[8].split(";")
              
             gene_id = info[4].split()[1].strip('"')
             ensemble_id = info[0].split()[1].strip('"')
             biotype = info[2].split()[1].strip('"')
    
             testDict[ensemble_id]=[ensemble_id, gene_id, biotype]
    return testDict

testDict = getIDhash()
for key, value in testDict.items():
     print value
          #print line
     #    if 'transcript_id' in testList:
     #        ids = testList.split(";")
     #        print geneTest, ids[0], ids[1]
     #    #   print i.split()
     #if i.split()[-1] == "'rRNA'":
     #biotype = i.strip().split("\t")[-1].split(";")[4]
     #if 'gene_biotype' in biotype:
     #    testWord = biotype.split()[1].strip('"')
     #    if 'rRNA' in testWord:
     #        print i.strip()
def getListOfFiles(rootDir, fileDir):
    
    listOfFiles = []

    for root, dirs, files in os.walk(rootDir):
        if dirs:
            if fileDir in dirs:
                test = dirs[dirs.index(fileDir)]
                testDir = os.path.join(root, test)
                if testDir:
                    for i in os.listdir(testDir):
                        if i != ".dir_bash_history":
                            listOfFiles.append(os.path.join(testDir, i))
    return listOfFiles
#
listOfFiles = getListOfFiles(rootDir, fileDir)

output = open("htseq-cout-table.txt", "w")

column = []
columns = []
nameColumn = []

for textFile in listOfFiles:
    f = open(textFile)
    
    for line in f:

        #-------------------------------------------------------
        # This section is specifit for columns name formating
        #-------------------------------------------------------

        fileAsStr = str(f)
        tmpName = fileAsStr.split("/")[-1]
        
        if tmpName.startswith("cf"):

            tmpRoot = tmpName.split("_")
            tmp1 = tmpRoot.pop()
            tmp2 = tmpRoot.pop()
            rootName  = ''.join(tmpRoot)
            sampleId = str(rootName.split("-")[1])

        else:

            tmpRoot = tmpName.split("_")
            sampleId = str(tmpRoot[0])
        #-------------------------------------------------------

        if not line.startswith("__"):

            dataValue = line.strip().split()[-1]
            EnsemblName = line.strip().split()[0]

            if sampleId not in column:
                column.append(sampleId)

            column.append(dataValue)
        # I'm pretty sure I can just have 
        # if len(nameColumn) < len(column)
        # but I'll for now 
        if len(nameColumn) < 65218:
            if not nameColumn:
                nameColumn.append('Ensembl gene names')
            nameColumn.append(EnsemblName)

    if nameColumn not in columns:
        
        columns.append(nameColumn)

    columns.append(column)
    column = []
#print len(columns)#
for betterName in zip(*columns):
    #print len(betterName)
    #print betterName
    print '\t'.join(betterName)
    #output.write('\t'.join(betterName)+'\n')
