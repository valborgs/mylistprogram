# -*- coding: utf-8 -*-

print("importing modules...")
try:
    from os import remove
    import csv
    import tkinter as tk
    from tkinter import *
    from tkinter import messagebox
    from pandas import DataFrame, read_csv
    from mydb import ConDB
    from myimg import Img
    from mychart import Drawchart
except:
    print('failed to import modules')
    exit()

window = Tk()
window.title("Animation DB")
window.wm_iconbitmap('./image/myicon.ico')
window.resizable(0, 0)
window.geometry("450x600")

normal_font = ('Verdana')
large_font = ('Verdana',20)
small_font = ('Verdana',10)

########################################################################################################

cndb = ConDB()
cndb.conndb()
cndb.createtable()
cndb.loaddata()


if not cndb.lview:
    imagefile = './image/wink.gif'
else:
    imagefile = './image/' + str(cndb.lview[0][5]) + ".gif"

#####################################################################################################

#change image
def changeim():
    global logo
    global imagefile
    global photolabel

    try:
        imageid = cndb.lview[cndb.animecount][5]
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

def set_label_value():
    title_value.set(str(cndb.a_title))
    gen_value.set(str(cndb.a_genre))
    pro_value.set(str(cndb.a_production))
    year_value.set(str(cndb.a_year))
    quarter_value.set(cndb.a_quarter)
    ln_value.set(cndb.listnumber)

#for next button
def nextanime():
    cndb.nextdata()
    if cndb.listnumber > len(cndb.lview):
        cndb.gofirstdata()
        set_label_value()
        changeim()
    else:
        cndb.sdata()
        set_label_value()
        changeim()

#for prev button
def prevanime():
    cndb.prevdata()
    if cndb.listnumber == 0:
        cndb.animecount = len(cndb.lview) - 1
        cndb.listnumber = len(cndb.lview)
        x=cndb.lview[-1]
        cndb.a_title = x[0]
        cndb.a_genre = x[1]
        cndb.a_production = x[2]
        cndb.a_year = x[3]
        cndb.a_quarter = x[4]
        set_label_value()
        changeim()
    else:
        cndb.sdata()
        set_label_value()
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
        cndb.getlist()
        imname = cndb.lview[-1][0]
        ss_url = cndb.lview[-1][5]
        myimg = Img(ss_url, imname)
        myimg.getimg()

    #press button function -> add new anime data
    def ad2db():
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
            xx = [i for i in cndb.lview if itn in i]
            if xx:#xx값이 하나라도 있다면
                sn = xx[0][0]
            else:
                sn = 0
            if itn == sn:
                messagebox.showinfo("error","this title is already in the list", parent=input_window)
            else:
                cndb.adddata(iqn, iyn, ipn, ign, itn)
                try:
                    getimage()
                except:
                    messagebox.showinfo("error", "Failed to get an image", parent=input_window)
                pvbt.configure(state=NORMAL)
                nxbt.configure(state=NORMAL)
                if cndb.totalcount == 0:
                    cndb.getlist()
                    cndb.totalcount += 1
                    cndb.listnumber += 1
                    cndb.animecount = 0
                    title_value.set(itn)
                    gen_value.set(ign)
                    pro_value.set(ipn)
                    year_value.set(iyn)
                    quarter_value.set(iqn)
                    ln_value.set(str(cndb.listnumber))
                    listviewcount.set("total "+ str(cndb.totalcount))
                    changeim()
                    messagebox.showinfo("done", "New data is inserted!", parent=input_window)
                else:
                    cndb.getlist()
                    cndb.listnumber = len(cndb.lview)
                    cndb.totalcount = len(cndb.lview)
                    cndb.animecount = cndb.listnumber - 1
                    title_value.set(itn)
                    gen_value.set(ign)
                    pro_value.set(ipn)
                    year_value.set(iyn)
                    quarter_value.set(iqn)
                    ln_value.set(str(cndb.listnumber))
                    listviewcount.set("total "+ str(cndb.totalcount))
                    changeim()
                    messagebox.showinfo("done", "New data is inserted!", parent=input_window)

    ib1 = Button(input_window, state=NORMAL, command=ad2db, text="SAVE", width=58, pady=20)
    ib1.grid(row=5,columnspan=2, pady=5)
    input_window.mainloop()

#delete window
def DeleteData():
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
    for max in range(len(cndb.lview)):
        listboxx.insert(max, str(str(max+1)+ ": " + cndb.lview[max][0]))
    listboxx.pack(side="left")

    scroll.config(command=listboxx.yview)

    def delfdb():
        global logo
        global imagefile
        global photolabel
        cndb.getlist()
        resultex = listboxx.curselection()
        if not resultex:
            messagebox.showinfo('error','please, select data!', parent=delete_window)
        else:
            listindex = resultex[0]
            cndb.deletedata(listindex)
            listboxx.delete(listindex)
            cndb.getlist()
            totalcount = len(cndb.lview)
            listviewcount.set("total "+ str(totalcount))
            delete_window.destroy()
            try:
                fn = str(cndb.fn)
                os.remove('./image/' + fn + '.gif')
            except:
                pass

            if not cndb.lview:
                cndb.totalcount = 0
                cndb.animecount = 0
                cndb.listnumber = 0
                title_value.set('None')
                gen_value.set('None')
                pro_value.set('None')
                year_value.set('None')
                quarter_value.set('None')
                listviewcount.set("total "+ str(cndb.totalcount))
                ln_value.set(cndb.listnumber)
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
    for maxx in range(len(cndb.lview)):
        showlistbox.insert(maxx, str(str(maxx+1)+ ": " + cndb.lview[maxx][0]))
    showlistbox.pack(side="left")

    scroll2.config(command=showlistbox.yview)

    def gobutt():
        resultex2 = showlistbox.curselection()
        if not resultex2:
            messagebox.showinfo('error','please, select data!', parent=sal_window)
        else:
            cndb.animecount = resultex2[0]
            cndb.listnumber = cndb.animecount + 1
            cndb.sdata()
            title_value.set(str(cndb.a_title))
            gen_value.set(str(cndb.a_genre))
            pro_value.set(str(cndb.a_production))
            year_value.set(str(cndb.a_year))
            quarter_value.set(str(cndb.a_quarter))
            ln_value.set(cndb.listnumber)
            changeim()
            sal_window.destroy()

    def ModifyData():

        resultex3 = showlistbox.curselection()

        if not resultex3:
            modierror = messagebox.showinfo('error','please, select data!', parent=sal_window)
        else:
            cndb.animecount = resultex3[0]
            cndb.listnumber = cndb.animecount + 1
            cndb.sdata()
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
            mt_value.set(cndb.a_title)
            me1 = Entry(mod_window, relief=SUNKEN, textvariable=mt_value, width=26, font=normal_font)
            me1.grid(row=0,column=1)

            Label(mod_window, relief=RIDGE, text="장르", width=8, font=normal_font).grid(row=1,column=0)

            mg_value=StringVar()
            mg_value.set(cndb.a_genre)
            me2 = Entry(mod_window, relief=SUNKEN, textvariable=mg_value, width=26, font=normal_font)
            me2.grid(row=1,column=1)

            Label(mod_window, relief=RIDGE, text="제작사", width=8, font=normal_font).grid(row=2,column=0)

            mp_value=StringVar()
            mp_value.set(cndb.a_production)
            me3 = Entry(mod_window, relief=SUNKEN, textvariable=mp_value, width=26, font=normal_font)
            me3.grid(row=2,column=1)

            Label(mod_window, relief=RIDGE, text="연도", width=8, font=normal_font).grid(row=3,column=0)

            my_value=StringVar()
            my_value.set(cndb.a_year)
            me4 = Entry(mod_window, relief=SUNKEN, textvariable=my_value, width=26, font=normal_font)
            me4.grid(row=3,column=1)

            Label(mod_window, relief=RIDGE, text="분기", width=8, font=normal_font).grid(row=4,column=0)

            mq_value=StringVar()
            mq_value.set(cndb.a_quarter)
            me5 = Entry(mod_window, relief=SUNKEN, textvariable=mq_value, width=26, font=normal_font)
            me5.grid(row=4,column=1)

            def moddata():
                global logo
                global imagefile
                global photolabel
                mtn = str(mt_value.get())
                mgn = str(mg_value.get())
                mpn = str(mp_value.get())
                myn = str(my_value.get())
                mqn = str(mq_value.get())

                cndb.modidata(mtn,mgn,mpn,myn,mqn)
                messagebox.showinfo('updated!','수정되었습니다!', parent=mod_window)

                cndb.getlist()
                cndb.sdata()
                title_value.set(str(cndb.a_title))
                gen_value.set(str(cndb.a_genre))
                pro_value.set(str(cndb.a_production))
                year_value.set(str(cndb.a_year))
                quarter_value.set(str(cndb.a_quarter))
                ln_value.set(cndb.listnumber)
                imageid = cndb.fn
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
    export_window = Toplevel()
    export_window.title("Export")
    export_window.wm_iconbitmap('./image/myicon.ico')
    export_window.resizable(0,0)
    export_window.attributes('-topmost', 'true')
    export_window.grab_set()

    def excsv():
        cndb.getlistnoid()

        head_row = [('Title', 'Genre', 'Production', 'Year', 'Quarter')]

        with open('list.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(head_row)
            writer.writerows(cndb.lview)

        csvFile.close()
        export_window.destroy()
        messagebox.showinfo('done','csvfile is created!')

    def exxls():
        cndb.getlistnoid()
        df = DataFrame(data = cndb.lview, columns=['Title', 'Genre', 'Production', 'Year', 'Quarter'])
        df.index += 1
        df.to_excel('list.xls',index=True,header=True)
        export_window.destroy()
        messagebox.showinfo('done','xlsfile is created!')

    Label(export_window, text='export to csv file', font=large_font).grid(row=0, column=0, padx=5, pady=10)
    Label(export_window, text='export to xls file', font=large_font).grid(row=1, column=0, padx=5, pady=10)
    csvbutton = Button(export_window, text='EXPORT', font=large_font, state=NORMAL, command=excsv)
    csvbutton.grid(row=0, column=1, padx=5, pady=10)
    xlsbutton = Button(export_window, text='EXPORT', font=large_font, state=NORMAL, command=exxls)
    xlsbutton.grid(row=1, column=1, padx=5, pady=10)

    if not cndb.lview:
        csvbutton.configure(text='NO DATAS',state='disabled')
        xlsbutton.configure(text='NO DATAS',state='disabled')
    export_window.mainloop()


def matplotcanvas():
    if not cndb.lview:
        messagebox.showinfo("error", "데이터가 없습니다")
    else:
        chart_window = Toplevel()
        chart_window.title("chart")
        chart_window.wm_iconbitmap('./image/myicon.ico')
        chart_window.resizable(0,0)
        chart_window.attributes('-topmost','true')

        cndb.getlist()
        ch = Drawchart(chart_window)
        ch.draw_chart(cndb.lview, 1, "TOP5 장르", chart_window)

        def g_chart():
            ch.destroy_chart()
            ch.draw_chart(cndb.lview, 1, "TOP5 장르", chart_window)

        def p_chart():
            ch.destroy_chart()
            ch.draw_chart(cndb.lview, 2, "TOP5 제작사", chart_window)

        def y_chart():
            ch.destroy_chart()
            ch.draw_chart(cndb.lview, 3, "TOP5 연도", chart_window)

        g_button = Button(chart_window, text='GENRE', command = g_chart)
        g_button.grid(row=0, column=0, sticky ='nsew')
        p_button = Button(chart_window, text='PRODUCTION', command = p_chart)
        p_button.grid(row=0, column=1, sticky ='nsew')
        y_button = Button(chart_window, text='YEAR', command = y_chart)
        y_button.grid(row=0, column=2, sticky ='nsew')



        chart_window.mainloop()


def aboutmew():
    aboutme_window = Toplevel()
    aboutme_window.title("About me")
    aboutme_window.wm_iconbitmap('./image/myicon.ico')
    aboutme_window.resizable(0,0)
    aboutme_window.geometry("+150+100")
    aboutme_window.attributes('-topmost', 'true')
    Label(aboutme_window, text='made by. MSE\nvoll1212@naver.com', width=30, padx=5, pady=5).grid(row=0,columnspan=3, padx=5, pady=5)
    Label(aboutme_window, text='1.0.3 ver', width=30, padx=5, pady=5).grid(row=1,columnspan=3, padx=5, pady=5)
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
expmenu.add_command(label="export", command=exportw)
expmenu.add_command(label="chart", command=matplotcanvas)
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
    logo = PhotoImage(file=cndb.winkimg)
photolabel = Label(ff, image=logo)
photolabel.image = logo #항상 이미지가 나타날 수 있도록?
photolabel.grid(row=0, columnspan=4)

#define buttons
pvbt = Button(ff, text="Prev", width=23, command=prevanime, state='disabled')
pvbt.grid(row=1, column=0)

listviewcount=StringVar()
listviewcount.set("total "+ str(cndb.totalcount))
Label(ff, textvariable=listviewcount, width=10).grid(row=1, column=1)

ln_value=StringVar()
ln_value.set(cndb.listnumber)
Entry(ff, textvariable=ln_value, width=4).grid(row=1, column=2)

nxbt = Button(ff, text="Next", width=23, command=nextanime, state='disabled')
nxbt.grid(row=1, column=3)

if len(cndb.lview) > 0:
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
title_value.set(str(cndb.a_title))
Entry(sf, relief=SUNKEN, textvariable=title_value, width=20, font=large_font).grid(row=0, column=1, columnspan=4)

#show genre
gen_value=StringVar()
gen_value.set(str(cndb.a_genre))
Entry(sf, relief=SUNKEN, textvariable=gen_value, width=20, font=large_font).grid(row=1, column=1)

#show production
pro_value=StringVar()
pro_value.set(str(cndb.a_production))
Entry(sf, relief=SUNKEN, textvariable=pro_value, width=20, font=large_font).grid(row=2, column=1)

#show year
year_value=StringVar()
year_value.set(str(cndb.a_year))
Entry(sf, relief=SUNKEN, textvariable=year_value, width=20, font=large_font).grid(row=3, column=1)

#show quarter
quarter_value=StringVar()
quarter_value.set(str(cndb.a_quarter))
Entry(sf, relief=SUNKEN, textvariable=quarter_value, width=20, font=large_font).grid(row=4, column=1)
#######################################################################################################################


#remain in the event loop until close the window

window.mainloop()
cndb.conn.close()
