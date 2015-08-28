
#### Overview

This project contains code to parse user activity from Tableau logs and analyze it.

It is written in Python and supports analyzing logs from Tableau version 8.2 or later.

#### Terminology

*registre log*: A file containing a list of JSON objects separated by newlines (to follow the convention set by Tableau logs).
Each object is a dictionary describing the user's action and additional information.

*Tableau event key*: Tableau logs consist of list of JSON objects separated by newlines. Each event has a key "k" describing what type of event it is.
User interaction is primarily recorded in "command-pre" events which are written when the user initiates certain actions (equivalently "command-post" events, which seem to be identical, but output when the command completes).

#### Navigating

* `datasets/` data given to participants to explore in pilot study
* `info/` data about the logs
* `registre/` main Python modules
  * `actions.py` parse Tableau log "command-pre" event parameters 
  * `graph.py` plot registre logs as Markov diagrams
  * `map.py` parse Tableau log files and output registre log files
  * `read.py` read registre log files
  * `tableaukeys.py` list of Tableau event keys that are not of interest
* `scripts/` scripts running registre code -- good source of examples on how to use it
* `test/` the start of a set of tests for testing the registre module

#### Dependencies

* Python 2.7 (other versions might work but are untested)
* pygraphviz (version ?)

#### Use

See the scripts in the `scripts` directory for an example of how to run the code. Alternatively, some of the modules are executable as scripts and print out help when given the `-h` option.

#### Contributing

1. If you want to add a feature, follow the instructions on contributing code in the wiki.
2. If you want to request a feature or report a bug, create a new issue. Search the issue list first to make sure your idea isn't already there.
