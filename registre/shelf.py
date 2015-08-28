def is_tabui_dropui(activity):
    return activity["action"] == "tabui:drop-ui"

def is_tabdoc_add_to_sheet(activity):
    return activity["action"] == "tabdoc:add-to-sheet"

def extract_description(activity):
    if is_tabui_dropui(activity):
        return activity["parameters"]["drag-description"]

def extract_source(activity):
    if is_tabui_dropui(activity):
        return activity["parameters"]["drag-source"]

def extract_target(activity):
    if is_tabui_dropui(activity):
        return activity["parameters"]["drop-target"]

def extract_is_copy(activity):
    if is_tabui_dropui(activity):
        return activity["parameters"]["is-copy"]

def extract_is_dead_drop(activity):
    if is_tabui_dropui(activity):
        return activity["parameters"]["is-dead-drop"]

def extract_is_right_drag(activity):
    if is_tabui_dropui(activity):
        return activity["parameters"]["is-right-drag"]

def extract_source_sheet(activity):
    if is_tabui_dropui(activity):
        return activity["parameters"].get("source-sheet", None)

def extract_target_sheet(activity):
    if is_tabui_dropui(activity):
        return activity["parameters"].get("target-sheet", None)

def extract_drop_context(activity):
    if is_tabui_dropui(activity):
        return activity["parameters"]["shelf-drop-context"]

def extract_selection(activity):
    if is_tabui_dropui(activity):
        return activity["parameters"].get("shelf-selection", None)

def extract_target_type(activity):
    if is_tabui_dropui(activity):
        shelf_drop_target = activity["parameters"]["shelf-drop-target-position"]
        return shelf_drop_target.get("shelf-type", None)

def extract_target_pos(activity):
    if is_tabui_dropui(activity):
        shelf_drop_target = activity["parameters"]["shelf-drop-target-position"]
        return shelf_drop_target.get("shelf-pos-index", None)

def extract_source_type(activity):
    if is_tabui_dropui(activity):
        shelf_drag_source = activity["parameters"]["shelf-drag-source-position"]
        return shelf_drag_source.get("shelf-type", None)

def extract_source_pos(activity):
    if is_tabui_dropui(activity):
        shelf_drag_source = activity["parameters"]["shelf-drag-source-position"]
        return shelf_drag_source.get("shelf-pos-index", None)

def extract_source_action(activity):
    if is_tabui_dropui(activity):
        shelf_drag_source = activity["parameters"]["shelf-drag-source-position"]
        return shelf_drag_source.get("shelf-drop-action", None)

def extract_aggregates(activity):
    if is_tabui_dropui(activity): 
        field_encodings = activity["parameters"]["field-encodings"]
        relations = [fe["fn"]["relation"] for fe in field_encodings]
        return [r.get("aggregate", None) for r in relations]
    if is_tabdoc_add_to_sheet(activity):
        return activity["parameters"]["fn"].get("aggregate", None) 

def extract_base_columns(activity):
    if is_tabui_dropui(activity):
        field_encodings = activity["parameters"]["field-encodings"]
        relations = [fe["fn"]["relation"] for fe in field_encodings]
        return [r.get("column", r["relation"]) for r in relations]
    if is_tabdoc_add_to_sheet(activity):
        fn = activity["parameters"]["fn"]
        return fn.get("column", fn["relation"]) 

def extract_column_types(activity):
    if is_tabui_dropui(activity):
        field_encodings = activity["parameters"]["field-encodings"]
        relations = [fe["fn"]["relation"] for fe in field_encodings]
        return [r.get("tabscale", None) for r in relations]
    if is_tabdoc_add_to_sheet(activity):
        return activity["parameters"]["fn"].get("tabscale", None) 

class Shelved(object):

    def __init__(self, activity):
        self.activity = activity

        self.is_drop_ui = activity["action"] == "tabui:drop-ui"
        self.is_add_to_sheet = activity["action"] == "tabdoc:add-to-sheet"

        # "parameters"
        self.description = extract_description(activity)
        self.source = extract_source(activity)
        self.target = extract_target(activity)

        self.is_copy = extract_is_copy(activity)
        self.is_dead_drop = extract_is_dead_drop(activity)
        self.is_right_drag = extract_is_right_drag(activity)

        self.source_sheet = extract_source_sheet(activity)
        self.target_sheet = extract_target_sheet(activity)
        self.drop_context = extract_drop_context(activity)
        self.selection = extract_selection(activity)

        # "shelf-drag-source-position"
        self.source_type = extract_source_type(activity)
        self.source_pos = extract_source_pos(activity)
        self.source_action = extract_source_action(activity)
        
        # "shelf-drop-target-position"
        self.target_type = extract_target_type(activity)
        self.target_pos = extract_target_pos(activity)
        
        # "field-encodings":
        self.aggregates = extract_aggregates(activity)
        self.base_columns = extract_base_columns(activity)
        self.column_tableau_types = extract_column_types(activity)
        
        self.sheet = None
        
    def was_removed(self):  
        return (
            self.is_drop_ui and
            self.source == "drag-drop-viz" and 
            self.target == "drag-drop-none") 

    def was_moved(self):
        return (
            self.is_drop_ui and 
            self.source == "drag-drop-viz" and 
            self.target == "drag-drop-viz") 



