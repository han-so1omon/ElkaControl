#include "elkamainwindow.h"
#include "ui_elkamainwindow.h"

ElkaMainWindow::ElkaMainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::ElkaMainWindow)
{
    ui->setupUi(this);
}

ElkaMainWindow::~ElkaMainWindow()
{
    delete ui;
}
