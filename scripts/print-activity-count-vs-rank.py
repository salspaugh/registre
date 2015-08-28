import collections
import matplotlib.pyplot as plt
import numpy as np
import os.path
import registre.read
import registre.words

TABLEAU_LOG_DIR = "logdata/assignment1/tableau-logs"
REGISTRE_LOG_DIR = "logdata/assignment1/registre-logs"
PARTICIPANTS_FILE = "logdata/assignment1/participants.txt"
REGISTRE_LOG_EXT = "-activities.txt"

def get_participants(filename):
    with open(filename) as f:
        return [name.strip() for name in f.readlines()]
    
participants = get_participants(PARTICIPANTS_FILE)
print "Number of participants:", len(participants)

def get_registre_for_participant(participant):
    registre_file = "".join([participant, REGISTRE_LOG_EXT])
    registre_file = os.path.join(REGISTRE_LOG_DIR, registre_file)
    return [a for a in registre.read.read_registre(registre_file)]

registres_by_participant = { participant: get_registre_for_participant(participant) for participant in participants }
activity_counts_sorted = sorted([(p, len(a)) for (p, a) in registres_by_participant.iteritems()], key=lambda x: x[1])

action_counts = collections.defaultdict(int)
for participant in participants:
    actions = [a["action"] for a in registres_by_participant[participant]]
    for action in actions:
        action_counts[action] += 1
print "Total number of action types: %d" % len(action_counts.keys())
action_counts_sorted = sorted(action_counts.iteritems(), key=lambda x: x[1], reverse=True)
print "{:42}{:5}".format("action", "count")
for (action, count) in action_counts_sorted:
    print "{:42}{:5}".format(action, count)

counts = [np.log(x[1]) for x in action_counts_sorted]
ranks = range(len(counts))

plt.plot(ranks, counts)
plt.xlim(xmax=max(ranks))
plt.xlabel("Rank", fontsize=16)
plt.ylabel("Count", fontsize=16)
plt.savefig("figs/activity-counts-vs-rank-log.pdf")

