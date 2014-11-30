#!/usr/bin/python3
# -*- coding. utf-8 -*-

import curses
from curses import wrapper
from curses.textpad import rectangle

from urllib import request
from html import parser
from json import loads

class QioApp:
    def __init__(self, stdscreen):
        self.data = []
        self.stdscr = stdscreen

    def initialize(self):
        # inialize curses env
        #self.stdscr = curses.initscr()
        if curses.has_colors():
            curses.start_color()

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        # turn off automatic echoing
        curses.noecho()

        # react keyboard immediatly, ie. cbreak mode
        curses.cbreak()

        self.stdscr.keypad(True)

        self.stdscr.clear()

        


        self.ikkuna()

        return True
    
    
    def get_new_joke(self):
        response = request.urlopen("http://api.icmb.com/jokes/random")
        ur = response.read()
        joke_json = loads(ur)
        #joke_json = loads(request.urlopen("http://api.icmb.com/jokes/random").read())
        return parser.HTMLParser().unescape(joke_json['value']['joke']).encode('utf-8')


    def ikkuna(self):
        
        self.stdscr.addstr(' QUITOOL v 0.0.1 (c) Tommi Rintala, Delektre Oy 2014', curses.A_REVERSE)
        self.stdscr.chgat(-1, curses.A_REVERSE)

        self.stdscr.addstr(curses.LINES-1,2,"Press 'R' to request a new quote, 'x' for exit")
        self.quote_window = curses.newwin(curses.LINES-2, curses.COLS, 1, 0)
        self.quote_text_window = self.quote_window.subwin(curses.LINES-6, curses.COLS-4, 3, 2)
        self.quote_window.box()

        self.stdscr.noutrefresh()
        self.quote_window.noutrefresh()
        curses.doupdate()
        # rectangle(self.stdscr, 0, 0, curses.LINES-1, curses.COLS-1)

        #self.stdscr.addstr(0,0,"QUITOOL v 0.0.1", curses.color_pair(1))
#        self.stdscr.addstr(curses.LINES-1, curses.COLS / 3, "press 'x' to exit applicatoin", curses.color_pair(0))
        
    def terminate(self):
        curses.nocbreak()
        self.stdscr.keypad(True)
        curses.echo()

        curses.curs_set(1)
        curses.endwin()
        return True

    def run(self):
        #loop here

        while True:
            c = self.quote_window.getch()

            if ( c == ord('r') or c == ord('R')):
                 self.quote_text_window.clear()
                 self.quote_text_window.addstr("Getting quote...", curses.color_pair(3))
                 self.quote_text_window.refresh()
                 self.quote_text_window.clear()
                 self.quote_text_window.addstr(self.get_new_joke())
            elif c == ord('q') or c == ord('x'):
                break;
            
            # refresh window stack from bottom to up
            self.stdscr.noutrefresh()
            self.quote_window.notefresh()
            self.quote_text_window.notrefresh()
            curses.doupdate();
        return True


def runapp(stdscr):
    app = QioApp(stdscr)
    app.initialize()
    app.run()
    app.terminate()


#if __name__ == "__main__":

wrapper(runapp)
