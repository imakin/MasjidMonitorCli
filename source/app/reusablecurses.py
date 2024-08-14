"""
@author: Muhammad Izzulmakin
@date: 2024-08
"""
import curses
import pyfiglet

class ReusableCurses():
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.log = self.log_dont

    def log_dont(self,t):
        pass

    def text_mid(self, text, y,x, scale=1, font="fonts/ansi_regular"):
        """
        Displays text centered on the screen at the given y, x coordinates.
        
        Args:
            text (str): The text to display.
            y (int): The y-coordinate of the center position.
            x (int): The x-coordinate of the center position.
            scale (int, optional): The scale factor for the text. Defaults to 1.
            font (str, optional): The font to use for the text. Defaults to "fonts/ansi_regular".
                means using file in current directory: './fonts/ansi_regular.flf'
        """
        stdscr = self.stdscr
        height, width = stdscr.getmaxyx()

        t = pyfiglet.figlet_format(text, font=font)
        # Scale the figlet text
        while True:
            scaled_text = []
            longest = 0
            for line in t.splitlines():
                scaled_line = ''.join([char * scale for char in line]) #multi column per char
                if len(scaled_line)>longest:
                    longest = len(scaled_line)
                for _ in range(scale): #multi row per char
                    scaled_text.append(scaled_line)
            
            if longest>width:
                scale -= 1
                continue

            if len(scaled_text)>height:
                scale -= 1
                continue
            
            ystart = y-(len(scaled_text)//2)
            yend = ystart+len(scaled_text)
            xstart = x-(len(scaled_text[0])//2)
            xend = xstart+longest

            if (ystart<0):
                ystart = 0
            if xstart<0:
                xstart = 0
            
            if yend>=height:
                ystart = height-len(scaled_text) - 1
            if xend>=width:
                xstart = width-longest - 1
            
            break
        
        self.log(f"yend: {yend}, height: {height}, xend:{xend}, width:{width}")

        for i,line in enumerate(scaled_text):
            stdscr.addstr(i+ystart, xstart, line)



# Example usage
if __name__ == "__main__":
    import curses

    def main(stdscr):
        reusable_curses = ReusableCurses(stdscr)
        reusable_curses.text_mid("Hello", 10, 30)
        stdscr.refresh()
        stdscr.getch()

    curses.wrapper(main)