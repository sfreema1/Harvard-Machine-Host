import string
# ========== INPUTS AND OUTPUTS ========== #
"""
s = 'Hello, world!'
print str(s)
print repr(s)
value = 1.0/7.0
print str(value)
print repr(value)
"""

# ========== Opening files ============ #

# Attempt
opened_file = {}
with open("open_test.txt") as f:
	for line in f:
		tok = line.split(',')
		tok[3] = tok[3].rstrip('\n')
		opened_file[tok[3]] = tok[1]+tok[2]

print opened_file
print opened_file["green"]
"""
# ========== Understanding Python "with" keyword ========== #
class controlled_execution():
	def __enter__(self):
		set things up
		return thing
	def __exit__(self,type,value,traceback):
		tear things down

with controlled_execution() as thing:
	some code
"""
"""
print string.ascii_uppercase[0]

# ========== Writing a table =========== #
for x in range(11):
	print repr(x).rjust(2),repr(x*x).rjust(3),repr(x*x*x).rjust(4)

for x in range(11):
	print '{0:10d} {1:3d} {2:4d}'.format(x,x**2,x**3)

print vars()
"""

test_list = [[] for i in range(2)]
print test_list
test_list = [[] for i in range(10)]
print test_list