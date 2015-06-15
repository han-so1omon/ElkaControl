''' Use web browswer for gui '''
from Tkinter import *

class GUI(object):
    def __init__(self, master):
        frame = Frame(master)
        frame.pack() # Size widget to fit text and make self visible

        self.master = master

        # Objects to include:
        # Quit button
        # Run elka button (use radiobuttons for run methods)
        # Run radios button (debugging)
        # Display window for plots and graphs (seperate windows)
        # Display panel for active (filled and unfilled) data sets
        # Display panel for setting control parameters
        #       Radio parameters, input method, gains, reset, etc
        # Display for camera (optional)
        # Command line for manual command inputs (maybe use SciPy/NumPy to
        # execute functions from a callback inside of a command window widget

        # create a menu
        # FIXME do these need to be instance variables
        menu = Menu(root)
        root.config(menu=menu)

        filemenu = Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label="New", command=self.callback_ex)
        filemenu.add_command(label="Open...", command=self.callback_ex)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=frame.quit)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.callback_ex)

        # create a toolbar
        toolbar = Frame(root)
        toolbar.pack()
        self.new_b = Button(toolbar, text='New', width=6,
                command=self.callback_ex)
        self.new_b.pack(side=LEFT, padx=2, pady=2)

        self.open_b = Button(toolbar, text='Open', width=6,
                command=self.callback_ex)
        self.open_b.pack(side=LEFT, padx=2, pady=2)

        self.save_b = Button(toolbar, text='Save', width=6,
                command=self.callback_ex)
        self.save_b.pack(side=LEFT, padx=2, pady=2)
        
        # create status bar
        self.label = Label(frame, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    # If no params passed, simply clears status bar
    def set_status(self, format='', *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def callback_ex(self):
        print 'example callback'

    def open_file(self, filename):
        try:
            fp = open(filename)
            return fp
        except:
            tkMessageBox.showwarning(
                'Open file',
                'Cannot open {0}'.format(filename)
            )
            return

root = Tk() # one root per app
root.title('ELKA Base')
gui = GUI(root)
gui.set_status(args='waiting')
root.mainloop() # causes application window to appear
root.destroy()
