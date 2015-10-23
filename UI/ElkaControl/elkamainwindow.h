#ifndef ELKAMAINWINDOW_H
#define ELKAMAINWINDOW_H

#include <QMainWindow>

namespace Ui {
class ElkaMainWindow;
}

class ElkaMainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit ElkaMainWindow(QWidget *parent = 0);
    ~ElkaMainWindow();

private:
    Ui::ElkaMainWindow *ui;
};

#endif // ELKAMAINWINDOW_H
