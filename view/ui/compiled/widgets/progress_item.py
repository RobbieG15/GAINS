# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progress_item.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(300, 108)
        Form.setMinimumSize(QSize(300, 0))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.status_box = QGroupBox(Form)
        self.status_box.setObjectName(u"status_box")
        self.verticalLayout_2 = QVBoxLayout(self.status_box)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.status_label = QLabel(self.status_box)
        self.status_label.setObjectName(u"status_label")

        self.verticalLayout_2.addWidget(self.status_label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.progress_bar = QProgressBar(self.status_box)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.horizontalLayout.addWidget(self.progress_bar)

        self.kill_btn = QPushButton(self.status_box)
        self.kill_btn.setObjectName(u"kill_btn")

        self.horizontalLayout.addWidget(self.kill_btn)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.status_box)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.status_box.setTitle(QCoreApplication.translate("Form", u"Name", None))
        self.status_label.setText(QCoreApplication.translate("Form", u"Status", None))
        self.kill_btn.setText(QCoreApplication.translate("Form", u"Kill", None))
    # retranslateUi

