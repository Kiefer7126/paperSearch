# -*- coding: utf-8 -*- 

import codecs
import sqlite3
import os
import math

#TF-IDF

def tf(all_terms, all_documents):
  tf_column = []
  for document in all_documents:
    tf_row = []
    for term in all_terms:
      try:
        tf_row.append(document.count(term)* 1.0 / len(document))
      except:
        tf_row.append(document.count(term))
    tf_column.append(tf_row)
  return tf_column

def idf(all_terms, all_documents):
  idf_value = []
  # 論文数
  document_num = len(all_documents[0])
  for term in all_terms:
    count = 0
    for document in all_documents:
      if term in document:
        count += 1
    idf_value.append(math.log10(document_num / count + 1))
  return idf_value

def tf_idf(all_terms, all_documents):
  tf_idf_column = []
  tf_matrix = tf(all_terms, all_documents)
  idf_row = idf(all_terms, all_documents)

  for tf_row in tf_matrix:
    tf_idf_row = []
    for (a, b) in zip(tf_row, idf_row):
      tf_idf_row.append(a * b)
    tf_idf_column.append(tf_idf_row)
  # print len(all_terms)
  # print len(idf_row)
  # print len(tf_matrix[0])
  return tf_idf_column

if __name__ == "__main__":

  # 全ての単語リスト
  all_terms = []
  # 論文毎の単語行列
  all_documents = []
  db_terms = []

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
     cur.execute("CREATE TABLE %s(FileName TEXT, JurnalName TEXT, Title TEXT, Year INTEGER, Vol TEXT, Author TEXT, terms TEXT)" % tableName)

# ディレクトリ内のファイルでループ
  files = os.listdir('./txt/')

  for selfFileName in files:
    #print selfFileName

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

#TF-IDF
  files = os.listdir('./terms/')

  for selfFileName in files:  
    document = []
    f = open('./terms/' + selfFileName, "r")
    for line in f:
      try:
        if line.split("\t")[1].startswith("N"):
          word = line.split("\t")[2]
          word = word.rstrip("\n")
          #重複あり
          document.append(word)

          if word in all_terms:
            pass
          else:
            all_terms.append(word)
      except:
        print "error"

    all_documents.append(document)

  fa = open("./all_terms.txt","w")
  for row in all_terms:
    fa.write(row)
    fa.write("\n")

  tf_idf_matrix = tf_idf(all_terms, all_documents)

  k = 0
  for tf_idf_row in tf_idf_matrix:
    sorted_matrix = sorted(tf_idf_row, reverse = True)
    #print sorted_matrix

    index = 0
    top_terms = []
    for rank in range(0,10):
      word_num = tf_idf_row.count(sorted_matrix[rank + index])
      if word_num < 7:
        for i in range(0, word_num): 
          top_terms.append(all_terms[tf_idf_row.index(sorted_matrix[rank + index]) + i])
        index += word_num
    
    interm = ""
    for term in top_terms:
      interm += term + ","

    interm = interm.replace("'","-")
    cur.execute("UPDATE %s SET terms = '%s' WHERE FileName = '%s'" % (tableName, interm, files[k].lstrip("out_").encode('utf-8')))
    k += 1

      #db_terms.append(top_terms)
# debag
  # fdb = open("./db_terms.txt","w")
  # for terms in db_terms:
  #   for term in terms:
  #     fdb.write(term)
  #     fdb.write("\n")
  #   fdb.write("---------------------------------")

#   fjn = codecs.open("./JurnalName.txt","w","utf-8")
#   ft = codecs.open("./Title.txt","w","utf-8")
#   fa = codecs.open("./Author.txt","w","utf-8")
#   fte = codecs.open("./terms.txt","w","utf-8")

# # テーブルの内容の書き込み
#   cur.execute("SELECT * FROM %s" % tableName)
#   for FileName, JurnalName, Title, Year, Vol, Author, terms in cur.fetchall():
#     fjn.write(JurnalName)
#     fjn.write("\n")
#     ft.write(Title)
#     ft.write("\n")
#     fa.write(Author)
#     fa.write("\n")
#     fte.write(terms)
#     fte.write("\n")
# #    print u"[%s][%s][%s][%s][%s][%s]" % (FileName, JurnalName, Title, Year, Vol, Author)

#   fjn.close()
#   ft.close()
#   fa.close()
#   fte.close()

  conn.commit()
  conn.close()