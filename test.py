'''
@author: Vikesh Khanna
Test script for predicate.py
'''
from predicate import *
import random

random.seed()

# Static tests
condition = "a > 5 and b<3"
print("Testing", condition)
predicate = Predicate(condition, { "a" : int, "b" : int })

test1 = predicate.match({"a":3, "b":5})
assert test1 == False
test2 = predicate.match({"a" : 6, "b" : 2})
assert test2 == True

condition = "(a > 5 and b<3) or c=STATE"
predicate = Predicate(condition, { "a" : int, "b" : int, "c" : str})
test1 = predicate.match({"a": 5, "b":4, "c":"SEL"})
assert test1 == False
test2 = predicate.match({"a" : 6, "b" : 5, "c" : "STATE"})
assert test2 == True

predicate = Predicate("(a > 5 and b<3) or (stack>4 and ACTION<=asa)")

# Random test generator
# Probability of this node being a leaf node
P=0.65
MAXV=10

class RandomNode:
	def __init__(self, val):
		self.val = val
		self.left = None
		self.right = None
	

def f_to_list(x):
	return map(int, x)

def get_rand_var():
	return chr(ord('a') + random.randint(0, 25))

def get_rand_list():
	# Max 5 elements, each in range (1, 10)
	n = random.randint(1, 5)
	rand_list = []
	for i in range(n):
		rand_list.append(random.randint(1, 10))

	return rand_list

def get_rand_val():
	return random.randint(1, MAXV)

# Probability 
def gen_tree(variables):
	toss = random.random()
	root = None

	if toss <= P:
		# leaf node
		comparator = random.choice(COMPARATORS)
		key = get_rand_var()
		value = get_rand_val()
		
		# if this variable has already been used and has a "HAS" operator, make sure it is "HAS" again
		if key in variables and variables[key] == f_to_list:
			comparator = Comparator.HAS

		val = "{0} {1} {2}".format(key, comparator, value)

		variables[key] = int

		if comparator == Comparator.HAS:
			variables[key] = f_to_list

		root = RandomNode(val)
	else:
		# operator node
		op = random.choice(OPERATORS)
		root = RandomNode(op)
		root.left = gen_tree(variables)
		root.right = gen_tree(variables)

	return root

def get_expr_from_tree(root):
	if root!=None:
		left = get_expr_from_tree(root.left)
		right = get_expr_from_tree(root.right)

		# Don't enclose in paranthesis for leaf nodes
		if root.left != None and root.right != None:
			return "({0} {1} {2})".format(left, root.val, right)
		else:
			return root.val
	return ""

def get_rand_values(variables):
	values = {}
	for key in variables:
		# If the comparator is HAS, generate a random list
		if variables[key] == f_to_list:
			values[key] = get_rand_list()
		else:
			values[key] = random.randint(1, MAXV)
	
	return values

def gen_expr():
	variables = {}
	root = gen_tree(variables)
	return get_expr_from_tree(root), variables

NUM_TESTS=100
NUM_TRIES_PER_COND=10

for i in range(NUM_TESTS):
	print("Test# ", i+1)
	print("***********")
	root = gen_tree({})
	condition, app = gen_expr()
	predicate = Predicate(condition, app)

	for j in range(NUM_TRIES_PER_COND):
		print("Attempt# ", j+1)
		values = get_rand_values(app)
		print("Condition", condition)
		print("Values", values)
		result = predicate.match(values)
		print("Resut", result)
		print("")
	
	print("*******")
