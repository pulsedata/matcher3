'''
Welcome to Matcher 3
(c) PulseData/ftxrc 2016

This matches the pristine, virgin PR.gov into usable ones.
'''

# TODO: Testability

import os, argparse, json, random, time
from result import Result
import algs

VERSION = "0.0.1"

parser = argparse.ArgumentParser(description='Create the matched dataset.')
parser.add_argument('graduates', metavar="graduates", type=str, help="The graduates file")
parser.add_argument('schools', metavar="schools", type=str, help="The schools file")
parser.add_argument('--debug', default=False, action="store_true", help='Whether to perform debug routines.')
args = parser.parse_args()

# Constants
GRADUATES = json.loads(open(args.graduates, 'r').read())
SCHOOLS = json.loads(open(args.schools, 'r').read())
TIME = int(time.time())

# The Result instance
r = Result()

def create_school_item(school_id, name, accuracy=90):
    """ Return a school_item spec compatible dict. """
    return {
        'id': school_id,
        'name': name,
        'accuracy': accuracy,
    }

def result_path(append='', debug=args.debug, timestamp=TIME):
    """ Get a path for the out directory. """
    if debug:
        return "out/%s-debug-v%s/%s" % (timestamp, VERSION, append)
    else:
        return "out/%s-production-v%s/%s" % (timestamp, VERSION, append)


# Begin the matcher.
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
        elif algs.word_matches(graduate['school'], school['name']) >= 2:
            # Get the levhenstein
            lev_percent = algs.levenshtein_percent(school['name'], graduate['school'])
            print("Found word_matches match. Low confidence result, flagged.")
            print("Levenshtein distance percent: %s percent" %  lev_percent)
            school_item = create_school_item(school['id'], school['name'], 30)
            # Break  the rules a bit for debugging
            if args.debug:
                school_item['levp'] = lev_percent
            break

    graduate['school_data'] = school_item
    if school_item:
        r.insert(school_item['accuracy'], graduate)

if not os.path.exists(result_path()):
    os.makedirs(result_path())

with open(result_path('all.json'), 'a') as f:
    f.write(json.dumps(r.all))

with open(result_path('high.json'), 'a') as f:
    f.write(json.dumps(r.high))

with open(result_path('medium.json'), 'a') as f:
    f.write(json.dumps(r.medium))
    
with open(result_path('low.json'), 'a') as f:
    f.write(json.dumps(r.low))

print("============= STATS =============")
print("%d out of %d records were matched by ftxrc/PulseData Matcher3(c)." % (len(r.all), len(GRADUATES)))
print("%d results were low confidence results, for manual review." % len(r.low))
print("%d results were mid-tier confidence results." % len(r.medium))
print("%d results were high confidence results." % len(r.high))
percent = (len(r.all) / len(GRADUATES)) * 100
print("%d percent of records could be matched using the algorithm." % percent)
print("=============  END STATS =============")

if args.debug:
    print("\n============= DEBUG =============")
    print("High-tier:")
    shuffled = random.sample(r.high, k=5)
    print(json.dumps(shuffled, indent=2))
    print("Mid-tier:")
    shuffled = random.sample(r.medium, k=5)
    print(json.dumps(shuffled, indent=2))
    print("Low-tier:")
    shuffled = random.sample(r.low, k=5)
    print(json.dumps(shuffled, indent=2))
    print("=============  END DEBUG =============")