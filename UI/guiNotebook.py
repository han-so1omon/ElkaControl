from gi.repository import Gtk

class GuiWindow(Gtk.Window):
  def __init__(self):
    Gtk.Window.__init__(self, title="ElkaControl Notebook")
    self.set_border_width(3)
    
    self.notebook = Gtk.Notebook()
    self.add(self.notebook)

    self.page1 = Gtk.Box()
    self.page1.set_border_width(10)
    self.page1.add(Gtk.Label('Welcome to ElkaControl'))
    self.notebook.append_page(self.page1, Gtk.Label('Main'))

    self.page2 = Gtk.Box()
    self.page2.set_border_width(10)
    self.page2.add(Gtk.Label('Parse Page'))
    self.notebook.append_page(self.page2, Gtk.Label('Parse'))

def guiMain():
  win = GuiWindow()
  win.connect('delete-event', Gtk.main_quit)
  win.show_all()
  Gtk.main()

if __name__ == '__main__':
  guiMain()
