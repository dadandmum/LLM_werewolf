# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'llm_tool_raw.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 774)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 10, 291, 201))
        self.AgentLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.AgentLayout.setObjectName(u"AgentLayout")
        self.AgentLayout.setContentsMargins(0, 0, 0, 0)
        self.horizon_agent = QHBoxLayout()
        self.horizon_agent.setObjectName(u"horizon_agent")
        self.agentLabel = QLabel(self.verticalLayoutWidget)
        self.agentLabel.setObjectName(u"agentLabel")

        self.horizon_agent.addWidget(self.agentLabel)

        self.agentCombo = QComboBox(self.verticalLayoutWidget)
        self.agentCombo.setObjectName(u"agentCombo")

        self.horizon_agent.addWidget(self.agentCombo)


        self.AgentLayout.addLayout(self.horizon_agent)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.agentTypeLabel = QLabel(self.verticalLayoutWidget)
        self.agentTypeLabel.setObjectName(u"agentTypeLabel")

        self.horizontalLayout.addWidget(self.agentTypeLabel)

        self.agentInfoCombo = QComboBox(self.verticalLayoutWidget)
        self.agentInfoCombo.setObjectName(u"agentInfoCombo")

        self.horizontalLayout.addWidget(self.agentInfoCombo)


        self.AgentLayout.addLayout(self.horizontalLayout)

        self.agentTypeLabel_4 = QLabel(self.verticalLayoutWidget)
        self.agentTypeLabel_4.setObjectName(u"agentTypeLabel_4")
        self.agentTypeLabel_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.AgentLayout.addWidget(self.agentTypeLabel_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.agentInfo = QPlainTextEdit(self.verticalLayoutWidget)
        self.agentInfo.setObjectName(u"agentInfo")
        self.agentInfo.setLineWidth(1)

        self.horizontalLayout_2.addWidget(self.agentInfo)


        self.AgentLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(300, 10, 491, 471))
        self.taskLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.taskLayout.setObjectName(u"taskLayout")
        self.taskLayout.setContentsMargins(0, 0, 0, 0)
        self.horizon_agent_2 = QHBoxLayout()
        self.horizon_agent_2.setObjectName(u"horizon_agent_2")
        self.taskLabel = QLabel(self.verticalLayoutWidget_2)
        self.taskLabel.setObjectName(u"taskLabel")

        self.horizon_agent_2.addWidget(self.taskLabel)

        self.taskCombo = QComboBox(self.verticalLayoutWidget_2)
        self.taskCombo.setObjectName(u"taskCombo")

        self.horizon_agent_2.addWidget(self.taskCombo)


        self.taskLayout.addLayout(self.horizon_agent_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.TaskParameterLabel = QLabel(self.verticalLayoutWidget_2)
        self.TaskParameterLabel.setObjectName(u"TaskParameterLabel")

        self.horizontalLayout_3.addWidget(self.TaskParameterLabel)


        self.taskLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.taskParameterText = QPlainTextEdit(self.verticalLayoutWidget_2)
        self.taskParameterText.setObjectName(u"taskParameterText")
        self.taskParameterText.setLineWidth(1)

        self.horizontalLayout_4.addWidget(self.taskParameterText)


        self.taskLayout.addLayout(self.horizontalLayout_4)

        self.FullTaskLabel = QLabel(self.verticalLayoutWidget_2)
        self.FullTaskLabel.setObjectName(u"FullTaskLabel")
        self.FullTaskLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.taskLayout.addWidget(self.FullTaskLabel)

        self.TaskFullText = QPlainTextEdit(self.verticalLayoutWidget_2)
        self.TaskFullText.setObjectName(u"TaskFullText")
        self.TaskFullText.setLineWidth(1)

        self.taskLayout.addWidget(self.TaskFullText)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 505, 781, 211))
        self.result = QVBoxLayout(self.verticalLayoutWidget_3)
        self.result.setObjectName(u"result")
        self.result.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.modelLabel = QLabel(self.verticalLayoutWidget_3)
        self.modelLabel.setObjectName(u"modelLabel")

        self.horizontalLayout_5.addWidget(self.modelLabel, 0, Qt.AlignmentFlag.AlignRight)

        self.modelCombo = QComboBox(self.verticalLayoutWidget_3)
        self.modelCombo.setObjectName(u"modelCombo")
        self.modelCombo.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_5.addWidget(self.modelCombo, 0, Qt.AlignmentFlag.AlignLeft)


        self.result.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.confirmButton = QPushButton(self.verticalLayoutWidget_3)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setMaximumSize(QSize(250, 16777215))
        self.confirmButton.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.confirmButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.confirmButton.setAutoFillBackground(False)
        self.confirmButton.setAutoDefault(False)

        self.horizontalLayout_7.addWidget(self.confirmButton)


        self.result.addLayout(self.horizontalLayout_7)

        self.resultLabel = QLabel(self.verticalLayoutWidget_3)
        self.resultLabel.setObjectName(u"resultLabel")
        self.resultLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.result.addWidget(self.resultLabel)

        self.resultText = QPlainTextEdit(self.verticalLayoutWidget_3)
        self.resultText.setObjectName(u"resultText")
        self.resultText.setEnabled(True)

        self.result.addWidget(self.resultText)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.confirmButton.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.agentLabel.setText(QCoreApplication.translate("MainWindow", u"Agent", None))
        self.agentTypeLabel.setText(QCoreApplication.translate("MainWindow", u"InfoType", None))
        self.agentTypeLabel_4.setText(QCoreApplication.translate("MainWindow", u"AgentInfo", None))
        self.taskLabel.setText(QCoreApplication.translate("MainWindow", u"Task", None))
        self.TaskParameterLabel.setText(QCoreApplication.translate("MainWindow", u"Parameter", None))
        self.FullTaskLabel.setText(QCoreApplication.translate("MainWindow", u"Full Prompt", None))
        self.modelLabel.setText(QCoreApplication.translate("MainWindow", u"Model", None))
        self.confirmButton.setText(QCoreApplication.translate("MainWindow", u"Confirm", None))
        self.resultLabel.setText(QCoreApplication.translate("MainWindow", u"Result", None))
    # retranslateUi

