import hashlib
import timeit

file_name = input("file name with relative location: ")
original_md5 = input("paste md5 to chech: ")

start = timeit.default_timer()

md5 = hashlib.md5()

with open(file_name,'rb') as file_to_check: #need to read in binary model
	# can't read large file
	#data = file_to_check.read()
	#md5 = hashlib.md5(data).hexdigest()
	for chunk in iter(lambda: file_to_check.read(128*256000),b''): 
	# around 30MB per chunk (the size is in bytes) ; python needs double size of memory to run
		md5.update(chunk)
		
stop = timeit.default_timer()
result = md5.hexdigest()

print( "\n Orignial MD5: %s" % original_md5)

print( "\n Download MD5: %s" % result)

print("\n Runtime: %s seconds" % (stop-start))

if result==original_md5:
	print("\n MD5 verified")
else:
	print("\n MS5s are different")


input("Press Enter to exit")
