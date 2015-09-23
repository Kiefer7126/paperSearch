# -*- coding: utf-8 -*- 

import codecs
import sqlite3
import os

if __name__ == "__main__":

  dbName         = "paper.db"
  tableName      = "paperIndex"
  selfFileName   = ""
  selfJurnalName = ""
  selfTitle      = ""
  selfAuthor     = ""

  conn = sqlite3.connect("./" + dbName)
  cur = conn.cursor()

# テーブルの有無を調べ，なければ作成
  cur = conn.execute("SELECT * FROM sqlite_master WHERE type = 'table' and name = '%s'" % tableName)
  if cur.fetchone() == None:
     cur.execute("CREATE TABLE %s(FileName TEXT, JurnalName TEXT, Title TEXT, Year INTEGER, Vol TEXT, Author TEXT)" % tableName)

# ディレクトリ内のファイルでループ
  files = os.listdir('./txt/')

  for selfFileName in files:
    print selfFileName

# ファイルを開く
    f = codecs.open("./txt/" + selfFileName,"r","utf-8")

    i = 1
    for row in f:
# 論文誌の名前
      if i == 3:
        selfJurnalName = row.encode('utf-8')
        selfJurnalName = selfJurnalName.replace("'","-")
        #改行コードの削除
        selfJurnalName = selfJurnalName.rstrip()   
# 論文のタイトル
      elif i == 6:
        selfTitle = row.encode('utf-8')
        selfTitle = selfTitle.replace("'","-")
        #改行コードの削除
        selfTitle = selfTitle.rstrip()
# 著者
      elif i == 7:
        selfAuthor = row.encode('utf-8')
        selfAuthor = selfAuthor.replace("'","-")
        #改行コードの削除
        selfAuthor = selfAuthor.rstrip()

      i += 1 
  
    f.close()

# 新規データの追加
    cur.execute("INSERT INTO %s(FileName, JurnalName, Title, Author) VALUES ('%s', '%s', '%s', '%s')" % (tableName, selfFileName.encode('utf-8'), selfJurnalName, selfTitle, selfAuthor))
  
  print "--------------------------------------------"

  fjn = codecs.open("./JurnalName.txt","w","utf-8")
  ft = codecs.open("./Title.txt","w","utf-8")
  fa = codecs.open("./Author.txt","w","utf-8")

# テーブルの内容の書き込み
  cur.execute("SELECT * FROM %s" % tableName)
  for FileName, JurnalName, Title, Year, Vol, Author in cur.fetchall():
    fjn.write(JurnalName)
    fjn.write("\n")
    ft.write(Title)
    ft.write("\n")
    fa.write(Author)
    fa.write("\n")
#    print u"[%s][%s][%s][%s][%s][%s]" % (FileName, JurnalName, Title, Year, Vol, Author)

  fjn.close()
  ft.close()
  fa.close()

  conn.commit()
  conn.close()