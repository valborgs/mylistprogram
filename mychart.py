# -*- coding: utf-8 -*-
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import rc, font_manager


class Drawchart():
    def __init__(self, masterwindow):
        self.fontpath = "./NanumGothic.ttf"
        self.font_name = font_manager.FontProperties(fname=self.fontpath).get_name()
        self.counts = dict()
        self.sizes= []
        self.subjects = ()
        self.colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'orange']
        self.f = Figure(figsize=(5,5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.f, master = masterwindow)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, columnspan=3)

    def draw_chart(self, list, num, titlename, masterwindow):
        self.canvas.get_tk_widget().destroy()
        self.counts = dict()
        self.sizes= []
        self.subjects = ()
        rc('font', family=self.font_name)

        for g in list:#list에cndb.lview넣기
            gs = g[int(num)]#장르는 1, 제작사는 2, 연도는 3 num에다 넣기
            self.counts[gs] = self.counts.get(gs, 0) + 1

        for subject, size in self.counts.items():
            self.subjects = self.subjects + (subject, )
            self.sizes.append(size)
        self.sizes = self.sizes[:5]
        self.subjects = self.subjects[:5]
        #explode = (0.1, 0, 0, 0)  # explode 1st slice

        self.f = Figure(figsize=(5,5), dpi=100)
        a = self.f.add_subplot(111)
        a.set_title(titlename)
        a.pie(self.sizes, labels = self.subjects, colors = self.colors, autopct='%1.1f%%', shadow=True, startangle=140)

        self.canvas = FigureCanvasTkAgg(self.f, master = masterwindow)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, columnspan=3)

    def destroy_chart(self):
        self.canvas.get_tk_widget().destroy()
