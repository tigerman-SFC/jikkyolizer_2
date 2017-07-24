from jikkyolizer_da2 import JikkyolizerAccess
import time
from datetime import datetime
import subprocess

class JikkyolizerVocalize():
	def __init__(self, item_id, group_id, raw_value, row_timestamp, reason, vocalize_prior, is_change):
		to_vocalize_data = JikkyolizerAccess()
		sql = 'SELECT auto_increment FROM information_schema.tables WHERE table_name = "voice_prior";'
		to_vocalize_data.cursor.execute(sql)
		jikkyo_id_pre = to_vocalize_data.cursor.fetchone() 
		jikkyo_id = jikkyo_id_pre['auto_increment']
		to_vocalize_data.dict_insert('voice_prior', { 'vocalize_kind':reason, 'vocalize_prior':vocalize_prior, 'group_id':group_id, 'item_id':item_id, 'raw_value':raw_value, 'row_timestamp':row_timestamp })
		to_vocalize_data.dict_insert('voice_prior_record', { 'ID':jikkyo_id, 'vocalize_kind':reason, 'vocalize_prior':vocalize_prior, 'group_id':group_id, 'item_id':item_id, 'raw_value':raw_value, 'row_timestamp':row_timestamp })
		
		how_ago = int(time.mktime(datetime.now().timetuple())) - int(datetime.strptime(row_timestamp, '%Y-%m-%d %H:%M:%S').strftime('%s'))
		how_ago_second = how_ago % 60
		how_ago_minute = int(how_ago % 3600 / 60)
		how_ago_hour = int(how_ago % 86400 / 3600)
		vocalize_sentence = '今から' 
		if how_ago_minute < 1:
			vocalize_sentence += str(how_ago_second) + '秒まえ、'
		elif how_ago_minute >= 1 and how_ago_hour < 1:
			vocalize_sentence += str(how_ago_minute) + '分まえ、'
		else:
			vocalize_sentence += str(how_ago_hour) + '時間まえ、'
		
		jikkyo_id5 = '{0:05d}'.format(jikkyo_id)
		
		if is_change == 1:
			vocalize_sentence += group_id + 'の、' + item_id + 'の値が、' + raw_value + '、になりました。'
		else:
			vocalize_sentence += group_id + 'の、' + item_id + 'の値が、' + raw_value + '、を示しました。'

		if reason == 'upper_jikkyolized':
			vocalize_sentence += 'これはとても高い値です。'
		elif reason == 'lower_jikkyolized':
			vocalize_sentence += 'これはとても低い値です。'
		elif reason == 'max_jikkyolized':
			vocalize_sentence += 'これは今までで最高の値です。'
		elif reason == 'min_jikkyolized':
			vocalize_sentence += 'これは今までで最高の値です。'
		
		cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id5 +'.wav'

		subprocess.call(cmd, shell=True) 


