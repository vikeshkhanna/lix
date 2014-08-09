**lix command line interface.**

Searches the Lix tests for the given search term and returns all the experiments for the matched tests. The search is a simple substring match - so all the tests for which the key contains a substring of the given search term will be returned. Additionally, the experiments may be filtered with a --filter switch. See example below.

**Usage**:
./lix.py -f PROD skill-endorsement --filter "state=ACTIVE and approve_user=jwon"
./lix.py -f PROD skill-endorsement --filter "state=ACTIVE and (approve_user=jwon or approve_user=ndave)"

