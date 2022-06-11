from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import os 
import pathlib
#trinh duyet
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.common.by import By
#trinh duyet

#nhan dien khuon mat
import _01_face_dataset
import _02_face_training
import _03_face_recognition
#nhan dien khuon mat
from datetime import date
#sql
import ketnoi
#sql
import audio
import shutil



# khai bao giao dien
ui_main,_ = loadUiType('main.ui')

# Hàm kết nối


def path():
	return pathlib.Path().resolve()


class MainApp(QMainWindow, ui_main):

	def __init__(self):
		QMainWindow.__init__(self)
		self.setupUi(self)
		try:
			os.mkdir('dataset', mode=0o777)
			os.mkdir('trainer', mode=0o777)
		except:
			print("")
		# click luu thong tin
		self.btn_train.clicked.connect(self.LuuThongTin)
		# click nhan dien khuon mat
		self.btn_NhanDang.clicked.connect(self.NhanDangKhuonMat)
		# thong bao
		self.SetNoti("Nhập thông tin sinh viên")
		# click cap nhat thong tin
		self.btn_capnhat.clicked.connect(self.CapNhatThongTin)
		# click out danh sach sinh vien
		self.btn_ds_SV.clicked.connect(self.DanhSachSV)
		# open ds sinh vien
		self.btn_ds_SV_Op.clicked.connect(self.DanhSachSVOp)
		# click danh sach diem danh
		today = date.today().strftime("%x").replace("/", "-")
		self.btn_list_dd_day.setText("Danh sách điểm danh " + str(today))
		self.btn_list_dd_day.clicked.connect(self.DanhSachDD)
		# click xoa sinh vien theo mssv
		self.btn_xoaSV.clicked.connect(self.XoaSinhVien)
		# click xoa all sv
		self.btn_delte_allSV.clicked.connect(self.XoaAllSinhVien)
		

		
	
	def SetNoti(self, txt):
		self.label = self.findChild(QLabel, "txt_noti")
		self.label.setText(txt)


	def LuuThongTin(self):
		mssv = self.edit_mssv.text()
		ten_sv  = self.edit_tensv.text()
		if ketnoi.LayTenSV(mssv) != True:
			audio.play("Sinh viên này đã tồn tại")
			self.SetNoti("Sinh viên này đã tồn tại")
			return
		# luu khuon mat
		try:
			# thong bao
			# audio play
			audio.play("Vui lòng nhìn vào camera")
			self.SetNoti("Vui lòng nhìn vào camera")
			_01_face_dataset.Dataset(mssv)
			# thong bao
			self.SetNoti("Thêm thông tin sinh viên")
			ketnoi.ThemSinhVien(mssv, ten_sv)
		except:
			# audio play
			audio.play("Có lỗi")
			# thong bao
			self.SetNoti("Có lỗi")
			print("Có lỗi")
			return
		# audio play
		audio.play("Tiến hành xử lý dữ liệu")
		# thong bao
		self.SetNoti("Tiến hành xử lý dữ liệu")
		_02_face_training.HuanLuyen()
		self.SetNoti("Đã xong !")
		# audio play
		audio.play("Đã hoàn thành cảm ơn bạn")
		QMessageBox.information(self, "Thông báo", "Lưu thông tin thành công")

	def NhanDangKhuonMat(self):
		# audio play
		audio.play("Vui lòng nhìn vào camera")
		self.SetNoti("Vui lòng nhìn vào camera")
		_03_face_recognition.NhanDien()

	def CapNhatThongTin(self):
		mssv = self.edit_mssv.text()
		ten_sv  = self.edit_tensv.text()
		if ketnoi.LayTenSV(mssv) != True:
			audio.play("Tiến hành cập nhật thông tin")
			self.SetNoti("Tiến hành cập nhật thông tin")
			# luu khuon mat
			try:
				# thong bao
				# audio play
				audio.play("Vui lòng nhìn vào camera")
				self.SetNoti("Vui lòng nhìn vào camera")
				_01_face_dataset.Dataset(mssv)
				# thong bao
				# self.SetNoti("Thêm thông tin sinh viên")
				# ketnoi.ThemSinhVien(mssv, ten_sv)
			except:
				# audio play
				audio.play("Có lỗi")
				# thong bao
				self.SetNoti("Có lỗi")
				print("Có lỗi")
				return
			# audio play
			audio.play("Tiến hành xử lý dữ liệu")
			# thong bao
			self.SetNoti("Tiến hành xử lý dữ liệu")
			_02_face_training.HuanLuyen()
			self.SetNoti("Đã xong !")
			# audio play
			audio.play("Đã hoàn thành cảm ơn bạn")
			QMessageBox.information(self, "Thông báo", "Cập nhật thông tin thành công")

	def DanhSachSV(self):
		ketnoi.LayDanhSachSV()
		QMessageBox.information(self, "Thông báo", "Tạo danh sách thành công")
		os.popen("danh-sach-sinh-vien.xlsx")

	def DanhSachSVOp(self):
		import os.path
		from os import path
		if path.isfile("danh-sach-sinh-vien.xlsx"):
			os.popen("danh-sach-sinh-vien.xlsx")
		else:
			QMessageBox.information(self, "Thông báo", "Danh sách sinh viên không tồn tại")

	def DanhSachDD(self):
		ketnoi.LayDanhSachDiemDanh()
		today = date.today().strftime("%x").replace("/", "-")
		self.SetNoti("Đã tạo danh sách điểm danh " + str(today))
		QMessageBox.information(self, "Thông báo", "Đã tạo danh sách điểm danh " + str(today))
		os.popen('danh-sach-diem_danh_'+str(today)+'.xlsx')

	def XoaSinhVien(self):
		mssv = self.edit_mssv.text()
		if mssv == "":
			QMessageBox.information(self, "Thông báo", "Vui lòng nhập mã số sinh viên")
		else:
			if ketnoi.LayTenSV(mssv) == False:
				ketnoi.DeleteSV(mssv)
				QMessageBox.information(self, "Thông báo", "Xoá thành công")
			else:
				QMessageBox.information(self, "Thông báo", "Sinh viên này không tồn tại !")


	def XoaAllSinhVien(self):
		ketnoi.DeleteAllSV()
		try:
			shutil.rmtree(str(path())+'\\dataset\\')
			shutil.rmtree(str(path())+'\\trainer\\')
		except:
			print("")
		QMessageBox.information(self, "Thông báo", "Xoá tất cả sinh viên thành công")
		try:
			os.mkdir('dataset', mode=0o777)
			os.mkdir('trainer', mode=0o777)
		except:
			print("")
		# xoa thu muc train and img




if __name__ == "__main__":
	
	app = QApplication(sys.argv)
	window = MainApp()
	window.show()
	app.exec()

	