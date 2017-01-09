'''
Welcome to Matcher 3
(c) PulseData/ftxrc 2016

This matches the pristine, virgin PR.gov into usable ones.
'''

from result import Result
import argparse, json, jellyfish

parser = argparse.ArgumentParser(description='Create the matched dataset.')
parser.add_argument('graduates', metavar="graduates", type=str, help="The graduates file")
parser.add_argument('schools', metavar="schools", type=str, help="The schools file")
parser.add_argument('--debug', default=False, action="store_true", help='Whether to perform debug routines.')
args = parser.parse_args()

GRADUATES = json.loads(open(args.graduates, 'r').read())
SCHOOLS = json.loads(open(args.schools, 'r').read())

r = Result()

def create_school_item(school_id, name, accuracy=90):
    return {
        'id': school_id,
        'name': name,
        'accuracy': accuracy
    }

def word_matches(str1, str2): 
    # Refactor
    str1 = str1.split()
    str2 = str2.split()
    words_str1 = [word for word in str1 if len(word) >= 3]
    words_str2 = [word for word in str2 if len(word) >= 3]
    return len(set(words_str1).intersection(words_str2))

def levenshtein_percent(str1, str2):
    lev = jellyfish.levenshtein_distance(str1, str2)
    mxp = max(len(str1), len(str2))
    levp = ((mxp - lev) / mxp) * 100
    return int(round(levp, 0))

for graduate in GRADUATES:
    school_item = None
    for school in SCHOOLS:
        if school['location']['municipality'] != graduate['location']['city']:
            # The school isn't in the graduate's municipality. Continue looking.
            continue

        if school['name'] == graduate['school']:
            # High confidence result; name and municipality match.
            school_item = create_school_item(school['id'], school['name'], 90)
            break
        elif school['name'] in graduate['school']:
            # Medium confidence, full string found in other one.
            school_item = create_school_item(school['id'], school['name'], 60)
            break
        elif word_matches(graduate['school'], school['name']) >= 2:
            # Get the levhenstein
            lev_percent = levenshtein_percent(school['name'], graduate['school'])
            print("Found word_matches match. Low confidence result, flagged.")
            print("Levenshtein distance percent: %s percent" %  lev_percent)
            school_item = create_school_item(school['id'], school['name'], 30)
            break
    # TODO: Integrate results
    graduate['school_data'] = school_item
    if school_item:
        r.insert(school_item['accuracy'], graduate)
    
print("%d records were matched by ftxrc/PulseData Matcher3(c)." % COUNTER_MATCHED)
percent = (len(r.all) / len(GRADUATES)) * 100
print("%d percent of records could be matched using the algorithm." % percent)
