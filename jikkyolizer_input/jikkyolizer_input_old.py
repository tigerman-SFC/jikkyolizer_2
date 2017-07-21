import sys
import pymysql
import time

def main(from_jikkyolizer_string):
	item_id, raw_value, timing = parse_arg(from_jikkyolizer_string)
	to_jikkyolizer_data = JikkyolizerAccess()
	to_jikkyolizer_data.dict_insert('sox_data', { 'item_id':item_id, 'raw_value':raw_value, 'row_timestamp':timing } )
	#add_jikkyolized_item(item_id, )

def parse_arg(from_jikkyolizer_string):
	fj_string = from_jikkyolizer_string
	print (fj_string + '\n', flush=True)
	item_id_start = len("item_id")
	item_id_start += 2
	raw_value_start = fj_string.find(" raw_value=") 
	item_id = fj_string[item_id_start:raw_value_start]
	raw_value_start += len(" raw_value=")
	timing_start = fj_string.find(" timing=")
	raw_value = fj_string[raw_value_start:timing_start]
	timing_start += len(" timing=")
	timing_process_date = len("2017-07-16")
	timing = fj_string[timing_start:timing_start + timing_process_date] + " "
	timing_process_time = len("01:00:00")
	timing += fj_string[timing_start + timing_process_date + 1 : timing_start + timing_process_date + 1 + timing_process_time]
	#print (item_id + '\n')
	#print (raw_value + '\n')
	#print (timing + '\n', flush=True)
	return item_id, raw_value, timing

	

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


if __name__ == '__main__':
	time.sleep(3)
	f = open('write.txt', 'a')
	f.write(sys.argv[1])
	f.close()
	print (sys.argv[1])
	main(sys.argv[1])
	sys.exit()
