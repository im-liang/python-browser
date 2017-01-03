from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import *

import sys

class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setWindowTitle('My Browser')

		self.setWindowIcon(QIcon('icon/logo.png'))
		self.show()


		self.tabs = QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
		self.tabs.currentChanged.connect(self.current_tab_changed)
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.close_current_tab)

		self.add_new_tab(QUrl('http://shiyanlou.com'), 'Homepage')

		self.setCentralWidget(self.tabs)

		new_tab_action = QAction(QIcon('icon/add_page.png'), 'New Page', self)
		new_tab_action.triggered.connect(self.add_new_tab)



		navigation_bar = QToolBar('Navigation')

		navigation_bar.setIconSize(QSize(16, 16))
		self.addToolBar(navigation_bar)


		back_button = QAction(QIcon('icon/back.png'), 'Back', self)
		next_button = QAction(QIcon('icon/next.png'), 'Forward', self)
		stop_button = QAction(QIcon('icon/cross.png'), 'stop', self)
		reload_button = QAction(QIcon('icon/renew.png'), 'reload', self)

		back_button.triggered.connect(self.tabs.currentWidget().back)
		next_button.triggered.connect(self.tabs.currentWidget().forward)
		stop_button.triggered.connect(self.tabs.currentWidget().stop)
		reload_button.triggered.connect(self.tabs.currentWidget().reload)

		navigation_bar.addAction(back_button)
		navigation_bar.addAction(next_button)
		navigation_bar.addAction(stop_button)
		navigation_bar.addAction(reload_button)


		self.urlbar = QLineEdit()

		self.urlbar.returnPressed.connect(self.navigate_to_url)

		navigation_bar.addSeparator()
		navigation_bar.addWidget(self.urlbar)

	

	def navigate_to_url(self):
		q = QUrl(self.urlbar.text())
		if q.scheme() == '':
			q.setScheme('http')
		self.tabs.currentWidget().setUrl(q)

	def renew_urlbar(self, q, browser=None):

		if browser != self.tabs.currentWidget():
			return

		self.urlbar.setText(q.toString())
		self.urlbar.setCursorPosition(0)

	def add_new_tab(self, qurl=QUrl(''), label='Blank'):
		browser = QWebView()
		browser.setUrl(qurl)
		i = self.tabs.addTab(browser, label)

		self.tabs.setCurrentIndex(i)
		
		browser.urlChanged.connect(lambda qurl, browser=browser: self.renew_urlbar(qurl, browser))
		
		browser.loadFinished.connect(lambda _, i=i, browser=browser: 
			self.tabs.setTabText(i, browser.page().mainFrame().title()))

	def tab_open_doubleclick(self, i):
		if i == -1:
			self.add_new_tab()

	def current_tab_changed(self, i):
		qurl = self.tabs.currentWidget().url()
		self.renew_urlbar(qurl, self.tabs.currentWidget())

	def close_current_tab(self, i):
		if self.tabs.conut() < 2:
			return
		self.tabs.removeTab(i)

		
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
