import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton)
from PyQt5.QtCore import QRect, QPropertyAnimation

class AppDemo(QWidget):
	def __init__(self):
		super().__init__()
		self.baseHeight = 50
		self.extendedHeight = 300
		self.rect = QRect(600, 300, 300, self.baseHeight)
		self.setGeometry(self.rect)

		self.btn = QPushButton('Expand', self)
		self.btn.move(20, 15)
		self.btn.clicked.connect(self.resizeWindow)

	def resizeWindow(self):
		currentHeight = self.height()

		if self.baseHeight == currentHeight:
			baseHeight = self.baseHeight
			extendedHeight = self.extendedHeight
			self.btn.setText('Expand')
		else:
			baseHeight = self.extendedHeight
			extendedHeight = self.baseHeight
			self.btn.setText('Shrink')

		self.animation = QPropertyAnimation(self, b'geometry')
		self.animation.setDuration(200)
		self.animation.setStartValue(QRect(600, 300, 300, baseHeight))
		self.animation.setEndValue(QRect(600, 300, 300, extendedHeight))
		self.animation.start()

if __name__ == '__main__':
	app = QApplication(sys.argv)

	demo = AppDemo()
	demo.show()

	sys.exit(app.exec_())