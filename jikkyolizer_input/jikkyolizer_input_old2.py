import sys
#import pymysql
#import time

from jikkyolizer_da import JikkyolizerAccess
from jikkyolizer_vocalize import JikkyolizerVocalize


def main(from_jikkyolizer_string):
	group_id, item_id, raw_value, row_timestamp = parse_arg(from_jikkyolizer_string)
	to_jikkyolizer_data = JikkyolizerAccess()
	to_jikkyolizer_data.dict_insert('sox_data', { 'group_id':group_id, 'item_id':item_id, 'raw_value':raw_value, 'row_timestamp':row_timestamp } )
	insert_jikkyolized(item_id, group_id, raw_value, row_timestamp, to_jikkyolizer_data)
	#JikkyolizerVocalize(item_id, group_id, raw_value, row_timestamp)
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

def insert_jikkyolized(item_id, group_id, raw_value, row_timestamp, fetch_jikkyolized_data):
	re_calc_flag = 0
	#fetch_jikkyolized_data = JikkyolizerAccess()
	sql = 'select * from sox_jikkyolized where item_id=\'' + item_id + '\' and group_id=\'' + group_id + '\';'
	print (sql, flush=True)
	fetch_jikkyolized_data.cursor.execute(sql)

	result = fetch_jikkyolized_data.cursor.fetchone()
	print (result, flush=True)
	if result['total_number'] == 0:
		result['item_kind'] = judge_item_kind(raw_value) 

		init_topics = []
		result['string_0'] = str(raw_value)
		if result['item_kind'] == 'int' or result['item_kind'] == 'float':
			init_topics.extend(['max_value', 'min_value'])
		for init_topic in init_topics:
			result[init_topic] = eval(result['item_kind'])(raw_value)

		init_ones = ['total_number', 'span_0']
		for init_one in init_ones:
			result[init_one] = 1

		result['others'] = 0
		for i in range (1,10):
			result['span_' + str(i)] = 0

		result['last_0'] = row_timestamp
		
	else:
		if result['item_kind'] == 'str':
			i = 0
			others_flag = 1
			for i in range(10):
				if raw_value == result['string_' + str(i)]:
					result['span_' + str(i)] += 1
					others_flag = 0
					break
				elif result['string_' + str(i)] is None:
					others_flag = 0
					result['string_' + str(i)] = raw_value
					result['span_' + str(i)] += 1
					break
			if others_flag == 1:
				result['others'] += 1
			

		elif result['item_kind'] == 'int' or result['item_kind'] == 'float':
			raw_value = eval(result['item_kind'])(raw_value)
			distance = result['max_value'] - result['min_value']
			if distance == 0:
				if raw_value == result['max_value']:
					result['span_0'] += 1
				else:
					re_calc('min', raw_value, result, fetch_jikkyolized_data)
			else:
				if raw_value < result['min_value']:
					re_calc('min', raw_value, result, fetch_jikkyolized_data)
				elif raw_value > result['max_value']:
					re_calc('max', raw_value, result, fetch_jikkyolized_data)
				else:
					for xi in range(10):
						i = 9 - xi
						if raw_value >= float(result['string_' + str(i)]):
							result['span_' + str(i)] += 1
							result['last_' + str(i)] = row_timestamp
							break
					#how_high = raw_value - result['min_value']
					#span_no = str(int(how_high * 10 / distance))
					#if span_no == 10:
					#	span_no -= 1
					#result[span_no] += 1

		result['total_number'] += 1

	update_dicts = result.copy()
	del update_dicts['group_id']
	del update_dicts['item_id']
	#del update_dicts['item_kind']
	where_dicts = {'group_id': '\'' + result['group_id'] + '\'','item_id':'\'' +  result['item_id'] + '\''}

	for i in range(10):
		if update_dicts['string_' + str(i)] is not None:
			update_dicts['string_' + str(i)] = '\'' + update_dicts['string_' + str(i)] + '\''
		else:
			update_dicts['string_' + str(i)] = 'null'
		if update_dicts['last_' + str(i)] is not None:
			update_dicts['last_' + str(i)] = '\'' + str(update_dicts['last_' + str(i)]) + '\''
		else:
			update_dicts['last_' + str(i)] = 'null'
	if update_dicts['max_value'] is None:
		update_dicts['max_value'] = 'null'
	if update_dicts['min_value'] is None:
		update_dicts['min_value'] = 'null'

	update_dicts['item_kind'] = '\'' + update_dicts['item_kind'] + '\''

	fetch_jikkyolized_data.dict_update('sox_jikkyolized', update_dicts, where_dicts)
	#fetch_jikkyolized_data.cursor.execute(sql)
	#fetch_jikkyolized_data.connector.commit()

	return 0

def re_calc(reason, raw_value, jikkyolized_data, fetch_jikkyolized_data):

	sql = 'select * from sox_data where item_id=\'' + jikkyolized_data['item_id'] + '\' and group_id=\'' + jikkyolized_data['group_id'] + '\';'
	fetch_jikkyolized_data.cursor.execute(sql)
	past_data = fetch_jikkyolized_data.cursor.fetchall()
	
	max_value = jikkyolized_data['max_value']
	min_value = jikkyolized_data['min_value']
	if reason == 'max':
		jikkyolized_data['max_value'] = raw_value
		max_value = raw_value
	elif reason == 'min':
		jikkyolized_data['min_value'] = raw_value
		min_value = raw_value

	distance = max_value - min_value
	if jikkyolized_data['item_kind'] == 'float':
		for i in range(10):
			jikkyolized_data['string_' + str(i)] = str(round(distance) * i / 10)
			jikkyolized_data['span_' + str(i)] = 0
	elif jikkyolized_data['item_kind'] == 'int':
		for i in range(10):
			if i >= 1:
				if jikkyolized_data['string_' + str(i)] != jikkyolized_data['string_' + str(i-1)]:
					jikkyolized_data['string_' + str(i)] = str(round(distance * i / 10))
					jikkyolized_data['span_' + str(i)] = 0
				else:
					jikkyolized_data['string_' + str(i)] = None
					jikkyolized_data['span_' + str(i)] = None
		
	for past_datum in past_data:
		for xi in range(10):
			i = 9 - xi
			if float(past_datum['raw_value']) >= float(jikkyolized_data['string_' + str(i)]):
				jikkyolized_data['span_' + str(i)] += 1
				jikkyolized_data['last_' + str(i)] = past_datum['row_timestamp']
				break

	return jikkyolized_data
	

	




def judge_item_kind(raw_value):
	try:
		dummy = float(raw_value)
	except:
		return 'str'
	try:
		dummy = int(raw_value)
		return 'int'
	except:
		return 'float'



if __name__ == '__main__':
	f = open('/var/log/jikkyolizer/input.log', 'a')
	f.write(sys.argv[1])
	f.close()
	print (sys.argv[1])
	main(sys.argv[1])
	sys.exit()
