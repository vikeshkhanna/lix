'''
@author : Vikesh Khanna
Builds and matches the predicate tree (Abstract Syntax Tree) from a logical infix expression. Using Shunting Yard algorithm.
'''

class Types:
	OP="OP"  # An operator
	CMP="CMP" # A comparator
	EXPR="EXPR" # Part of an expression (key or value) but not a comparator
	PARANS="PARANS" # ( or )

class Operator:
	AND = 'and'
	OR = 'or'

class Comparator:
	LEQ = '<='
	LT = '<'
	GT = '>'
	GTE = '>='
	EQ = '='

OPERATORS = [Operator.AND, Operator.OR]
COMPARATORS = [Comparator.LEQ, Comparator.LT, Comparator.GT, Comparator.GTE, Comparator.EQ]
PARANS = ["(", ")"]

# Comparator Node.
# For example, a > 5 => comparator is '>', Key is 'a', Value is '5'
class CmpNode:
	def __init__(self, key, comparator, value):
		self.type = Types.CMP
		self.comparator = comparator
		self.key = key
		self.value = value

	def __repr__(self):
		return "CMP.{0}{1}{2}".format(self.comparator, self.key, self.value)

# Operator Node
# For example, "and" => operator is "and"
class OpNode:
	def __init__(self, operator):
		self.type = Types.OP
		self.operator = operator
	
	def __repr__(self):
		return "OP.{0}".format(self.operator)

# Tree Node is a wrapper for cmp and op nodes.
# They are the part of the AST and contain within themselves an opnode or a cmpnode.
class TreeNode:
	def __init__(self, node):
		self.node = node
		self.left = None
		self.right = None
	
	def __repr__(self):
		return str(self.node)

# Main class to handle predicates. The user creates the predicate object with a condition (like, a>3 and b <5) and optionally an "apply" dictionary to convert
# values in the predicates. For instance a < 5 => 5 is an int, and c=XYZ => XYZ is a string. So the apply dictionary would be {"a" : int, "c" : str}
# The user can then subsequently call the match function with the dictionary of actual values of the variables.
class Predicate:
	# @param condition : string representation of the logical infix expression
	# @param apply : Optional dictionary to convert variables to a different type/form.
	# For example ((a > 5 or  b > c) and c > d)
	def __init__(self, condition, apply = {}):
		self.apply = apply
		self.root = self.make_tree(condition)
		#self.print_tree(self.root)
	
	def make_tree(self, condition):
		postfix = self.get_postfix(condition)
		return self.get_tree_from_postfix(postfix)

	# Makes the AST from the Postfix expression
	def get_tree_from_postfix(self, postfix):
		tree_stack = []

		while len(postfix) > 0:
			node = postfix.pop(0)
			# Operator Node. Pop right, pop left and join with the operator
			if node.type == Types.OP:
				right = tree_stack.pop()
				left = tree_stack.pop()
				tmp_root = TreeNode(node)
				tmp_root.left = left
				tmp_root.right = right
				tree_stack.append(tmp_root)
			else:
			# Cmp Node. Create a tree node and push into the tree_stack.
				tree_stack.append(TreeNode(node))

		return tree_stack.pop()

	def get_next_word(self, condition, index):
		#print("next_word", index)
		word  = []
		j = index

		# skip leading whitespace
		while condition[j] == ' ' or condition[j] == "\t":
			j += 1

		# While we don't reach a new whitespace.
		while j < len(condition) and condition[j] != " ":
			if condition[j] in COMPARATORS:
				# Comparator reached when word is already formed. For example, a<4  (without space)
				if len(word) != 0:
					break
				else:
				# This is only comparator. For example, a < 4 (with space). or a <4 (without latter space.)
				# The check for GTE and LEQ is performed after the while loop.
					word.append(condition[j])
					j += 1
					break

			if condition[j] in PARANS:
				if len(word) != 0:
					# Word is already formed, this paranthesis is not a part of this word. For example, (a <3) (without space between 3 and paran)
					break
				else:
					# This is only the paranthese. For example (a < 3 ). Notice no white space.
					word.append(condition[j])
					j += 1
					break

			word.append(condition[j])
			j += 1

		type = Types.EXPR
		str_word = "".join(word)

		if str_word in OPERATORS:
			type = Types.OP
		elif str_word in COMPARATORS:
			# If word is < or >, check for <= and >=
			if condition[j] == "=":
				word.append(condition[j])
				j += 1
			type = Types.CMP
		elif str_word in PARANS:
			type = Types.PARANS
	
		#print("Returning", word, type)
		return ("".join(word), type, j)

	# Converts the infix expression to postfix using Shunting Yard algorithm.
	def get_postfix(self, condition): 
		i = 0
		stack = []
		postfix = []

		while i < len(condition):
			#print("Stack", stack)
			#print("Output", postfix)
			token = condition[i]
			
			# Ignore whitespace
			if token != " " and token != "\t":
				word, type, i  = self.get_next_word(condition, i)

				# word is an operator (say o1). Pop and output the operator (say, o2) from the stack while precedence of o1 < o2
				# Lower index in OPERATORS implies higher precedence
				if type == Types.OP:
					while len(stack)>0 and stack[-1] in OPERATORS and OPERATORS.index(word) > OPERATORS.index(stack[-1]):
						postfix.append(OpNode(stack.pop()))
					# Push this operator on the stack
					stack.append(word)
				# If word is a left paran, just append it on the stack.
				elif word == "(":
					stack.append(word)
				elif word == ")":
					while len(stack)>0 and stack[-1] in OPERATORS:
						postfix.append(OpNode(stack.pop()))
					# Pop off the left parananthesis
					if len(stack) == 0 or (len(stack) > 0 and stack[-1] != "("):
						raise Exception("Mismatched Paranthesis")
					else:
						stack.pop()
				# This is the key. Next two words should be CMP and EXPR respectively.
				else:
					cmp, type, i = self.get_next_word(condition, i)
					if type!=Types.CMP:
						raise Exception("Malformed expression. Please use logical infix expressions.")
					val, type, i = self.get_next_word(condition, i)
					if type!=Types.EXPR:
						raise Exception("Malformed expression. Please use logical infix expressions.")
					postfix.append(CmpNode(word, cmp, self.get_proper_value(word, val)))
			else:
				i += 1

		#print("End Stack", stack)
		while len(stack) > 0:
			op = stack.pop()

			if op not in OPERATORS:
				raise Exception("Mismatched Parantheses")
			else:
				postfix.append(OpNode(op))
	
		return postfix

	# Converts the value in the cmpNode to its proper form by applying the function supplied (if any)
	def get_proper_value(self, key, value):
		if key in self.apply:
			func = self.apply[key]

			try:
				return func(value)
			except:
				raise Exception("Could not apply conversion function to value. function={0}, key={1}, value={2}".format(func, key, value))

		return value

	# Infix printing of the Tree.
	def print_tree(self, root):
		if root!=None:
			self.print_tree(root.left)
			print(root.node)
			self.print_tree(root.right)

	# Tests whether the actual key and value satisfy the predicate in the cmp_node
	def match_cmp(self, cmp_node, actual_value):
		expected_value = cmp_node.value
		#print("match_cmp=> ac, cmp, ex=>", actual_value, cmp_node.comparator, expected_value)
		if cmp_node.comparator == Comparator.LEQ:
			return actual_value <= expected_value
		elif cmp_node.comparator == Comparator.LT:
			return actual_value < expected_value
		elif cmp_node.comparator == Comparator.GTE:
			return actual_value >= expected_value
		elif cmp_node.comparator == Comparator.GT:
			return actual_value > expected_value
		elif cmp_node.comparator == Comparator.EQ:
			return actual_value == expected_value
		else:
			raise Exception("Unsupported comparator")

		return False

	# Returns true if the given dictionary matches the condition.
	# Dictionary is of the form { a : 3, b : 5, s: 4} where the condition is for the form (a>3 and b<4) or s=2 
	def match(self, values):
		return self.match_inner(values, self.root)

	# Performs an inorder traversal of the tree and checks each leaf predicate against the dictionary.
	def match_inner(self, values, root):
		#print("match_inner", root, values)
		if root != None:
			# Return true for CMP (always leaf) nodes trivially
			if root.node.type == Types.CMP:
				key = root.node.key

				if key not in values:
					raise Exception("Condition key not found in the dictionary: {0}".format(key))

				return self.match_cmp(root.node, values[key])
			else:
			# OP Node. Returns the result of left and right sub-tree matches joined by the appropriate condition
				left = self.match_inner(values, root.left)
				right = self.match_inner(values, root.right)
				#print("ops", left, right, root.node.operator)

				if root.node.operator == Operator.AND:
					return left and right
				elif root.node.operator == Operator.OR:
					return left or right
				else:
					raise Exception("Unsupported Operator")
	
		# For null nodes, return true trivially
		return True
