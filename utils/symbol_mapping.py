#!/usr/bin/env python


chips = [
	3653456430,    #  0
	3986437410,    #  1
	786023250,     #  2
	585997365,     #  3
	1378802115,    #  4
	891481500,     #  5
	3276943065,    #  6
	2620728045,    #  7
	2358642555,    #  8
	3100205175,    #  9
	2072811015,    # 10
	2008598880,    # 11
	125537430,     # 12
	1618458825,    # 13
	2517072780,    # 14
	3378542520     # 15
	]

def mirror(n, bits):
	o = 0
	for i in range(bits):
		if(n & (1 << i)):
			o = o | (1 << (bits - 1 - i))
	return o


mapping = []

for c in range(16):
	# ahhhhhh endianess
	c = chips[mirror(c, 4)]
	c = mirror(c, 32)

	for i in range(16):
		rem = c % 4
		c = c / 4

		# QPSK
		if(rem == 0):
			mapping.append(-1-1j)
		elif (rem == 1):
			mapping.append( 1-1j)
		elif (rem == 2):
			mapping.append(-1+1j)
		elif (rem == 3):
			mapping.append( 1+1j)


print "length: " + str(len(mapping))
print mapping
