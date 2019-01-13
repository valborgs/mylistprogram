# -*- coding: utf-8 -*-
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import rc, font_manager
import numpy as np


class Drawchart():
    def __init__(self, masterwindow):
        self.fontpath = "./NanumGothic.ttf"
        self.font_name = font_manager.FontProperties(fname=self.fontpath).get_name()
        self.counts = dict()
        self.sizes= []
        self.subjects = ()
        self.colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'orange']
        self.f = Figure(figsize=(7,5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.f, master = masterwindow)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, columnspan=3, sticky='nsew')

    def destroy_chart(self):
        self.canvas.get_tk_widget().destroy()

    def draw_chart(self, list, num, titlename, masterwindow):
        self.counts = dict()
        self.sizes= []
        self.subjects = ()
        rc('font', family=self.font_name)

        for g in list:#list에cndb.lview넣기
            gs = g[int(num)]#장르는 1, 제작사는 2, 연도는 3 num에다 넣기
            if gs in self.counts:
                self.counts[gs] += 1
            else:
                self.counts[gs] = 1

        top_list = sorted(self.counts.items(), key=lambda x: x[1], reverse=True)
        top5_list = top_list[:5]
        for subject, size in top5_list:
            self.subjects = self.subjects + (subject, )
            self.sizes.append(size)

        #explode = (0.1, 0, 0, 0)  # explode 1st slice

        self.f = Figure(figsize=(7,5), dpi=100)
        a = self.f.add_subplot(111)
        a.set_title(titlename)

        def func(pct, allvals):
            absolute = int(pct/100.*np.sum(allvals))
            return "{:.1f}%\n({:d})".format(pct, absolute)

        a.pie(self.sizes, labels = self.subjects, colors = self.colors, autopct=lambda pct: func(pct, self.sizes), shadow=True, startangle=140)

        self.canvas = FigureCanvasTkAgg(self.f, master = masterwindow)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, columnspan=3)
