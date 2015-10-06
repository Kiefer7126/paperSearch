# -*- coding: utf-8 -*- 

import os

if __name__ == "__main__":

  files = os.listdir('./txt/')
  flag = 0

  for selfFileName in files:
    print selfFileName

# ファイルを開く
    f = open("./txt/" + selfFileName,"r")
    lines = f.readlines()
    line_number = 0

    for line in lines:
      
      if line.startswith('ABSTRACT') or line.startswith('Abstract') or line.startswith('abstract') or line.startswith('Keyword'):
        # print lines[line_number]
        # print lines[line_number + 1]
        fa = open("./abstract/" + selfFileName,"w")
        fa.write(lines[line_number])

        if lines[line_number + 1].startswith('Download'):
          line_number += 1

        fa.write(lines[line_number + 1])
        fa.close()

      line_number += 1

    f.close()

