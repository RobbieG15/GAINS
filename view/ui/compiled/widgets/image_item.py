# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'image_item.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(300, 102)
        Form.setMinimumSize(QSize(300, 0))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.image_box = QGroupBox(Form)
        self.image_box.setObjectName(u"image_box")
        self.verticalLayout_3 = QVBoxLayout(self.image_box)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.preview_widget = QWidget(self.image_box)
        self.preview_widget.setObjectName(u"preview_widget")

        self.horizontalLayout.addWidget(self.preview_widget)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.path_label = QLabel(self.image_box)
        self.path_label.setObjectName(u"path_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.path_label.sizePolicy().hasHeightForWidth())
        self.path_label.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.path_label)

        self.metadata_label = QLabel(self.image_box)
        self.metadata_label.setObjectName(u"metadata_label")

        self.verticalLayout_2.addWidget(self.metadata_label)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.view_image_btn = QPushButton(self.image_box)
        self.view_image_btn.setObjectName(u"view_image_btn")

        self.horizontalLayout.addWidget(self.view_image_btn)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.image_box)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.image_box.setTitle(QCoreApplication.translate("Form", u"Image Name", None))
        self.path_label.setText(QCoreApplication.translate("Form", u"Save Path", None))
        self.metadata_label.setText(QCoreApplication.translate("Form", u"Metadata", None))
        self.view_image_btn.setText(QCoreApplication.translate("Form", u"View Image", None))
    # retranslateUi

