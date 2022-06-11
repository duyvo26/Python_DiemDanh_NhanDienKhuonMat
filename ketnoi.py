from mysql.connector import MySQLConnection, Error
import pandas as pd
from datetime import date

def connect():
		db_config = {
	        'host': 'localhost',
	        'database': 'pydiemdanh',
	        'user': 'root',
	        'password': ''
	    }
		conn = None
		try:
			conn = MySQLConnection(**db_config)
			if conn.is_connected():
				return conn
		except Error as error:
			print(error)
		return conn




def ThemSinhVien(mssv, ten_sv):

	sql = ("INSERT INTO sinhvien "
               "(mssv, ten_sv) "
               "VALUES (%s, %s)")
	data = (mssv, ten_sv)
	conn = connect()
	cursor = conn.cursor()
	cursor.execute(sql, data)
	conn.commit()
	print("___________________________________________________")
	print(cursor.rowcount, "Thêm thành công")
	print("___________________________________________________")



def CheckDiemDanh(mssv):
	db = connect()
	mycursor = db.cursor()
	
	today = date.today()
	sql = ("SELECT mssv FROM diemdanh WHERE mssv = "+mssv+" and date_format(date(date_diemdanh),'%Y-%m-%d') = '"+str(today)+"'")
	mycursor.execute(sql)
	myresult = mycursor.fetchone()
	if myresult == None:
		return True
	else:
		return False

def GetTimeDiemDanh(mssv):
	db = connect()
	mycursor = db.cursor()
	today = date.today()
	sql = ("SELECT date_diemdanh FROM diemdanh WHERE mssv = "+str(mssv)+" and date_format(date(date_diemdanh),'%Y-%m-%d') = '"+str(today)+"'")
	mycursor.execute(sql)
	myresult = mycursor.fetchone()
	if myresult == None:
		return False
	else:
		return myresult[0]

def LayTenSV(mssv):
	if CheckDiemDanh(mssv) == True:
		db = connect()
		mycursor = db.cursor()
		sql = ("SELECT ten_sv FROM sinhvien WHERE mssv = "+mssv)
		mycursor.execute(sql)
		myresult = mycursor.fetchone()
		try:
			return myresult[0]
		except:
			return True
	else:
		return False

def DeleteSV(mssv):
	db = connect()
	mycursor = db.cursor()
	sql = ("DELETE  FROM sinhvien WHERE mssv = "+ mssv)
	mycursor.execute(sql)
	db.commit()
	DeleteSV_DD(mssv)
	
def DeleteSV_DD(mssv):
	db = connect()
	mycursor = db.cursor()
	sql = ("DELETE  FROM diemdanh WHERE mssv = "+ mssv)
	mycursor.execute(sql)
	db.commit()


def DeleteAllSV():
	db = connect()
	mycursor = db.cursor()
	sql = ("DELETE  FROM sinhvien")
	mycursor.execute(sql)
	db.commit()
	DeleteAllSV_DD()


def DeleteAllSV_DD():
	db = connect()
	mycursor = db.cursor()
	sql = ("DELETE  FROM diemdanh")
	mycursor.execute(sql)
	db.commit()


def LayDanhSachSV():
	db = connect()
	mycursor = db.cursor()
	sql = ("SELECT * FROM sinhvien")
	mycursor.execute(sql)
	# myresult = mycursor.fetchone()
	# print(mycursor)
	MSSV = []
	Ho_Ten = []
	for x in mycursor:
		MSSV.append(str(x[2]))
		Ho_Ten.append(str(x[1]))

	data_series = {"MSSV" :MSSV,"Ho Ten": Ho_Ten}
	df_data = pd.DataFrame(data_series)
	df_data.to_excel('danh-sach-sinh-vien.xlsx') 
	print("Tạo file danh sách hoàn tất")


def LayTenSV(mssv):
	if CheckDiemDanh(mssv) == True:
		db = connect()
		mycursor = db.cursor()
		sql = ("SELECT ten_sv FROM sinhvien WHERE mssv = "+mssv)
		mycursor.execute(sql)
		myresult = mycursor.fetchone()
		try:
			return myresult[0]
		except:
			return True
	else:
		return False

def LayDanhSachDiemDanh():
	db = connect()
	mycursor = db.cursor()
	sql = ("SELECT * FROM sinhvien")
	mycursor.execute(sql)
	# myresult = mycursor.fetchone()
	# print(mycursor)
	MSSV = []
	Ho_Ten = []
	TinhTrang = []
	Time_DiemDanh = []

	for x in mycursor:
		MSSV.append(str(x[2]))
		Ho_Ten.append(str(x[1]))
		time_dd = GetTimeDiemDanh(x[2])
		# print(time_dd)
		if time_dd == False:
			time_dd = ""
		Time_DiemDanh.append(str(time_dd))

	for i in MSSV:
		tinhtrang = CheckDiemDanh(i)
		if tinhtrang == True:
			tinhtrang = "Vắng"
		else:
			tinhtrang = "Có mặt"

		TinhTrang.append(tinhtrang)
	
	data_series = {"MSSV" :MSSV,"Ho Ten": Ho_Ten,"Diem danh": TinhTrang, "Thoi gian": Time_DiemDanh}
	df_data = pd.DataFrame(data_series)
	today = date.today().strftime("%x").replace("/", "-")
	df_data.to_excel('danh-sach-diem_danh_'+str(today)+'.xlsx') 
	print("Tạo file danh sách hoàn tất")
	



def LaySVTonTai(mssv):

	db = connect()
	mycursor = db.cursor()
	sql = ("SELECT ten_sv FROM sinhvien WHERE mssv = " + mssv)
	mycursor.execute(sql)
	myresult = mycursor.fetchone()
	try:
		return myresult[0]
	except:
		return True



def DiemDanh(mssv):
	sql = ("INSERT INTO diemdanh (mssv) VALUES ("+str(mssv)+")")
	conn = connect()
	cursor = conn.cursor()
	cursor.execute(sql)
	conn.commit()
	print("___________________________________________________")
	print(cursor.rowcount, "Diem danh thành công")
	print("___________________________________________________")