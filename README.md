**lix command line interface.**

Lex is a command-line interface for Lix @ LinkedIn. It searches the Lix tests for the given search term and returns all the experiments for the matched tests. The search is a simple substring match - so all the tests for which the key contains a substring of the given search term will be returned (Consistent with go/lix). Additionally, Lex provides powerful filtering of the experiments. Experiments may be filtered with a --filter switch. The *Usage* section specifies the most commonly used conditions. See the predicate grammer below if more advanced filtering is desired. 

**Usage**:
./lix.py -f PROD skill-endorsement --filter "state=ACTIVE and approve_user=jwon"
./lix.py -f PROD skill-endorsement --filter "state=ACTIVE and (approve_user=jwon or approve_user=ndave)"
./lix.py -f PROD skill-endorsement --filter "state=ACTIVE and (approve_user=jwon or owners has ndave)"

**Predicate Grammar**
Condition -> Condition Operator Condition
Condition -> (Condition)
Condition -> Key Comparator Value
Operator -> and | or
Comparator ->  > | < | <= | >= | = | has
Key -> *
Value -> *
