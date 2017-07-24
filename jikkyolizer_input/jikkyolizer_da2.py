import pymysql

class JikkyolizerAccess(object):
	def __init__(self):
		self.get_cursor_database_access()
		#self.connector = self.fetch_object['connector']
		#self.cursor = self.fetch_object['cursor']

	def get_cursor_database_access(self):
		self.connector = pymysql.connect(host="172.17.0.3", db="jikkyolizer_data", user="root", passwd="sqladmin", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
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
		sql = "insert into " + str(Table) + " (" + SetParams + ") values(" + SetValues + ");"
		#print (sql)
		self.cursor.execute(sql)
		self.connector.commit()
		return 0 

	def dict_update(self, Table, update_dicts, where_dicts):
		Params = update_dicts.keys()
		Values = update_dicts.values()
		update_string = 'update ' + Table + ' set '
		for Param,Value in zip(Params, Values):
			update_string += Param + '=' + str(Value) + ','
		update_string = update_string[:-1]
		update_string += ' where '
		where_params = where_dicts.keys()
		where_values = where_dicts.values()
		for where_param, where_value in zip(where_params, where_values):
			update_string += where_param + '=' + str(where_value) + ' and '
		update_string = update_string[:-5]

		print(update_string, flush=True)

		self.cursor.execute(update_string)
		self.connector.commit()
		return 0
			
		


