import json
import os
import os.path
import re
import read

class Session(object):
    
    def __init__(self, explorer, recorder, assignment, dataset, logpath):
        self.explorer = explorer
        self.recorder = recorder
        self.assignment = assignment
        self.dataset = dataset
        self.logpath = logpath
        self.activities = [a for a in read.read_registre(self.logpath)]

def get_sessions(directory):
    # Ugly exploration session parsing code.
    sessions = []
    datasets_analyzed = {}
    assignment_pattern = re.compile("assignment[\d]")
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for dirname in dirnames:
            if assignment_pattern.match(dirname) is not None:
                datasets_analyzed[dirname] = {}
        for filename in filenames:
            if filename == "data-analyzed.json":
                assignment = os.path.split(dirpath)[1]
                with open(os.path.join(dirpath, filename)) as f:
                    mapping = json.load(f)
                for (user, dataset) in mapping.iteritems():
                    datasets_analyzed[assignment][user] = mapping[user]
        if len(dirnames) == 0 and os.path.split(dirpath)[1] == "registre-logs":
            for filename in filenames:
                explorer = filename.replace("-activities.txt", "")
                recorder = explorer
                assignment = os.path.split(os.path.split(dirpath)[0])[1]
                dataset = datasets_analyzed[assignment][explorer]
                logpath = os.path.join(dirpath, filename)
                hidx = explorer.find("-")
                if hidx > -1:
                    recorder = explorer[hidx+1:]
                    explorer = explorer[:hidx]
                s = Session(explorer, recorder, assignment, dataset, logpath)
                if len(s.activities) > 0:
                    sessions.append(s)
    return sessions
