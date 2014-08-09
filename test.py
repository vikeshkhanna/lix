from predicate import *

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
