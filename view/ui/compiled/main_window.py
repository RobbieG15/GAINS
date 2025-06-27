# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.action_new_project = QAction(MainWindow)
        self.action_new_project.setObjectName(u"action_new_project")
        self.action_import_image = QAction(MainWindow)
        self.action_import_image.setObjectName(u"action_import_image")
        self.action_open_project = QAction(MainWindow)
        self.action_open_project.setObjectName(u"action_open_project")
        self.action_save_project = QAction(MainWindow)
        self.action_save_project.setObjectName(u"action_save_project")
        self.action_save_as = QAction(MainWindow)
        self.action_save_as.setObjectName(u"action_save_as")
        self.action_exit = QAction(MainWindow)
        self.action_exit.setObjectName(u"action_exit")
        self.actions_annotations = QAction(MainWindow)
        self.actions_annotations.setObjectName(u"actions_annotations")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menu_file.addAction(self.action_new_project)
        self.menu_file.addAction(self.action_open_project)
        self.menu_file.addAction(self.action_save_project)
        self.menu_file.addAction(self.action_save_as)
        self.menu_file.addAction(self.action_exit)
        self.menuEdit.addAction(self.action_import_image)
        self.menuView.addAction(self.actions_annotations)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_new_project.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.action_import_image.setText(QCoreApplication.translate("MainWindow", u"Import Image", None))
#if QT_CONFIG(tooltip)
        self.action_import_image.setToolTip(QCoreApplication.translate("MainWindow", u"Import a Whole Slide Image (.svs)", None))
#endif // QT_CONFIG(tooltip)
        self.action_open_project.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.action_save_project.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.action_save_as.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
        self.action_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actions_annotations.setText(QCoreApplication.translate("MainWindow", u"Annotations", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

