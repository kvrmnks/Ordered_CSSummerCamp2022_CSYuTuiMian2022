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

def split_by_time(contents: list) -> tuple:
    p1 = re.compile(r"【报名截止[^】]*】")
    pt = re.compile(r"\w+\.\w+\.\w+")
    useful_contents = []
    no_date_contents = []
    undecidable_contents = []

    for x in contents:
        r1 = re.findall(p1, x)
        # print(r1)
        if len(r1) != 0:
            ti = re.findall(pt, r1[0])
            if len(ti) == 0:
                # print(x)
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
    
    return (due_contents, no_date_contents, overdue_contents, undecidable_contents)

if __name__ == '__main__':
    #os.system("git pull https://github.com/LinghaoChan/CSSummerCamp2022.git")
    file = open('./CSSummerCamp2022/README.md', encoding='UTF-8')
    summercamp_contents = file.readlines()
    file.close()
    
    file = open('./CSYuTuiMian2022/README.md', encoding='UTF-8')
    yutuimian_contents = file.readlines()
    file.close()
    # print(contents)

    summercamp_contents = preprocess(summercamp_contents)
    yutuimian_contents = preprocess(yutuimian_contents)

    (sc_due, sc_am, sc_dead, sc_ud) = split_by_time(summercamp_contents)
    (yt_due, yt_am, yt_dead, yt_ud) = split_by_time(yutuimian_contents)

    sc_due = [('[夏令营]'+x[0], x[1]) for x in sc_due]
    sc_dead= [('[夏令营]'+x[0], x[1]) for x in sc_dead]
    yt_due = [('[预推免]'+x[0], x[1]) for x in yt_due]
    yt_dead= [('[预推免]'+x[0], x[1]) for x in yt_dead]

    due = []
    due.extend(sc_due)
    due.extend(yt_due)
    due = sorted(due, key=lambda x:x[1])

    am = []
    am.extend(sc_am)
    am.extend(yt_am)

    dead = []
    dead.extend(sc_dead)
    dead.extend(yt_dead)
    dead = sorted(dead, key=lambda x:x[1])


    file = open('./README.md','w',encoding='UTF-8')
    file.write('数据来源: [CSSummerCamp2022](https://github.com/LinghaoChan/CSSummerCamp2022)     [CSYuTuiMian2022](https://github.com/CS-BAOYAN/CSYuTuiMian2022) \n')
    file.write('### 尚未截止\n')
    for x in due:
        file.write(x[0]+'\n')
    file.write('### 截止具体时间特殊\n')
    for x in am:
        file.write(x+'\n')
    file.write('### 已截止\n')
    for x in dead:
        file.write(x[0]+'\n')
    file.close()

    file = open('./CSSummerCamp2022_XOR.md','w',encoding='UTF-8')
    for x in sc_ud:
        file.write(x+'\n')
    file.close()

    file = open('./CSYuTuiMian2022_XOR.md','w',encoding='UTF-8')
    for x in yt_ud:
        file.write(x+'\n')
    file.close()