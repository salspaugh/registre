import copy
import logging
import re
import shelf

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

IGNORE = [
   "tabui:save-workbook",
   "tabdoc:resize-cell",
   "tabdoc:resize-header",
   "tabui:scroll-sheet",
   "tabui:upgrade-datasources-ui",
   "tabui:connect-datasource",
   "tabui:connection-edit-connection-ui",
   "tabdoc:extract",
   "tabdoc:move-dashboard-edge",
   "tabdoc:pane-zoom-factor",
   "tabui:document"
]
    
PASTED = re.compile("(?P<basename>.*) \([\d]+\)")

class Sheet(object):
    
    def __init__(self, name, counter, is_dashboard=False):
        self.name = name
        self.counter = counter
        self.is_dashboard = is_dashboard
        self.graphtype = None

    def __str__(self):
        return self.name


class Context(object):
    """
    Current state of the Tableau application based on a stream of log events.
    """

    def __init__(self, id, last_activity=None, next_activity=None, noop=False,
                sheets=None, shelves=None, dashboards=None):
        self.id = id
        self.last_activity = last_activity
        self.next_activity = next_activity
        self.noop = noop
        self.current_sheet = None # This is most often wrong.
        self.deleted_sheets = 0 # We don't know which sheet is deleted so this is the best we can do.
        self.sheets = [] if sheets is None else sheets
        # Note: extra wrong sheets are created because we don't know exactly what is duplicated.
        self.shelves = [] if shelves is None else shelves
        self.dashboards = [] if dashboards is None else dashboards
        self._sheet_counter = 0
        self._dashboard_counter = 0
        self._clipboard = None
        self._undo_target = None
        self._parent = None
        self._child = None
        self._apply = {
            "tabui:drop-ui": self.apply_tabui_drop_ui,
            "tabdoc:add-to-sheet": self.apply_tabdoc_add_to_sheet,
            "tabui:connection-analyze-data-ui": self.apply_tabui_connection_analyze_data_ui,
            "tabui:new-worksheet-ui": self.apply_tabui_new_worksheet_ui,
            "tabui:duplicate-sheet-ui": self.apply_tabui_duplicate_sheet_ui,
            "tabui:duplicate-sheet-or-crosstab-ui": self.apply_tabui_duplicate_sheet_or_crosstab_ui, 
            "tabui:export-workbook-sheets-ui": self.apply_tabui_export_workbook_sheet_ui,
            "tabui:paste": self.apply_tabui_paste,
            "tabdoc:rename-sheet": self.apply_tabdoc_rename_sheet,
            "tabdoc:undo": self.apply_tabdoc_undo,
            "tabdoc:redo": self.apply_tabdoc_redo,
            "tabui:new-dashboard-ui": self.apply_tabui_new_dashboard_ui,
            "tabdoc:drop-on-dashboard": self.apply_tabdoc_drop_on_dashboard,
            "tabui:delete-sheet-ui": self.apply_tabui_delete_sheet_ui,
            #"tabdoc:show-me": self.tabdoc_show_me,
            #"tabdoc:select-legend-item": "",
            #"tabui:change-aggregation-ui": "",
            #"tabdoc:remove-fields": "",
            #"tabdoc:highlight": ""
            #"tabdoc:add-to-sheet-ui": self.apply_tabdoc_add_to_sheet_ui, # adds col to sheet on right click, possible missing info
            #"tabdoc:add-to-sheet": self.apply_tabdoc_add_to_sheet # adds col to sheet on double click
        }
        self._apply.update({ event: self.apply_ignore for event in IGNORE })

    def __repr__(self):
        return "Context(%d, last_activity=%s, next_activity=%s, noop=%s)" % (self.id, str(self.last_activity), str(self.next_activity), str(self.noop))

    def __str__(self):
        parent_id = child_id = -1
        parent_action = child_action = "--"
        if self._parent is not None:
            parent_id = self._parent.id
            if self._parent.last_activity is not None:
                parent_action = self._parent.last_activity["action"]
        if self._child is not None:
            child_id = self._child.id
            if self._child.last_activity is not None:
                child_action = self._child.last_activity["action"]
        action = self.last_activity["action"] if self.last_activity is not None else "--"
        return "({:4} {:36} [{:4} {:36}] {:4} {:36}) {}".format(
            parent_id, parent_action, 
            self.id, action, 
            child_id, child_action, 
            str(self._undo_target))

    def apply(self, activity):
        self.next_activity = activity
        child = Context(self.id+1, last_activity=activity, 
            sheets=copy.deepcopy(self.sheets), shelves=copy.deepcopy(self.shelves), 
            dashboards=copy.deepcopy(self.dashboards))
        self._child = child
        child._parent = self
        child._undo_target = self.id
        child._sheet_counter = self._sheet_counter
        child._dashboard_counter = self._dashboard_counter
        child._clipboard = self._clipboard 
        self._apply.get(activity["action"], self.apply_default)(child, activity)
        return child
    
    def apply_tabdoc_undo(self, child, activity):
        target = self.get_undo_target()
        child.copy_state(target)
       
    def get_undo_target(self):
        target = self._undo_target
        curr = self
        while curr.id > target: curr = curr._parent
        return curr 

    def copy_state(self, target):
        # Because we want to maintain true activity record including undos?
        #self.last_activity = copy.deepcopy(target.last_activity)
        #self.next_activity = copy.deepcopy(target.next_activity)
        self.noop = copy.deepcopy(target.noop)
        self.current_sheet = copy.deepcopy(target.current_sheet)
        self.deleted_sheets = copy.deepcopy(target.deleted_sheets)
        # Because undo-ing doesn't undo creation of a sheet?
        #self.sheets = copy.deepcopy(target.sheets)
        #self.sheets = copy.deepcopy(target.dashboards)
        #self._sheet_counter = copy.deepcopy(target._sheet_counter)
        self.shelves = copy.deepcopy(target.shelves)
        self._undo_target = copy.deepcopy(target._undo_target)

    def apply_tabdoc_redo(self, child, activity):
        target = self.get_redo_target()
        child.copy_state(target)
   
    def get_redo_target(self):
        target = self._undo_target + 2
        curr = self
        while curr.id > target: curr = curr._parent
        return curr

    def apply_default(self, child, activity):
        logger.warning("No apply function for %s" % activity["action"])
        if "parameters" in activity:
            logger.warn("%s has parameters: %s" % (activity["action"], activity["parameters"]))
        child.noop = True

    def apply_ignore(self, child, activity):
        logger.info("Ignoring %s event" % activity["action"])
        if "parameters" in activity:
            logger.warn("%s has parameters: %s" % (activity["action"], activity["parameters"]))
        child.noop = True
    
    def append_sheet(self, sheet_to_append):
        matching_sheets = filter(lambda s: s.name == sheet_to_append.name, self.sheets)
        if len(matching_sheets) > 0:
            curr_sheets = ", ".join([s.name for s in self.sheets])
            logger.error("Sheet already exists: %s. Current sheets: %s" % (sheet_to_append.name, curr_sheets))
            assert len(matching_sheets) == 1
            # We can assume it was supposed to have been deleted?
            match = matching_sheets[0]
            self.sheets.remove(match)            
            for shelved in self.shelves: # TODO: Make sure all shelved items have a sheet!
                if shelved.sheet is not None and shelved.sheet.name == match.name:
                    self.shelves.remove(shelved) # Remove the shelved items too.
        self.sheets.append(sheet_to_append)
    
    def append_dashboard(self, dashboard_to_append):
        matching_dashboards = filter(lambda s: s.name == dashboard_to_append.name, self.dashboards)
        if len(matching_dashboards) > 0:
            curr_dashboards = ", ".join([s.name for s in self.dashboards])
            logger.error("Dashboard already exists: %s. Current dashboards: %s" % (dashboard_to_append.name, curr_dashboards))
            assert len(matching_dashboards) == 1
            # We can assume it was supposed to have been deleted?
            match = matching_dashboards[0]
            self.dashboards.remove(match)            
        self.dashboards.append(dashboard_to_append)

    def apply_tabui_connection_analyze_data_ui(self, child, activity):
        child._sheet_counter += 1
        sheet = Sheet("Sheet %d" % child._sheet_counter, child._sheet_counter)
        child.append_sheet(sheet)
        child.current_sheet = sheet
        
    def remove_shelved(self, shelved):
        # TODO

    def move_shelved(self, shelved):
        # TODO

    def apply_tabui_drop_ui(self, child, activity):
        shelved = shelf.Shelved(activity)
        if shelved.was_removed():
            child.remove_shelved(shelved)
        elif shelved.was_moved():
            child.move_shelved(shelved)
        else:
            placed = False
            for sheet in self.sheets:
                if sheet.name == shelved.target_sheet:
                    shelved.sheet = sheet
                    placed = True
            if not placed:
                logger.error("No such sheet found: %s" % shelved.target_sheet)
            child.shelves.append(shelved)

    def apply_tabdoc_add_to_sheet(self, child, activity):
        self.apply_tabui_drop_ui(child, activity)

    def apply_tabui_new_worksheet_ui(self, child, activity):
        child._sheet_counter += 1
        sheet = Sheet("Sheet %d" % child._sheet_counter, child._sheet_counter)
        child.append_sheet(sheet)
        child.current_sheet = sheet

    def apply_tabui_duplicate_sheet_ui(self, child, activity):
        # We have to duplicate both sheets and dashboards because we don't know what was duplicated.
        # Whatever is duplicated, we don't have the correct shelves on.
        child._sheet_counter += 1
        sheet = Sheet("Sheet %d" % child._sheet_counter, child._sheet_counter)
        child.append_sheet(sheet)
        child._dashboard_counter += 1
        dashboard = Sheet("Dashboard %d" % child._dashboard_counter, child._dashboard_counter, is_dashboard=True)
        child.append_sheet(dashboard) # Append to sheets or dashboards? Both because we don't always know if something is a dashboard or sheet?
        child.append_dashboard(dashboard)
        child.current_sheet = sheet
    
    def apply_tabui_duplicate_sheet_or_crosstab_ui(self, child, activity):
        # TODO: Find out if this is different from the function called due to
        #       version difference.
        self.apply_tabui_duplicate_sheet_ui(child, activity)

    def apply_tabui_export_workbook_sheet_ui(self, child, activity):
        use_clipboard = bool(activity["parameters"]["use-clipboard"])
        if use_clipboard: # TODO: Figure out how to handle multiple source worksheets.
            child._clipboard = activity["parameters"]["source-worksheets"][0]

    def apply_tabui_paste(self, child, activity):
        basename = sheet._clipboard
        matches = PASTED.match(sheet._clipboard)
        if matches is not None:
            basename = matches.group("basename")
        n = 0
        for sheet in child.sheets:
            if PASTED.match(sheet.name) is not None:
                n += 1
        k = n + 1
        child._sheet_counter += 1
        sheet = Sheet("%s (%d)" % (basename, k), child._sheet_counter)
        for shelved in child.shelves:
            if shelved.sheet.name == self._clipboard:
                new_shelved = copy.deepcopy(shelved)
                new_shelved.sheet = sheet
                child.shelves.apppend(new_shelved)
        child.append_sheet(sheet)

    def apply_tabdoc_rename_sheet(self, child, activity):
        old_sheet_name = activity["parameters"]["sheet"]
        new_sheet_name = activity["parameters"]["new-sheet"]
        found = False
        for sheet in child.sheets:
            if sheet.name == old_sheet_name:
                sheet.name = new_sheet_name
                found = True
        if not found:
            raise ValueError("No such sheet: %s. Current sheets: %s" % (sheet_to_remove.name, curr_sheets))
        set_active = bool(activity["parameters"]["set-active"])
        if set_active:
            child.current_sheet = new_sheet

    def apply_tabui_delete_sheet_ui(self, child, activity):
        child.deleted_sheets += 1

    def apply_tabui_new_dashboard_ui(self, child, activity):
        child._dashboard_counter += 1
        dashboard = Sheet("Dashboard %d" % child._dashboard_counter, child._dashboard_counter, is_dashboard=True)
        child.append_sheet(dashboard)
        child.append_dashboard(dashboard)

    def apply_tabdoc_drop_on_dashboard(self, child, activity):
        dashboard_name = activity["parameters"].get("worksheet", None)
        if dashboard_name is not None:
            dashboard = Sheet(dashboard_name, -1, is_dashboard=True)
            child.append_sheet(dashboard)
            child.append_dashboard(dashboard)

    def apply_tabdoc_show_me(self, child, activity):
        # TODO: Finish me.
        graph_type = activity["parameters"]["show-me-command-type"] 
        sheet = activity["parameters"]["worksheet"]

def generate_contexts(activities):
    contexts = []
    curr_context = Context(0)
    for activity in activities:
        curr_context = curr_context.apply(activity)
        logging.info("Context: %s" % str(curr_context))
        if curr_context.id > 0:
            assert curr_context._parent is not None
        contexts.append(curr_context)
    return contexts

