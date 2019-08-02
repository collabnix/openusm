import os
import sys
import time
test_file = open('counter.txt','w')
counter = 0
while True:
	print counter
	counter = counter + 1
	test_file.write('Counter is %s'%(counter))
	time.sleep(3)
	if counter == 100:
		test_file.close()
		sys.exit(0)
