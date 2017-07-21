import sys
f = open(sys.argv[1],'w')
f.write('hoge')
f.close()
f = open(sys.argv[2],'r')
for row in f:
	print (row)
f.close()
print (sys.argv)
