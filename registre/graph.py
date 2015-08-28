import itertools
import pygraphviz as pgv
import map
import read

START_TOKEN = "start"
END_TOKEN = "end"
NEGLIGIBLE = "negligible"
LABEL_LENGTH = 14
THRESHOLD = .2

GRAPH_ATTRS = {
    "directed": True,
    "rankdir": "LR"
}

NODE_ATTRS = {
    "color": "",
    "style": "",
    "shape": "circle",
    "height": "1.2",
    "fontname": "Bitstream Vera Sans",
    "fontsize": 8
}

EDGE_ATTRS = {
    "fontsize": 16,
    "fontname": "Bitstream Vera Sans"
}

def graph_activity(activities, output, normalize=True, threshold=THRESHOLD):
    graph, start, end = make_activity_graph(activities, normalize=normalize)
    draw_graph(graph, start, end, output, threshold)

def draw_graph(graph, start, end, output, threshold):
    plot = pgv.AGraph(**GRAPH_ATTRS)
    seen = set()
    has_incoming = set()
    has_outgoing = set()

    # Add nodes.
    for src in graph.iterkeys():
        seen.add(src)
        add_node(plot, src, start=start, end=end)

    # Add edges.
    for (src, dstdict) in graph.iteritems():
        for (dst, weight) in dstdict.iteritems():
            if weight < threshold: continue
            if dst not in seen:
                seen.add(dst)
                add_node(plot, dst, start=start, end=end)
            if not src == dst:
                has_incoming.add(dst)
                has_outgoing.add(src)
            add_edge(plot, src, dst, weight)

    # Make sure all edges have an incoming and outgoing edge.
    for node in seen:
        if node not in has_incoming and node != start:
            srcs = {}
            for (src, dsts) in graph.iteritems():
                for (dst, weight) in dsts.iteritems():
                    if dst == node and not src == dst:
                        srcs[src] = weight
            if len(srcs) > 0:
                s = sorted(srcs.items(), key=lambda x: x[1], reverse=True)[0][0]
                add_edge(plot, s, node, NEGLIGIBLE)
        if node not in has_outgoing and node != end:
            dsts = graph.get(node, None)
            dsts = sorted(dsts.items(), key=lambda x: x[1], reverse=True)
            dsts = filter(lambda x: x[0] != node, dsts)
            d = dsts[0][0]
            add_edge(plot, node, d, NEGLIGIBLE)

    plot.draw(output, prog="dot") 

def add_node(graph, node, start=None, end=None):
    color = NODE_ATTRS["color"]
    style = NODE_ATTRS["style"] 
    if node == start:
        color = '#74c476' # green
        style = "filled"
    if node == end:
        color = '#ef6548' # red
        style = "filled"
    graph.add_node(n=wrap_text(node), 
        style=style,
        color=color,    
        shape=NODE_ATTRS["shape"],
        height=NODE_ATTRS["height"],
        fontname=NODE_ATTRS["fontname"], 
        fontsize=NODE_ATTRS["fontsize"])

def wrap_text(text):
    wrapped = ""
    rest = text
    while len(rest) > LABEL_LENGTH:
        wrapped += rest[:LABEL_LENGTH] + "\n" 
        rest = rest[LABEL_LENGTH:]
    wrapped += rest
    return wrapped

def add_edge(graph, src, dst, weight):
    linewidth = str(float(weight)*5) if weight <= 1 else "1" 
    if weight == NEGLIGIBLE:
        graph.add_edge(wrap_text(src), wrap_text(dst), 
        label=weight,
        fontname=EDGE_ATTRS["fontname"], 
        fontsize=EDGE_ATTRS["fontsize"],
        style="dotted")
    else:
        graph.add_edge(wrap_text(src), wrap_text(dst),
        label="%.2f" % weight, 
        fontname=EDGE_ATTRS["fontname"], 
        fontsize=EDGE_ATTRS["fontsize"],
        style="setlinewidth("+linewidth+")")

def make_activity_graph(activities, normalize):
    graph = {}
    start = activities[0]["action"]
    end = activities[-1]["action"]
    for idx, activity in enumerate(activities[:-1]):
        src = activity["action"]
        dst = activities[idx+1]["action"]
        if not src in graph:
            graph[src] = {}
        if not dst in graph[src]:
            graph[src][dst] = 0.
        graph[src][dst] += 1.
    if normalize:
        for (src, dstdict) in graph.iteritems():
            total = float(sum(dstdict.values()))
            for (dst, weight) in dstdict.iteritems():
                graph[src][dst] = weight * 1. / total
    return graph, start, end

if __name__ == "__main__":
    import argparse
    DEFAULT_GRAPH = "graph.pdf"
    parser = argparse.ArgumentParser("Create state machine graph from Tableau or Registre log.")
    parser.add_argument("-t", "--tableaulog",
                        help="path to the Tableau log file to parse")
    parser.add_argument("-r", "--registrelog",
                        help="path to the Tableau log file to parse")
    parser.add_argument("-o", "--output",
                        help="path to the graph to output (default is %s)" % DEFAULT_GRAPH)
    parser.add_argument("-n", "--normalize", action="store_true",
                        help="whether to normalize the edge weights to be frequencies rather than counts")
    args = parser.parse_args()
    if args.tableaulog is None and args.registrelog is None:
        raise RuntimeError("You must provide an input file.")
        parser.print_help()
    if args.tableaulog is not None and args.registrelog is not None:
        raise RuntimeError("Please provide only one input.")
        parser.print_help()
    if args.output is None:
        args.output = DEFAULT_GRAPH
   
    activity_gen = map.parse_tableau_log(args.tableaulog) if args.tableaulog else read.read_registre(args.registrelog) 
    activities = [activity for activity in activity_gen]
    graph_activity(activities, args.output, normalize=args.normalize) 
