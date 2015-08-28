import os.path
import registre.context
import registre.featurize
import registre.read

PARTICIPANTS_FILE = "participants.txt"
REGISTRE_LOG_DIR = "registre-logs"
REGISTRE_LOG_EXT = "-activities.txt"

def get_participants(base_dir):
    filename = os.path.join(base_dir, PARTICIPANTS_FILE)
    with open(filename) as f:
        return [name.strip() for name in f.readlines()]

def get_activities_for_participant(base_dir, participant):
    registre_file = "".join([participant, REGISTRE_LOG_EXT])
    registre_file = os.path.join(base_dir, REGISTRE_LOG_DIR, registre_file)
    return [a for a in registre.read.read_registre(registre_file)]

def generate_contexts(base_dir, participants):
    activities_by_participant = { participant: get_activities_for_participant(base_dir, participant) for participant in participants }
    contexts = []
    for (participant, activity) in activities_by_participant.iteritems():
        print "Participant: %s" % participant
        contexts.extend(registre.context.generate_contexts(activity))
        #try:
        #    contexts.extend(registre.context.generate_contexts(activity))
        #except Exception as e:
        #    print "Error in participant %s" % participant
        #    raise e
    #contexts.extend(registre.context.generate_contexts(activities_by_participant["anna-cameron"]))
    print "Done forming contexts."
    return contexts

def print_variables(contexts):
    features = registre.featurize.get_possible_features(contexts)
    for (variable, domain) in features.iteritems():
        print variable, domain

# Assignment 1
base_dir = "logs/assignment1"
participants = get_participants(base_dir)
# These are broken because they started with pre-existing workbook?
participants.remove("cameron1")
participants.remove("cameron2")
participants.remove("jenny")
participants.remove("hassan")
contexts = generate_contexts(base_dir, participants)
#print_variables(contexts)

# Assignment 2
#base_dir = "logs/assignment2"
#participants = get_participants(base_dir)
#contexts = generate_contexts(base_dir, participants)
#print_variables(contexts)

# Assignment 3
#base_dir = "logs/assignment3"
#participants = get_participants(base_dir)
#contexts = generate_contexts(base_dir, participants)
#print_variables(contexts)
