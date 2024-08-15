import curses
import time
import json
from datetime import (
    datetime,
    timedelta,
)

import reusablecurses
from config import Const
from log import log_once

class Abstract():pass

class App(reusablecurses.ReusableCurses):
    closest_prev = object()
    closest_next = object()

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.log = log_once
        self.freq = 2 # Hz
        with open("data.json") as f:
            data = f.read()
            self.jadwal = json.loads(data)
        self.run()

    def run(self):
        stdscr = self.stdscr
        stdscr.timeout(1000//self.freq)
        key = None
        font = "ANSI Regular"

        while True:
            
            stdscr.clear()

            # Get the number of rows and columns
            height, width = stdscr.getmaxyx()
            halfheight = height//2
            halfwidth = width//2

            # Generate large text using pyfiglet with different fonts
            
            current_time = self.datetime_get_now()
            day_of_the_week = current_time.weekday()
            current_second = str(current_time.second).zfill(2)
            
            colon = '.' if (current_time.second%2)==0 else ':'
            current_time = f"{str(current_time.hour).zfill(2)}{colon}{str(current_time.minute).zfill(2)}"
        
            prev = {
                ['seconds', 'jadwal', 'name'][i]:v
                for i,v in enumerate(self.get_closest(self.closest_prev))
            }
            next = {
                ['seconds', 'jadwal', 'name'][i]:v
                for i,v in enumerate(self.get_closest(self.closest_next))
            }

            curtime = f"{str((next['seconds']//60)%60).zfill(2)}:{str(next['seconds']%60).zfill(2)}"
            if int(next['seconds']/3600)>0:
                curtime = f"{str(next['seconds']//3600).zfill(2)}:{curtime}"



            try:
                self.text_mid(f"{current_time}", halfheight, width//3, scale=3, font='fonts/ansi_regular')
            except:pass
            try:
                self.text_mid(
                    f"{next['name']} -{curtime}",
                    3*(height//4),
                    width//3,
                    scale=1,
                    font="fonts/maxiwi"
                )
            except:pass


            stdscr.refresh()
            newkey = stdscr.getch() #read key press until timeout
            if newkey != -1:
                key = newkey


    datetime_adjust_enabled = True
    def datetime_get_now(self):
        """
        to support mocking
        e.g.: return datetime.datetime(year=2024, month=6, day=10, hour=16, minute=10, second=50)
        """
        if self.datetime_adjust_enabled:
            d = 0
            try:
                with open('DEBUG_TIMEDELTA', 'r') as f:
                    d = int(f.read())
            except:
                self.datetime_adjust_enabled = False
                d = 0
            return datetime.now() + timedelta(seconds=d)
        else:
            return datetime.now()



    def get_closest(self, prev_or_next):
        """
        get the closest jadwal to current time which was previous passed/upcoming
        @param prev_or_next: 
                    either self.closest_prev for closest passed time 
                    or self.closest_next for closest upcoming time
        """
        if prev_or_next not in [self.closest_next, self.closest_prev]:
            raise ValueError("get_closest expect prev_or_next to be self.closest_next or self.closest_prev")
        dt = self.datetime_get_now()
        year = str(dt.year)
        month = Const.months[dt.month]
        next_month = Const.get_month(dt.month+1)
        prev_month = Const.get_month(dt.month-1)
        
        day = str(dt.day)
        hour = dt.hour
        minute = dt.minute
        second = dt.second
        current_time_value = (hour*60*60)+(minute*60)+second
        
        closest = None
        gaps = []
        jadwals = []
        prayer_names = []
        for pray in self.jadwal["2024"][month][day]:
            t = self.jadwal["2024"][month][day][pray].split(":")
            h = int(t[0])
            m = int(t[1])
            v = h*60*60 + m*60
            gap = 0
            if prev_or_next==self.closest_next:
                gap = v-current_time_value
            elif prev_or_next==self.closest_prev:
                gap = current_time_value-v
            if gap>=0:
                gaps.append(gap)
                prayer_names.append(pray)
                jadwals.append(self.jadwal["2024"][month][day][pray])
        
        if len(gaps)==0:
            #accross the day, when prev is yesterday isya, or next is tomorrow shubuh
            if prev_or_next==self.closest_next:
                try:
                    t = self.jadwal["2024"][month][str(int(day)+1)]["shubuh"].split(":")
                except KeyError:
                    t = self.jadwal["2024"][next_month]["1"]["shubuh"].split(":")
                h = int(t[0])
                m = int(t[1])
                v = h*60*60 + m*60
                gap = (24*60*60)-current_time_value+v
                gaps.append(gap)
                prayer_names.append("shubuh")
                try:
                    jadwals.append(self.jadwal["2024"][month][str(int(day)+1)]["shubuh"])
                except KeyError:
                    jadwals.append(self.jadwal["2024"][next_month]["1"]["shubuh"])
                #~ masjidmonitor_log.info("esok")
            elif prev_or_next==self.closest_prev:
                try:
                    t = self.jadwal["2024"][month][str(int(day)-1)]["isya"].split(":")
                except KeyError:
                    days = [int(n) for n in self.jadwal["2024"][prev_month].keys()]
                    days.sort()
                    last_day = str(days[-1])
                    t = self.jadwal["2024"][prev_month][last_day]["isya"].split(":")
                h = int(t[0])
                m = int(t[1])
                v = h*60*60 + m*60
                gap = current_time_value + (24*60*60)-v
                gaps.append(gap)
                prayer_names.append("isya")
                
                try:
                    jadwals.append(self.jadwal["2024"][month][str(int(day)-1)]["isya"])
                except KeyError:
                    days = [int(n) for n in self.jadwal["2024"][prev_month].keys()]
                    days.sort()
                    last_day = str(days[-1])
                    jadwals.append(self.jadwal["2024"][prev_month][last_day]["isya"])
                
                #~ masjidmonitor_log.info("kmrn")                              #~ masjidmonitor_log.info("kmrn")
        gap = min(gaps)
        i = gaps.index(gap)
        #~ gap = gaps[0]
        #~ for g in gaps:
            
        jadwal = jadwals[i]
        #~ masjidmonitor_log.info("GET CLOSEST next?{}. gaps: {}, jadwals: {}, names: {}".format(prev_or_next==self.closest_next, gaps,jadwals,prayer_names))
        prayer_name = prayer_names[i]
        try:
            return gap,jadwal,prayer_name.decode("utf-8")
        except AttributeError:#python3 prayer_name is str object
            return gap,jadwal,prayer_name
            
    



def main(stdscr):
    app = App(stdscr)

if __name__=="__main__":
    curses.wrapper(main)
