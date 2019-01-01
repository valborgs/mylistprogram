# -*- coding: utf-8 -*-
import sqlite3


class ConDB():
    def __init__(self):
        self.lview = []
        self.totalcount = 0
        self.listnumber = 0
        self.animecount = 0
        self.a_title = 'None'
        self.a_genre = 'None'
        self.a_production = 'None'
        self.a_year = 'None'
        self.a_quarter = 'None'
        self.fn = 0

    def conndb(self):
        print("connecting anime DB...")
        self.conn = sqlite3.connect('animelist.sqlite')
        self.cur = self.conn.cursor()


    def createtable(self):
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Title (
            t_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL,
            t_name TEXT UNIQUE,
            genre_id INTEGER,
            production_id INTEGER,
            year_id INTEGER,
            quarter_id INTEGER
        )''')
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Genre (
            id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL,
            g_name TEXT UNIQUE
        )''')
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Production (
            id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL,
            p_name TEXT UNIQUE
        )''')
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Year (
            id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL,
            year TEXT UNIQUE
        )''')
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Quarter (
            id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL,
            quarter TEXT UNIQUE
        )''')
        self.bef = self.cur.execute('''SELECT quarter FROM Quarter''').fetchall()
        if len(self.bef) == 0:
            for x in range(1,5):
                self.cur.execute(
                '''INSERT OR IGNORE INTO Quarter (quarter) VALUES (?)''', (x,)
                )
        self.conn.commit()

    def loaddata(self):
        print("loading datas from DB...")
        self.cur.execute('''
        SELECT t_name, g_name, p_name, year, quarter, t_id
        FROM Title
        JOIN Genre ON Title.genre_id = Genre.id
        JOIN Production ON Title.production_id = Production.id
        JOIN Year ON Title.year_id = Year.id
        JOIN Quarter ON Title.quarter_id = Quarter.id
        ''')
        self.lview = self.cur.fetchall()
        if self.lview:
            self.totalcount = len(self.lview)
            self.gofirstdata()
        else:
            pass

    def getlist(self):
        self.cur.execute('''
        SELECT t_name, g_name, p_name, year, quarter, t_id
        FROM Title
        JOIN Genre ON Title.genre_id = Genre.id
        JOIN Production ON Title.production_id = Production.id
        JOIN Year ON Title.year_id = Year.id
        JOIN Quarter ON Title.quarter_id = Quarter.id
        ''')
        self.lview = self.cur.fetchall()

    def getlistnoid(self):
        self.cur.execute('''
        SELECT t_name, g_name, p_name, year, quarter
        FROM Title
        JOIN Genre ON Title.genre_id = Genre.id
        JOIN Production ON Title.production_id = Production.id
        JOIN Year ON Title.year_id = Year.id
        JOIN Quarter ON Title.quarter_id = Quarter.id
        ''')
        self.lview = self.cur.fetchall()

    def gofirstdata(self):
        self.listnumber = 1
        self.animecount = 0
        self.a_title = self.lview[0][0]
        self.a_genre = self.lview[0][1]
        self.a_production = self.lview[0][2]
        self.a_year = self.lview[0][3]
        self.a_quarter = self.lview[0][4]

    def sdata(self):
        x = self.lview[self.animecount]
        self.a_title = x[0]
        self.a_genre = x[1]
        self.a_production = x[2]
        self.a_year = x[3]
        self.a_quarter = x[4]
        self.fn = x[5]

    def nextdata(self):
        self.animecount += 1
        self.listnumber += 1

    def prevdata(self):
        self.animecount -= 1
        self.listnumber -= 1

    def adddata(self, iqn, iyn, ipn, ign, itn):
        f_quarter = self.cur.execute("SELECT id From Quarter WHERE quarter = ?", [iqn]).fetchone()[0]
        self.cur.execute('''INSERT OR IGNORE INTO  Year (year) VALUES (?)''', (iyn,))
        f_year = self.cur.execute("SELECT id From Year WHERE year = ?", [iyn]).fetchone()[0]
        self.cur.execute('''INSERT OR IGNORE INTO Production (p_name) VALUES (?)''', (ipn,))
        f_production = self.cur.execute("SELECT id From Production WHERE p_name = ?", [ipn]).fetchone()[0]
        self.cur.execute('''INSERT OR IGNORE INTO Genre (g_name) VALUES (?)''', (ign,))
        f_genre = self.cur.execute("SELECT id From Genre WHERE g_name = ?", [ign]).fetchone()[0]
        self.cur.execute('''INSERT INTO Title (t_name, genre_id, production_id, year_id, quarter_id ) VALUES (?,?,?,?,?)''', (itn, f_genre, f_production, f_year, f_quarter))
        self.conn.commit()

    def deletedata(self, listindex):
        bfn = self.lview[listindex]
        self.fn = bfn[5]#선택한애니메이션의id값
        self.cur.execute('''DELETE FROM Title WHERE t_id=?''',(self.fn,))
        self.conn.commit()

    def modidata(self, mtn, mgn, mpn, myn, mqn):
        try:
            self.cur.execute('''SELECT id FROM Genre WHERE g_name =?''',(mgn,))
            mgn2 = self.cur.fetchone()[0]
        except:
            self.cur.execute('''INSERT OR IGNORE INTO Genre (g_name) VALUES (?)''', (mgn,))
            self.cur.execute('''SELECT id FROM Genre WHERE g_name =?''',(mgn,))
            mgn2 = self.cur.fetchone()[0]

        try:
            self.cur.execute('''SELECT id FROM Production WHERE p_name =?''',(mpn,))
            mpn2 = self.cur.fetchone()[0]
        except:
            self.cur.execute('''INSERT OR IGNORE INTO Production (p_name) VALUES (?)''', (mpn,))
            self.cur.execute('''SELECT id FROM Production WHERE p_name =?''',(mpn,))
            mpn2 = self.cur.fetchone()[0]

        try:
            self.cur.execute('''SELECT id FROM Year WHERE year =?''',(myn,))
            myn2 = self.cur.fetchone()[0]
        except:
            self.cur.execute('''INSERT OR IGNORE INTO  Year (year) VALUES (?)''', (myn,))
            self.cur.execute('''SELECT id FROM Year WHERE year =?''',(myn,))
            myn2 = self.cur.fetchone()[0]

        self.cur.execute('''SELECT id FROM Quarter WHERE quarter =?''',(mqn,))
        mqn2 = self.cur.fetchone()[0]

        self.cur.execute('''UPDATE Title SET t_name = ? WHERE t_name = ?''',(mtn,self.a_title))
        self.cur.execute('''UPDATE Title SET genre_id = ? WHERE t_name = ?''',(mgn2,self.a_title))
        self.cur.execute('''UPDATE Title SET production_id = ? WHERE t_name = ?''',(mpn2,self.a_title))
        self.cur.execute('''UPDATE Title SET year_id = ? WHERE t_name = ?''',(myn2,self.a_title))
        self.cur.execute('''UPDATE Title SET quarter_id = ? WHERE t_name = ?''',(mqn2,self.a_title))

        self.conn.commit()


x = ConDB()
x.conndb()
x.createtable()
x.loaddata()
