import os
import re
import datetime
if __name__ == '__main__':
    #os.system("git pull https://github.com/LinghaoChan/CSSummerCamp2022.git")
    file = open('./CSSummerCamp2022/README.md', encoding='UTF-8')
    contents = file.readlines()
    file.close()
    #print(contents)
    useful_contents = []
    p1 = re.compile(r"【报名截止: \w+\.\w+\.\w+】")
    p2 = re.compile(r"【报名截止：\w+\.\w+\.\w+】")
    pt = re.compile(r"\w+\.\w+\.\w+")
    for x in contents:
        r1 = re.findall(p1, x)
        r2 = re.findall(p2, x)
        ti=""
        if len(r1) != 0:
          #  print(r1)
            ti = re.findall(pt, r1[0])[0]
        elif len(r2) != 0:
         #   print(r2)
            ti = re.findall(pt, r2[0])[0]
        else:
            continue
        #print(ti)
        #print(ti.split('.'))
        ti = ti.split('.')
        ti = [int(x) for x in ti]
       # print(ti)
        ti = datetime.datetime(ti[0],ti[1],ti[2])
       # print(ti)
        useful_contents.append((x,ti))
    useful_contents = sorted(useful_contents, key=lambda x:x[1])
    # print(useful_contents)
    td = datetime.date.today()
    td = datetime.datetime(td.year,td.month,td.day)
    # print(td)
    due_contents = [x for x in useful_contents if not x[1] < td]
    overdue_contents = [x for x in useful_contents if x[1] < td]
    file = open('./README.md','w',encoding='UTF-8')
    for x in due_contents:
        file.write(x[0]+'\n')
    file.write('### Overdued\n')
    for x in overdue_contents:
        file.write(x[0]+'\n')
    file.close()
