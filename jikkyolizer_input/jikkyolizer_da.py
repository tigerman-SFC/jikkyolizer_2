import pymysql

class JikkyolizerAccess(object):
	def __init__(self):
		self.get_cursor_database_access()
		#self.connector = self.fetch_object['connector']
		#self.cursor = self.fetch_object['cursor']

	def get_cursor_database_access(self):
		self.connector = pymysql.connect(host="172.17.0.2", db="jikkyolizer_data", user="root", passwd="sqladmin", charset="utf8", cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.connector.cursor()
		#self.access_object = { 'connector' : self.connector, 'cursor' : self.connector.cursor()}
		#return access_object

	def dict_insert(self, Table, Dicts):
		Params = Dicts.keys()
		Values = Dicts.values()
		SetParams = ''
		SetValues = ''
		StringValue = ''
		for Param in Params:
			if SetParams != '': 
				SetParams += ','
			SetParams += Param
		for Value in Values:
			if SetValues != '':
				SetValues += ','
			if isinstance(Value, str):
				SetValues += "'" + str(Value) + "'"
			else:
				SetValues += str(Value)
		sql = "insert into " + str(Table) + " (" + str(SetParams) + ") values(" + str(SetValues) + ");"
		print (sql)
		self.cursor.execute(sql)
		self.connector.commit()
		return 0 





