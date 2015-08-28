import json
import dateutil.parser

# Project imports:
import actions
import tableaukeys

def write_registre(input, output):
    with open(output, 'w') as activity_record:
        for activity in parse_tableau_log(input):
            json.dump(activity, activity_record) #sort_keys=True, indent=4, separators=(',', ': '))
            activity_record.write("\n")
            activity_record.flush()

def parse_tableau_log(input):
    with open(input) as raw_log:
        for line in raw_log:
            for activity in parse_tableau_log_line(line):
                yield activity

def parse_tableau_log_line(line):
    event = json.loads(line)
    activity = {}
    if event["k"] == "command-pre" and event["v"]["name"]:
        activity["action"] = event["v"]["name"]
        activity["timestamp"] = float(dateutil.parser.parse(event["ts"]).strftime('%s.%f'))
        parse_activity_parameters(activity, event["v"]["args"])
        yield activity

def parse_activity_parameters(activity, args):
    parameters = parse_command_pre_args(activity["action"], args)
    if parameters is not None and len(parameters) > 0:
        activity["parameters"] = parameters

def parse_command_pre_args(action, args):
    rest = split_command_pre_args(args)
    if rest is not None:
        return actions.ACTION_PARSERS.get(action, actions.DEFAULT_PARSER)(rest)

def split_command_pre_args(args):
    rest = None
    action_idx = args.find(" ")
    if action_idx > -1:
        rest = args[action_idx:].strip()
    return rest


if __name__ == "__main__":
    import argparse
    OUTPUT_DEFAULT = "activity.txt"
    parser = argparse.ArgumentParser("Extract activity records from Tableau logs.")
    parser.add_argument("-i", "--input",
                        help="path to the log file to parse")
    parser.add_argument("-o", "--output",
                        help="path to the activity record file to output (default is %s)" % OUTPUT_DEFAULT)

    args = parser.parse_args()
    if args.input is None:
        raise RuntimeError("You must provide an input file.")
        parser.print_help()
    if args.output is None:
        args.output = OUTPUT_DEFAULT

    write_registre(args.input, args.output) 
