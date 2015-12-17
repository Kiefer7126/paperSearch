# -*- coding: utf-8 -*- 

import sqlite3
import os
import sys

def openPDF(selfFileName):
  print '----------------------------------'

  if len(selfFileName) == 0:
    print 'Not found!'
    quit()

  else:
    print u"開きたいファイル番号を入力、またはシステムの終了(n)"
    inputFileNum = raw_input()
    if inputFileNum.isdigit():
      os.system('C:/Users/b1012046/python/paperSearch/pdf/' + selfFileName[int(inputFileNum) - 1])
      quit()
    else:
      quit()

def printResults(fileNum, results):
  
  print '----------------------------------'
  print "[%s]" % fileNum
  
  i = 0
  
  for value in str(results).split(","):
    if i > 0:
      print value.lstrip("(u'").lstrip(" u'").rstrip("'").rstrip("')")
    i += 1

if __name__ == "__main__":

  dbName         = "paper.db"
  tableName      = "paperIndex"

  con = sqlite3.connect("./paper.db")
  cur = con.cursor()

  param = sys.argv
  paramLen = len(param)

  columnName = ""
  fileNum = 1
  selfFileName = []

  if paramLen <= 2:
    print 'Usage : python search.py -t hogehoge'
    print '        -t (title)'
    print '        -a (author)'
    print '        -k (terms)'
    quit()

  else:  
    if param[1] == '-t':
      columnName = 'Title'

    elif param[1] == '-a':
      columnName = 'Author'

    elif param[1] == '-k':
      columnName = 'terms'

    else:
      print 'Usage : python search.py -t hogehoge'
      print '        -t (title)'
      print '        -a (author)'
      print '        -k (terms)'
      quit()
  
    searchWord = '%' + param[2] + '%'
    for results in cur.execute("SELECT FileName, Title, Author FROM paperIndex WHERE %s LIKE '%s'" % (columnName, searchWord)):
      selfFileName.append(str(results).split(",")[0].lstrip("(u'").rstrip("txt',)") + "pdf")
      printResults(fileNum, results)
      fileNum += 1

  openPDF(selfFileName)

  con.commit()
  con.close()