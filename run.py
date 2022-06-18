import os
import re
import datetime

def preprocess(contents):
    current_university = ""
    processed_content = []
    for strip in contents:
        strip: str
        if strip.startswith("# "):
            current_university = strip[2:-1]
        ind = strip.find("】")
        if ind != -1:
            strip = strip[:ind+1] + f"[{current_university}] " + strip[ind+1:]
        
        processed_content.append(strip)
    
    return processed_content

if __name__ == '__main__':
    #os.system("git pull https://github.com/LinghaoChan/CSSummerCamp2022.git")
    file = open('./CSSummerCamp2022/README.md', encoding='UTF-8')
    contents = file.readlines()
    file.close()
    # print(contents)

    contents = preprocess(contents)

    useful_contents = []
    no_date_contents = []
    undecidable_contents = []
    p1 = re.compile(r"【报名截止[^】]*】")
    pt = re.compile(r"\w+\.\w+\.\w+")

    for x in contents:
        r1 = re.findall(p1, x)
        # print(r1)
        if len(r1) != 0:
            ti = re.findall(pt, r1[0])
            if len(ti) == 0:
                print(x)
                no_date_contents.append(x)
            else:
                ti = ti[0]
                ti = ti.split('.')
                ti = [int(x) for x in ti]
                ti = datetime.datetime(ti[0],ti[1],ti[2])
                useful_contents.append((x,ti))
        else:
            undecidable_contents.append(x)
        useful_contents = sorted(useful_contents, key=lambda x:x[1])
        td = datetime.date.today()
        td = datetime.datetime(td.year,td.month,td.day)
        due_contents = [x for x in useful_contents if not x[1] < td]
        overdue_contents = [x for x in useful_contents if x[1] < td]
    file = open('./README.md','w',encoding='UTF-8')
    file.write('### 尚未截止\n')
    for x in due_contents:
        file.write(x[0]+'\n')
    file.write('### 截止具体时间未定\n')
    for x in no_date_contents:
        file.write(x+'\n')
    file.write('### 已截止\n')
    for x in overdue_contents:
        file.write(x[0]+'\n')
    file.close()
    
    file = open('./XOR.md','w',encoding='UTF-8')
    for x in undecidable_contents:
        file.write(x+'\n')
    file.close()
