import json
import re
from string import whitespace as WHITESPACE

QUOTES = ['"', "'", "`"]
ESCAPE = '\\'
SPECIAL = ['=']
LBRACKET = '['
RBRACKET = ']'
LBRACE = '{'
RBRACE = '}'

FN_PATTERN = re.compile("\[(?P<table>.*)\]\.\[(?P<relation>.*)\]")

def default_parser(args):
    """
    .. function:: default_parser(args)

    Parse the list of parameters to the 'command-pre' event (i.e., 
    event["v"]["args"] with event["v"]["name"] removed). This list is actually 
    a string with space-separated key-value pairs, where the values can be
    a regular string, a JSON object, or XML (?).

    :param args: space-separated string list of key-value pairs (i.e., u'k="v"')
    :type args: string    
    :rtype: dict
    """
    parameters = {}
    tokens = []
    currtok = []
    brackstack = []
    bracestack = []
    escaped = False
    quoted = False
    enlisted = False
    enbraced = False
    quotechar = ''
    for char in args:
        if not quoted and not enlisted and not enbraced:
            if char in SPECIAL:
                if currtok: tokens.append("".join(currtok))
                currtok = []
                escaped = False
                continue
            if char in QUOTES:
                if escaped:
                    escaped = False
                    currtok.append(char)
                    continue
                else:
                    escaped = False
                    quoted = True
                    quotechar = char
                    currtok.append(char)
                    continue
            if char in WHITESPACE:
                if currtok:
                    tokens.append("".join(currtok))
                    currtok = []
                escaped = False
                continue
            if char == LBRACKET:
                brackstack.append(char)
                enlisted = True
                currtok.append(char)
                escaped = False
                continue
            if char == LBRACE:
                bracestack.append(char)
                enbraced = True
                currtok.append(char)
                escaped = False
                continue
            if char == ESCAPE:
                if not escaped:
                    escaped = True
                    currtok.append(char)
                    continue
                else: # the last character escaped this one
                    escaped = False
                    currtok.append(char)
                    continue
            # not special, whitespace, quotechar, or escape
            if escaped: escaped = False
            currtok.append(char)
            continue
        if quoted and not enlisted and not enbraced:
            if char in QUOTES:
                if escaped:
                    escaped = False
                    currtok.append(char)
                    continue
                else:
                    if char == quotechar:
                        escaped = False
                        quoted = False
                        quotechar = ''
                        currtok.append(char)
                        tokens.append("".join(currtok))
                        currtok = []
                        continue
                    else:
                        escaped = False
                        currtok.append(char)
                        continue
            if char == ESCAPE:
                if not escaped:
                    escaped = True
                    currtok.append(char)
                    continue
                else: # the last character escaped this one
                    escaped = False
                    currtok.append(char)
                    continue
            # not a quote or an escape character
            if escaped: escaped = False
            currtok.append(char)
            continue
        if enlisted and not quoted and not enbraced:
            currtok.append(char)
            if char == LBRACKET:
                brackstack.append(char)
            if char == RBRACKET:
                brackstack.pop()
                if len(brackstack) == 0:
                    enlisted = False
                    tokens.append("".join(currtok))
                    currtok = []
                    continue      
        if enbraced and not quoted and not enlisted:
            currtok.append(char)
            if char == LBRACE:
                bracestack.append(char)
            if char == RBRACE:
                bracestack.pop()
                if len(bracestack) == 0:
                    enbraced = False
                    tokens.append("".join(currtok))
                    currtok = []
                    continue      
    if currtok: tokens.append("".join(currtok))
    
    parameters = { tokens[i]: tokens[i+1] for i in range(0, len(tokens), 2) }
    for (key, val) in parameters.iteritems():
        try:
            parameters[key] = json.loads(val)
        except:
            pass
    return parameters

def tabui_drop_ui_parser(args):
    event = default_parser(args)
    field_encodings = event["field-encodings"]
    event["field-encodings"] = []
    for field_encoding in field_encodings:
        fn = field_encoding["fn"]
        field_encoding["fn"] = parse_fn(fn)
        event["field-encodings"].append(field_encoding)
    return event

def tabdoc_add_to_sheet(args):
    event = default_parser(args)
    event["fn"] = parse_fn(event["fn"])
    return event

def parse_fn(fn):
    data = {}
    match = re.match(FN_PATTERN, fn)
    if match is not None:
        table = match.group("table")    
        relation = match.group("relation")
        data["table"] = table
        data["relation"] = { "relation": relation }
        colon = relation.find(":")
        if colon < 0:
            data["relation"]["column"] = relation
            return data
        data["relation"]["aggregate"] = relation[:colon]
        rest = relation[colon+1:]
        colon = rest.find(":")
        if colon > 0:
            data["relation"]["column"] = rest[:colon]
            data["relation"]["tabscale"] = rest[colon+1:]
    return data

DEFAULT_PARSER = default_parser
ACTION_PARSERS = {
    "default": default_parser,
    "tabui:drop-ui": tabui_drop_ui_parser,
    "tabdoc:add-to-sheet": tabdoc_add_to_sheet
}
