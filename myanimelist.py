# -*- coding: utf-8 -*-

print("importing modules...")
try:
    import os
    from os import remove
    import sqlite3
    import urllib.request
    from io import StringIO
    from PIL import Image
    import PIL
    import csv
    from lxml.html import parse
    import requests
    import tkinter as tk
    from tkinter import *
    from tkinter import messagebox
    from bs4 import BeautifulSoup
    from pandas import DataFrame, read_csv
    import pandas as pd
except:
    print('failed to import modules')
    exit()
#코드순서: sqlite > 버튼,새창 > tkinter

#create window object
window = Tk()
#표시줄이름
window.title("Animation DB")
#아이콘
window.wm_iconbitmap('./image/myicon.ico')
#창크기 고정
window.resizable(0, 0)
#창이 열리는 위치와 크기
window.geometry("450x600")

#폰트설정
normal_font = ('Verdana')
large_font = ('Verdana',20)
small_font = ('Verdana',10)

########################################################################################################
#sqlite db 접근 및 데이터 받기
print("connecting anime DB...")
conn = sqlite3.connect('animelist.sqlite')

cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Title (
    t_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL,
    t_name TEXT UNIQUE,
    genre_id INTEGER,
    production_id INTEGER,
    year_id INTEGER,
    quarter_id INTEGER
)''')
cur.execute('''
CREATE TABLE IF NOT EXISTS Genre (
    id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL,
    g_name TEXT UNIQUE
)''')
cur.execute('''
CREATE TABLE IF NOT EXISTS Production (
    id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL,
    p_name TEXT UNIQUE
)''')
cur.execute('''
CREATE TABLE IF NOT EXISTS Year (
    id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL,
    year TEXT UNIQUE
)''')
cur.execute('''
CREATE TABLE IF NOT EXISTS Quarter (
    id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL,
    quarter TEXT UNIQUE
)''')

conn.commit()

#quarter값은 미리 생성
bef = cur.execute('''SELECT quarter FROM Quarter''').fetchall()
if len(bef) == 0:
    for x in range(1,5):
        cur.execute(
        '''INSERT OR IGNORE INTO Quarter (quarter) VALUES (?)''', (x,)
        )
        conn.commit()



print("loading datas from DB...")
cur.execute('''SELECT t_name, g_name, p_name, year, quarter, t_id FROM Title JOIN Genre ON Title.genre_id = Genre.id JOIN Production ON Title.production_id = Production.id JOIN Year ON Title.year_id = Year.id JOIN Quarter ON Title.quarter_id = Quarter.id''')

lview = cur.fetchall()


if len(lview) == 0:
    totalcount = 0
    listnumber = 0
    animecount = 0
    a_title = 'None'
    a_genre = 'None'
    a_production = 'None'
    a_year = 'None'
    a_quarter = 'None'
    imagefile = './image/wink.gif'
else:
    totalcount = len(lview)
    animecount = 0
    listnumber = 1
    x=lview[animecount]
    a_title = x[0]
    a_genre = x[1]
    a_production = x[2]
    a_year = x[3]
    a_quarter = x[4]
    a_ttid = x[5]
    imagefile = './image/' + str(a_ttid) + ".gif"

#####################################################################################################

#버튼 작동, 새창 생성, 기타 함수

#change image
def changeim():
    global animecount
    global lview
    global logo
    global imagefile
    global photolabel

    try:
        imageid = lview[animecount][5]
        strimageid = str(imageid)
        imagefile = './image/' + strimageid + ".gif"
        logo = PhotoImage(file = imagefile)
        photolabel.configure(image = logo)
        photolabel.image = logo #항상 이미지가 나타날 수 있도록?
    except:
        imagefile = './image/'+"wink.gif"
        logo = PhotoImage(file = imagefile)
        photolabel.configure(image = logo)
        photolabel.image = logo #항상 이미지가 나타날 수 있도록?


#for next button
def nextanime():
    global lview
    global animecount
    global listnumber
    global totalcount
    animecount += 1
    listnumber += 1
    if listnumber > len(lview):
        animecount = 0
        listnumber = 1
        x=lview[0]
        a_title = x[0]
        a_genre = x[1]
        a_production = x[2]
        a_year = x[3]
        a_quarter = x[4]
        title_value.set(str(a_title))
        gen_value.set(str(a_genre))
        pro_value.set(str(a_production))
        year_value.set(str(a_year))
        ln_value.set(listnumber)
        quarter_value.set(a_quarter)
        changeim()
    else:
        x=lview[animecount]
        a_title = x[0]
        a_genre = x[1]
        a_production = x[2]
        a_year = x[3]
        a_quarter = x[4]
        title_value.set(str(a_title))
        gen_value.set(str(a_genre))
        pro_value.set(str(a_production))
        year_value.set(str(a_year))
        quarter_value.set(a_quarter)
        ln_value.set(listnumber)
        changeim()



#for prev button
def prevanime():
    global lview
    global animecount
    global listnumber
    global totalcount
    animecount -= 1
    listnumber -= 1
    if listnumber == 0:
        animecount = len(lview) - 1
        listnumber = len(lview)
        x=lview[-1]
        a_title = x[0]
        a_genre = x[1]
        a_production = x[2]
        a_year = x[3]
        a_quarter = x[4]
        title_value.set(str(a_title))
        gen_value.set(str(a_genre))
        pro_value.set(str(a_production))
        year_value.set(str(a_year))
        quarter_value.set(a_quarter)
        ln_value.set(listnumber)
        changeim()
    else:
        x=lview[animecount]
        a_title = x[0]
        a_genre = x[1]
        a_production = x[2]
        a_year = x[3]
        a_quarter = x[4]
        title_value.set(str(a_title))
        gen_value.set(str(a_genre))
        pro_value.set(str(a_production))
        year_value.set(str(a_year))
        quarter_value.set(a_quarter)
        ln_value.set(listnumber)
        changeim()

#########################################################################################################################
#new window
def InputData():
    input_window = Toplevel()
    input_window.title("create new data")
    input_window.wm_iconbitmap('./image/myicon.ico')
    input_window.resizable(0,0)
    input_window.geometry("+605+100")#창이 켜지는 위치 지정
    input_window.attributes('-topmost', 'true')#창 맨 앞으로
    input_window.grab_set()

    Label(input_window, relief=RIDGE, text="제목", width=8, font=normal_font).grid(row=0,column=0)

    it_value=StringVar()
    ie1 = Entry(input_window, relief=SUNKEN, textvariable=it_value, width=26, font=normal_font)
    ie1.grid(row=0,column=1)

    Label(input_window, relief=RIDGE, text="장르", width=8, font=normal_font).grid(row=1,column=0)

    ig_value=StringVar()
    ie2 = Entry(input_window, relief=SUNKEN, textvariable=ig_value, width=26, font=normal_font)
    ie2.grid(row=1,column=1)

    Label(input_window, relief=RIDGE, text="제작사", width=8, font=normal_font).grid(row=2,column=0)

    ip_value=StringVar()
    ie3 = Entry(input_window, relief=SUNKEN, textvariable=ip_value, width=26, font=normal_font)
    ie3.grid(row=2,column=1)

    Label(input_window, relief=RIDGE, text="연도", width=8, font=normal_font).grid(row=3,column=0)

    iy_value=StringVar()
    ie4 = Entry(input_window, relief=SUNKEN, textvariable=iy_value, width=26, font=normal_font)
    ie4.grid(row=3,column=1)

    Label(input_window, relief=RIDGE, text="분기", width=8, font=normal_font).grid(row=4,column=0)

    iq_value=StringVar()
    ie5 = Entry(input_window, relief=SUNKEN, textvariable=iq_value, width=26, font=normal_font)
    ie5.grid(row=4,column=1)




    # image download
    def getimage():
        cur.execute('''
        SELECT t_name, g_name, p_name, year, quarter, t_id
        FROM Title
        JOIN Genre ON Title.genre_id = Genre.id
        JOIN Production ON Title.production_id = Production.id
        JOIN Year ON Title.year_id = Year.id
        JOIN Quarter ON Title.quarter_id = Quarter.id
        ''')
        lview = cur.fetchall()
        imname = lview[-1][0]
        ss_url = lview[-1][5]
        s_url = str(ss_url)
        gi_url = 'https://namu.wiki/w/'
        urll =gi_url + imname
        savename = './image/' + s_url + ".gif"

        text = requests.get(urll).text
        soup = BeautifulSoup(text, 'html.parser')
        imagelist = soup.find("div", class_="wiki-table-wrap table-right")
        imlist = imagelist.find("img", class_="wiki-image")

        ilist = imlist.get("data-src")
        imsrc = str(ilist)
        rsrc = "https:" + imsrc

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(rsrc, savename)

        y1 = PIL.Image.open(savename)
        y1size = 300, 320
        rey1 = y1.resize(y1size)
        rey1.save(savename)


    #press button function -> add new anime data
    def ad2db():
        global totalcount
        global listnumber
        global animecount
        global lview
        itn = it_value.get()
        ign = ig_value.get()
        ipn = ip_value.get()
        iyn = iy_value.get()
        iqn = iq_value.get()

        if itn == "" or ign == "" or ipn == "" or iyn == "" or iqn == "":
            messagebox.showinfo("error","please, fill blanks", parent=input_window)

        elif iqn not in ("1", "2", "3", "4"):
            messagebox.showinfo("error","quarter value must be 1~4 !", parent=input_window)

        else:
            xx = [i for i in lview if itn in i]
            if xx:#xx값이 하나라도 있다면
                sn = xx[0][0]
            else:
                sn = 0
            if itn == sn:
                messagebox.showinfo("error","this title is already in the list", parent=input_window)
            else:
                f_quarter = cur.execute("SELECT id From Quarter WHERE quarter = ?", [iqn]).fetchone()[0]
                cur.execute('''INSERT OR IGNORE INTO  Year (year) VALUES (?)''', (iyn,))
                f_year = cur.execute("SELECT id From Year WHERE year = ?", [iyn]).fetchone()[0]
                cur.execute('''INSERT OR IGNORE INTO Production (p_name) VALUES (?)''', (ipn,))
                f_production = cur.execute("SELECT id From Production WHERE p_name = ?", [ipn]).fetchone()[0]
                cur.execute('''INSERT OR IGNORE INTO Genre (g_name) VALUES (?)''', (ign,))
                f_genre = cur.execute("SELECT id From Genre WHERE g_name = ?", [ign]).fetchone()[0]
                cur.execute('''INSERT INTO Title (t_name, genre_id, production_id, year_id, quarter_id ) VALUES (?,?,?,?,?)''', (itn, f_genre, f_production, f_year, f_quarter ))
                conn.commit()
                try:
                    getimage()
                except:
                    messagebox.showinfo("error", "Failed to get an image", parent=input_window)
                pvbt.configure(state=NORMAL)
                nxbt.configure(state=NORMAL)
                if totalcount == 0:
                    cur.execute('''SELECT t_name, g_name, p_name, year, quarter, t_id
                    FROM Title
                    JOIN Genre ON Title.genre_id = Genre.id
                    JOIN Production ON Title.production_id = Production.id
                    JOIN Year ON Title.year_id = Year.id
                    JOIN Quarter ON Title.quarter_id = Quarter.id''')
                    lview = cur.fetchall()
                    totalcount += 1
                    listnumber += 1
                    animecount = 0
                    title_value.set(itn)
                    gen_value.set(ign)
                    pro_value.set(ipn)
                    year_value.set(iyn)
                    quarter_value.set(iqn)
                    ln_value.set(str(listnumber))
                    listviewcount.set("total "+ str(totalcount))
                    changeim()
                    messagebox.showinfo("done", "New data is inserted!", parent=input_window)
                else:
                    cur.execute('''SELECT t_name, g_name, p_name, year, quarter, t_id
                    FROM Title
                    JOIN Genre ON Title.genre_id = Genre.id
                    JOIN Production ON Title.production_id = Production.id
                    JOIN Year ON Title.year_id = Year.id
                    JOIN Quarter ON Title.quarter_id = Quarter.id''')
                    lview = cur.fetchall()
                    listnumber = len(lview)
                    totalcount = len(lview)
                    animecount = listnumber - 1
                    title_value.set(itn)
                    gen_value.set(ign)
                    pro_value.set(ipn)
                    year_value.set(iyn)
                    quarter_value.set(iqn)
                    ln_value.set(str(listnumber))
                    listviewcount.set("total "+ str(totalcount))
                    changeim()
                    messagebox.showinfo("done", "New data is inserted!", parent=input_window)

    ib1 = Button(input_window, state=NORMAL, command=ad2db, text="SAVE", width=58, pady=20)
    ib1.grid(row=5,columnspan=2, pady=5)
    input_window.mainloop()

#delete window
def DeleteData():
    global lview
    delete_window = Toplevel()
    delete_window.title("delete data")
    delete_window.wm_iconbitmap('./image/myicon.ico')
    delete_window.resizable(0,0)
    delete_window.geometry("+605+100")
    delete_window.attributes('-topmost', 'true')
    delete_window.grab_set()

    dwf = LabelFrame(delete_window, text = ' Anime List ')
    dwf.pack()

    scroll = Scrollbar(dwf)
    scroll.pack(side="right", fill="y")

    listboxx = Listbox(dwf, selectmode='extended', width=55, height=10, relief='solid', yscrollcommand= scroll.set)
    for max in range(len(lview)):
        listboxx.insert(max, str(str(max+1)+ ": " + lview[max][0]))
    listboxx.pack(side="left")

    scroll.config(command=listboxx.yview)

    def delfdb():
        global animecount
        global listnumber
        global totalcount
        global lview
        resultex = listboxx.curselection()
        if not resultex:
            messagebox.showinfo('error','please, select data!', parent=delete_window)
        else:
            listindex = resultex[0]
            bfn = lview[listindex]
            fn = bfn[5]#선택한애니메이션의id값
            listboxx.delete(listindex)
            cur.execute('''DELETE FROM Title WHERE t_id=?''',(fn,))
            conn.commit()
            cur.execute('''SELECT t_name, g_name, p_name, year, quarter, t_id
            FROM Title
            JOIN Genre ON Title.genre_id = Genre.id
            JOIN Production ON Title.production_id = Production.id
            JOIN Year ON Title.year_id = Year.id
            JOIN Quarter ON Title.quarter_id = Quarter.id''')
            lview = cur.fetchall()

            totalcount = len(lview)
            listviewcount.set("total "+ str(totalcount))
            delete_window.destroy()
            try:
                fn = str(fn)
                os.remove('./image/' + fn + '.gif')
            except:
                pass

            if not lview:
                totalcount = 0
                animecount = 0
                listnumber = 0
                title_value.set('None')
                gen_value.set('None')
                pro_value.set('None')
                year_value.set('None')
                quarter_value.set('None')
                listviewcount.set("total "+ str(totalcount))
                ln_value.set(listnumber)
                imagefile = './image/wink.gif'
                logo = PhotoImage(file = imagefile)
                photolabel.configure(image = logo)
                photolabel.image = logo
                pvbt.configure(state=DISABLED)
                nxbt.configure(state=DISABLED)
            messagebox.showinfo('done','data is deleted!')


    deletebutton = Button(delete_window, text="DELETE", width=50, command=delfdb)
    deletebutton.pack()
    delete_window.mainloop()

def showall():
    global lview
    sal_window = Toplevel()
    sal_window.title("showall")
    sal_window.wm_iconbitmap('./image/myicon.ico')
    sal_window.resizable(0,0)
    sal_window.geometry("+605+100")
    sal_window.attributes('-topmost', 'true')
    sal_window.grab_set()#해당 창만 포커스

    swf = LabelFrame(sal_window, text = ' List ')
    swf.pack()

    scroll2 = Scrollbar(swf)
    scroll2.pack(side="right", fill="y")

    showlistbox = Listbox(swf, selectmode='extended', width=55, height=20, relief='solid', yscrollcommand= scroll2.set)
    for maxx in range(len(lview)):
        showlistbox.insert(maxx, str(str(maxx+1)+ ": " + lview[maxx][0]))
    showlistbox.pack(side="left")

    scroll2.config(command=showlistbox.yview)

    def gobutt():
        global lview
        global animecount
        global listnumber
        resultex2 = showlistbox.curselection()
        if resultex2 == ():
            messagebox.showinfo('error','please, select data!', parent=sal_window)
        else:
            animecount = resultex2[0]
            listnumber = animecount + 1
            x=lview[animecount]
            a_title = x[0]
            a_genre = x[1]
            a_production = x[2]
            a_year = x[3]
            a_quarter = x[4]
            title_value.set(str(a_title))
            gen_value.set(str(a_genre))
            pro_value.set(str(a_production))
            year_value.set(str(a_year))
            quarter_value.set(str(a_quarter))
            ln_value.set(listnumber)
            changeim()
            sal_window.destroy()

    def ModifyData():
        global lview
        global animecount
        global listnumber

        resultex3 = showlistbox.curselection()

        if resultex3 == ():
            modierror = messagebox.showinfo('error','please, select data!', parent=sal_window)
        else:
            listorder = resultex3[0]
            x = lview[listorder]
            m_title = x[0]
            m_genre = x[1]
            m_pro = x[2]
            m_year = x[3]
            m_qua = x[4]
            mod_window = Toplevel()
            mod_window.title("modify")
            mod_window.wm_iconbitmap('./image/myicon.ico')
            mod_window.resizable(0,0)
            mod_window.lift()
            mod_window.geometry("+605+100")
            mod_window.attributes('-topmost', 'true')
            sal_window.grab_release()
            mod_window.grab_set()

            Label(mod_window, relief=RIDGE, text="제목", width=8, font=normal_font).grid(row=0,column=0)

            mt_value=StringVar()
            mt_value.set(m_title)
            me1 = Entry(mod_window, relief=SUNKEN, textvariable=mt_value, width=26, font=normal_font)
            me1.grid(row=0,column=1)

            Label(mod_window, relief=RIDGE, text="장르", width=8, font=normal_font).grid(row=1,column=0)

            mg_value=StringVar()
            mg_value.set(m_genre)
            me2 = Entry(mod_window, relief=SUNKEN, textvariable=mg_value, width=26, font=normal_font)
            me2.grid(row=1,column=1)

            Label(mod_window, relief=RIDGE, text="제작사", width=8, font=normal_font).grid(row=2,column=0)

            mp_value=StringVar()
            mp_value.set(m_pro)
            me3 = Entry(mod_window, relief=SUNKEN, textvariable=mp_value, width=26, font=normal_font)
            me3.grid(row=2,column=1)

            Label(mod_window, relief=RIDGE, text="연도", width=8, font=normal_font).grid(row=3,column=0)

            my_value=StringVar()
            my_value.set(m_year)
            me4 = Entry(mod_window, relief=SUNKEN, textvariable=my_value, width=26, font=normal_font)
            me4.grid(row=3,column=1)

            Label(mod_window, relief=RIDGE, text="분기", width=8, font=normal_font).grid(row=4,column=0)

            mq_value=StringVar()
            mq_value.set(m_qua)
            me5 = Entry(mod_window, relief=SUNKEN, textvariable=mq_value, width=26, font=normal_font)
            me5.grid(row=4,column=1)

            def moddata():
                global lview
                global animecount
                global listnumber

                mtn = str(mt_value.get())
                mgn = str(mg_value.get())
                mpn = str(mp_value.get())
                myn = str(my_value.get())
                mqn = str(mq_value.get())

                try:
                    cur.execute('''SELECT id FROM Genre WHERE g_name =?''',(mgn,))
                    mgn2 = cur.fetchone()[0]
                except:
                    cur.execute('''INSERT OR IGNORE INTO Genre (g_name) VALUES (?)''', (mgn,))
                    cur.execute('''SELECT id FROM Genre WHERE g_name =?''',(mgn,))
                    mgn2 = cur.fetchone()[0]

                try:
                    cur.execute('''SELECT id FROM Production WHERE p_name =?''',(mpn,))
                    mpn2 = cur.fetchone()[0]
                except:
                    cur.execute('''INSERT OR IGNORE INTO Production (p_name) VALUES (?)''', (mpn,))
                    cur.execute('''SELECT id FROM Production WHERE p_name =?''',(mpn,))
                    mpn2 = cur.fetchone()[0]

                try:
                    cur.execute('''SELECT id FROM Year WHERE year =?''',(myn,))
                    myn2 = cur.fetchone()[0]
                except:
                    cur.execute('''INSERT OR IGNORE INTO  Year (year) VALUES (?)''', (myn,))
                    cur.execute('''SELECT id FROM Year WHERE year =?''',(myn,))
                    myn2 = cur.fetchone()[0]

                cur.execute('''SELECT id FROM Quarter WHERE quarter =?''',(mqn,))
                mqn2 = cur.fetchone()[0]

                cur.execute('''UPDATE Title SET t_name = ? WHERE t_name = ?''',(mtn,m_title))
                cur.execute('''UPDATE Title SET genre_id = ? WHERE t_name = ?''',(mgn2,m_title))
                cur.execute('''UPDATE Title SET production_id = ? WHERE t_name = ?''',(mpn2,m_title))
                cur.execute('''UPDATE Title SET year_id = ? WHERE t_name = ?''',(myn2,m_title))
                cur.execute('''UPDATE Title SET quarter_id = ? WHERE t_name = ?''',(mqn2,m_title))

                conn.commit()
                messagebox.showinfo('updated!','수정되었습니다!', parent=mod_window)

                cur.execute('''SELECT t_name, g_name, p_name, year, quarter, t_id
                FROM Title
                JOIN Genre ON Title.genre_id = Genre.id
                JOIN Production ON Title.production_id = Production.id
                JOIN Year ON Title.year_id = Year.id
                JOIN Quarter ON Title.quarter_id = Quarter.id''')
                lview = cur.fetchall()
                animecount = resultex3[0]
                listnumber = animecount + 1
                x=lview[animecount]
                a_title = x[0]
                a_genre = x[1]
                a_production = x[2]
                a_year = x[3]
                a_quarter = x[4]
                title_value.set(str(a_title))
                gen_value.set(str(a_genre))
                pro_value.set(str(a_production))
                year_value.set(str(a_year))
                quarter_value.set(str(a_quarter))
                ln_value.set(listnumber)
                imageid = x[5]
                strimageid = str(imageid)
                imagefile = './image/' + strimageid + ".gif"
                logo = PhotoImage(file = imagefile)
                photolabel.configure(image = logo)
                photolabel.image = logo
                sal_window.destroy()
                mod_window.destroy()

            mb1 = Button(mod_window, state=NORMAL, command=moddata, text="수정", width=58, pady=20)
            mb1.grid(row=5,columnspan=2, pady=5)
            mod_window.mainloop()

    gobutton = Button(sal_window, text="GO", width=50, command=gobutt)
    gobutton.pack()

    modifybutton = Button(sal_window, text="MODIFY", width=50, command=ModifyData)
    modifybutton.pack()
    sal_window.mainloop()

def exportw():
    global lview
    export_window = Toplevel()
    export_window.title("Export")
    export_window.wm_iconbitmap('./image/myicon.ico')
    export_window.resizable(0,0)
    export_window.attributes('-topmost', 'true')
    export_window.grab_set()

    def excsv():
        cur.execute('''
        SELECT t_name, g_name, p_name, year, quarter
        FROM Title
        JOIN Genre ON Title.genre_id = Genre.id
        JOIN Production ON Title.production_id = Production.id
        JOIN Year ON Title.year_id = Year.id
        JOIN Quarter ON Title.quarter_id = Quarter.id
        ''')
        lview = cur.fetchall()

        head_row = [('Title', 'Genre', 'Production', 'Year', 'Quarter')]

        with open('list.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(head_row)
            writer.writerows(lview)

        csvFile.close()
        export_window.destroy()
        messagebox.showinfo('done','csvfile is created!')

    def exxls():
        cur.execute('''
        SELECT t_name, g_name, p_name, year, quarter
        FROM Title
        JOIN Genre ON Title.genre_id = Genre.id
        JOIN Production ON Title.production_id = Production.id
        JOIN Year ON Title.year_id = Year.id
        JOIN Quarter ON Title.quarter_id = Quarter.id
        ''')
        lview = cur.fetchall()
        df = pd.DataFrame(data = lview, columns=['Title', 'Genre', 'Production', 'Year', 'Quarter'])
        df.index += 1
        df.to_excel('list.xls',index=True,header=True)

    Label(export_window, text='export to csv file', font=large_font).grid(row=0, column=0, padx=5, pady=10)
    Label(export_window, text='export to xls file', font=large_font).grid(row=1, column=0, padx=5, pady=10)
    csvbutton = Button(export_window, text='EXPORT', font=large_font, state=NORMAL, command=excsv)
    csvbutton.grid(row=0, column=1, padx=5, pady=10)
    xlsbutton = Button(export_window, text='EXPORT', font=large_font, state=NORMAL, command=exxls)
    xlsbutton.grid(row=1, column=1, padx=5, pady=10)

    if not lview:
        csvbutton.configure(text='NO DATAS',state='disabled')
        xlsbutton.configure(text='NO DATAS',state='disabled')
    export_window.mainloop()

def aboutmew():
    aboutme_window = Toplevel()
    aboutme_window.title("About me")
    aboutme_window.wm_iconbitmap('./image/myicon.ico')
    aboutme_window.resizable(0,0)
    aboutme_window.geometry("+150+100")
    aboutme_window.attributes('-topmost', 'true')
    Label(aboutme_window, text='made by. MSE', width=30, padx=5, pady=5).grid(row=0,columnspan=3, padx=5, pady=5)
    Label(aboutme_window, text='0.785 ver', width=30, padx=5, pady=5).grid(row=1,columnspan=3, padx=5, pady=5)
    aboutme_window.mainloop()

#####################################################################################################################



#define menu bar
menu1 = Menu(window)
filemenu = Menu(menu1,tearoff=0)
filemenu.add_command(label="show all", command=showall)
filemenu.add_separator()
filemenu.add_command(label="new data", command=InputData)
filemenu.add_command(label="delete data", command=DeleteData)
filemenu.add_separator()
filemenu.add_command(label="quit", command=window.destroy)
menu1.add_cascade(label="Data", menu=filemenu)
expmenu = Menu(menu1,tearoff=0)
expmenu.add_command(label="export to CSV", command=exportw)
menu1.add_cascade(label="Export", menu=expmenu)
aboutmenu = Menu(menu1,tearoff=0)
aboutmenu.add_command(label="About me", command=aboutmew)
menu1.add_cascade(label="About", menu=aboutmenu)
window.config(menu=menu1)





######################################################################################################################
#frame1
ff = LabelFrame(window, text=" Search ")
ff.pack(fill=X)

#image label
try:
    logo = PhotoImage(file=imagefile)
except:
    logo = PhotoImage(file='./image/wink.gif')
photolabel = Label(ff, image=logo)
photolabel.image = logo #항상 이미지가 나타날 수 있도록?
photolabel.grid(row=0, columnspan=4)

#define buttons
pvbt = Button(ff, text="Prev", width=23, command=prevanime, state='disabled')
pvbt.grid(row=1, column=0)

listviewcount=StringVar()
listviewcount.set("total "+ str(totalcount))
Label(ff, textvariable=listviewcount, width=10).grid(row=1, column=1)

ln_value=StringVar()
ln_value.set(listnumber)
Entry(ff, textvariable=ln_value, width=4).grid(row=1, column=2)

nxbt = Button(ff, text="Next", width=23, command=nextanime, state='disabled')
nxbt.grid(row=1, column=3)

if len(lview) > 0:
    pvbt.configure(state=NORMAL)
    nxbt.configure(state=NORMAL)
###############################################################################################################




################################################################################################################
#frame2
sf = LabelFrame(window, text=" Result ")
sf.pack(fill=X)

#define 5 labels Title, Genre, Production, Year, Quarter
Label(sf, relief=RIDGE, text="제목", width=5, height=1, font=large_font).grid(row=0,column=0)

Label(sf, relief=RIDGE, text="장르", width=5, height=1, font=large_font).grid(row=1,column=0)

Label(sf, relief=RIDGE, text="제작사", width=5, height=1, font=large_font).grid(row=2,column=0)

Label(sf, relief=RIDGE, text="연도", width=5, height=1, font=large_font).grid(row=3,column=0)

Label(sf, relief=RIDGE, text="분기", width=5, height=1, font=large_font).grid(row=4,column=0)

#show title name
title_value=StringVar()
title_value.set(str(a_title))
Entry(sf, relief=SUNKEN, textvariable=title_value, width=20, font=large_font).grid(row=0, column=1, columnspan=4)

#show genre
gen_value=StringVar()
gen_value.set(str(a_genre))
Entry(sf, relief=SUNKEN, textvariable=gen_value, width=20, font=large_font).grid(row=1, column=1)

#show production
pro_value=StringVar()
pro_value.set(str(a_production))
Entry(sf, relief=SUNKEN, textvariable=pro_value, width=20, font=large_font).grid(row=2, column=1)

#show year
year_value=StringVar()
year_value.set(str(a_year))
Entry(sf, relief=SUNKEN, textvariable=year_value, width=20, font=large_font).grid(row=3, column=1)

#show quarter
quarter_value=StringVar()
quarter_value.set(str(a_quarter))
Entry(sf, relief=SUNKEN, textvariable=quarter_value, width=20, font=large_font).grid(row=4, column=1)
#######################################################################################################################














#remain in the event loop until close the window

window.mainloop()
conn.close()
