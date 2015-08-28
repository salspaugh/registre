import collections
import sys
import registre.read

filenames = sys.argv[1:]

with open("tableau-action-counts.csv", 'w') as csvfile:
    action_count = collections.defaultdict(int)
    for filename in filenames:
        for activity in registre.read.read_registre(filename):
            action_count[activity["action"]] += 1

    action_count = sorted(action_count.iteritems(), key=lambda x: x[1], reverse=True)
    for (action, count) in action_count:
        csvfile.write("%s,%d\n" % (action, count))

with open("tableau-action-counts-user-weighted.csv", 'w') as csvfile:
    action_per_user_count = {}
    nusers = 0.
    for filename in filenames:
        nusers += 1.
        action_per_user_count[filename] = collections.defaultdict(int)
        for activity in registre.read.read_registre(filename):
            action_per_user_count[filename][activity["action"]] += 1

    action_count = collections.defaultdict(list)
    for (user, user_action_count) in action_per_user_count.iteritems():
        total = float(sum(user_action_count.values()))
        for (action, count) in user_action_count.iteritems():
            action_count[action].append(count/total)

    action_count = { action: sum(fracs)*1./nusers for (action, fracs) in action_count.iteritems() }
    action_count = sorted(action_count.iteritems(), key=lambda x: x[1], reverse=True)
    for (action, count) in action_count:
        csvfile.write("%s,%.2f\n" % (action, count))
