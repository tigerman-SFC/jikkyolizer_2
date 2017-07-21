import sys
#import pymysql
#import time

from jikkyolizer_da import JikkyolizerAccess

def main(from_jikkyolizer_string):
	group_id, item_id, raw_value, timing = parse_arg(from_jikkyolizer_string)
	to_jikkyolizer_data = JikkyolizerAccess()
	to_jikkyolizer_data.dict_insert('sox_data', { 'group_id':group_id, 'item_id':item_id, 'raw_value':raw_value, 'row_timestamp':timing } )
	insert_jikkyolized(item_id, group_id, raw_value, row_timestamp)
	#add_jikkyolized_item(item_id, )

def parse_arg(from_jikkyolizer_string):
	fj_string = from_jikkyolizer_string
	print (fj_string + '\n', flush=True)
	group_id_start = len("group_id")
	group_id_start += 1
	item_id_start = fj_string.find(" item_id=") 
	group_id = fj_string[group_id_start:item_id_start]
	item_id_start += len(" item_id=")
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
	return group_id, item_id, raw_value, timing

def insert_jikkyolized(item_id,group_id, raw_value, row_timestamp):
	fetch_jikkyolized_data = JikkyolizerAccess()
	sql = 'select * from sox_jikkyolized where item_id=' + item_id + ' and group_id=' + group_id + ';'
	fetch_jikkyolized_data.cursor.execute(sql)
	result = cursor.fetchone()
	if total_number == 0:
		result['item_kind'] = judge_item_kind(raw_value)
	if result['item_kind'] == 'string':
		i = 0
		others_flag = 1
		for i in range(10):
			if raw_value is None:
				others_flag = 0
				result['string_' + str(i)] = raw_value
				break
			if raw_value == result[eval('string_' +str(i))]:
				others_flag = 0
				break
		if others_flag == 1:
			result['others'] += 1
		



	result['total_number'] += 1
	

def judge_item_kind(raw_value):
	try:
		dummy = float(raw_value)
	except:
		return 'string'
	try:
		dummy = int(raw_value):
	except:
		return 'float'
	finally:
		return 'int'



if __name__ == '__main__':
	f = open('/var/log/jikkyolizer/input.log', 'a')
	f.write(sys.argv[1])
	f.close()
	print (sys.argv[1])
	main(sys.argv[1])
	sys.exit()
