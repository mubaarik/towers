import argparse
class ParseCheck:
	def __init__(self, a,b,c):
		self.a =a 
		self.b=b;
		self.c = c;
	def printa(self):
		print "Printing a:",self.a
	def printb(self):
		print "Printing b: ",self.b 
	def printc(self):
		print "Printing c: ", self.c 
if __name__ == "__main__":
	prsr = argparse.ArgumentParser(description = 'Running the program to manupilate stream file data')
	prsr.add_argument('a', action='store', type=int)
	prsr.add_argument('b', action='store', type=float)
	prsr.add_argument('c', action='store',type = list)

	prsr.add_argument('--call', choices=('a', 'b', 'c'), dest='func_call', default='a')
	args = prsr.parse_args()
	check = ParseCheck(args.a,args.b,args.c);
	if args.func_call=='b':
		check.printb()
	elif args.func_call=='c':
		check.printc()
	else:
		check.printa()

#add_argument parameters
	#Actions:
		#Actions can be:
			#1. stroing the data as a single argument or part of a list
			#2. Storing constant value when the argument is encountered
			#3. Counting the number of times an argument is seen
			#4. Calling a callback function
			#5. Defualt: store the argument when encountered and converting the type if provided, otherwise string
			#If dest argument is specified, the value is stored in the parsed argument dictionary with the key specified by dest
			#By defualt the arguments are taking from sys.arv[1:]
			#The arguments are parsed using the GNU/POSIX convention so the option arguments can be mixed
			#The return value from parse_args() is a namespace containing the arguments passed to the command
			#The object stores the arguments as attributes so if your argument is dest is 'myoption' you can access the value as args.myoption

		#examples
#for signle character arguments(optionals), you pass them as '-c' and provide them as '-cval' or '-c' 'val'
	#example
		# parser.add_argument('-a', action="store_true", default=False)
		# parser.add_argument('-b', action="store", dest="b")
		# parser.add_argument('-c', action="store", dest="c", type=int)
		# print parser.parse_args(['-a', '-bval', '-c', '3'])
#For multiple character options, you pass them as '--option' and provide them as '--option' 'val' or '--option=val'
	#Example
		# parser.add_argument('--mubarik', action = 'store_true', default=False)
		# parser.add_argument('--jaamac', action = 'store', dest = 'jaamac')
		# parser.add_argument('--garaad', action = 'store', dest = 'garaad', type=int)
		# print parser.parse_args(['--mubarik','--jaamac','jaangeri', '--garaad=3'])
#Handles non optional argumenets too
	#Exanple
		# parser.add_argument('count', action = 'store', type=int)
		# parser.add_argument('uint', action = 'store')
		# print parser.parse_args(['3','inches'])
#Argument actions
	#store
		#Save argument after type conversion(if needed), defualt
	#store_true/store_false
		#Save the appropriate boolean value. These actions are used to implement boolean switches.
	#store_const
	#append 
		#Save the value to a list. Multiple values are saved if the argument is repeated.
	#append_canst
		#Save a value defined in the argument specification to a list.
	#version
		#Prints version details about the program and then exits.
	#Example
		# parser.add_argument('-s', dest='simple_value', help = 'storing simple one character value')
		# parser.add_argument('-c', action='store_const', dest='constant value',const='constant', help='Store constant value')
		# parser.add_argument('-t', action='store_true', default=False, dest='boolean_switch', help='Set a switch to true')
		# parser.add_argument('-f', action='store_false', default=False,dest='boolean_switch', help='Set a switch to false')
		# parser.add_argument('-a', action='append', dest='collection',default=[],help='Add repeated values to a list',)
		# parser.add_argument('-A', action='append_const', dest='const_collection',const='value-1-to-append',default=[],help='Add different values to list')
		# parser.add_argument('-B', action='append_const', dest='const_collection',const='value-2-to-append',help='Add different values to list')
		# parser.add_argument('--version', action='version', version='%(prog)s 1.0')

		# results = parser.parse_args()
		# print 'simple_value     =', results.simple_value
		# print 'constant_value   =', results.constant_value
		# print 'boolean_switch   =', results.boolean_switch
		# print 'collection       =', results.collection
		# print 'const_collection =', results.const_collection
'''

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="printing a,b, or c")

	parser.add_argument('-s', dest='simple_value', help = 'storing simple one character value')
	parser.add_argument('-c', action='store_const', dest='constant_value',const='constant_value', help='Store constant value')
	parser.add_argument('-t', action='store_true', default=False, dest='boolean_switch', help='Set a switch to true')
	parser.add_argument('-f', action='store_false', default=False,dest='boolean_switch', help='Set a switch to false')
	parser.add_argument('-a', action='append', dest='collection',default=[],help='Add repeated values to a list',)
	parser.add_argument('-A', action='append_const', dest='const_collection',const='value-1-to-append',default=[],help='Add different values to list')
	parser.add_argument('-B', action='append_const', dest='const_collection',const='value-2-to-append',help='Add different values to list')
	parser.add_argument('--version', action='version', version='%(prog)s 1.0')

	results = parser.parse_args()
	print 'simple_value     =', results.simple_value
	print 'constant_value   =', results.constant_value
	print 'boolean_switch   =', results.boolean_switch
	print 'collection       =', results.collection
	print 'const_collection =', results.const_collection

'''


















