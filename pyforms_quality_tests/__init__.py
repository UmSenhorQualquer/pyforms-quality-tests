import datetime, os, math, operator
from PIL import Image
from functools import reduce
from pyforms import BaseWidget
from PyQt4 import QtGui, QtCore


def makeLambdaFunc(func, **kwargs):
	return lambda: func(**kwargs)


def grab_screen(widget, outpath): 
	if isinstance(widget, (BaseWidget,QtGui.QMainWindow) ):
		win_id 	   = QtGui.QApplication.desktop().winId()
		x, y, w, h = widget.rect().x(), widget.rect().y(), widget.rect().width(), widget.rect().height()
		p = widget.mapToGlobal(QtCore.QPoint(x, y))
		x, y = p.x(), p.y()
		QtGui.QPixmap.grabWindow( win_id, x, y, w, h ).save(outpath, 'png')
	else:
		win_id = QtGui.QApplication.desktop().winId()
		QtGui.QPixmap.grabWindow( win_id ).save(outpath, 'png')


def take_screenshot(widget, outpath, timeout=500, wait=False): 
	QtCore.QTimer.singleShot(timeout, makeLambdaFunc(grab_screen, widget=widget, outpath=outpath))
	
	if wait:
		last_time = datetime.datetime.now()
		while ((datetime.datetime.now()-last_time).total_seconds() * 1000.0)<timeout:
			QtGui.QApplication.processEvents()


def sleep(timeout):
	last_time = datetime.datetime.now()
	while ((datetime.datetime.now()-last_time).total_seconds() * 1000.0)<timeout:
		QtGui.QApplication.processEvents()

def test_screenshot(data_path, filename):
	input_path 	= os.path.join(data_path, 'expected-data', filename)
	output_path = os.path.join(data_path, 'output-data', filename)

	image1 = Image.open(input_path)
	image2 = Image.open(output_path)
	h1 = image1.histogram()
	h2 = image2.histogram()
	rms = math.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
	return rms