import json
import registre.shelf
import unittest


class TestShelvedConstructor(unittest.TestCase):

    def setUp(self):
        drop1 = json.loads('{"action": "tabui:drop-ui", "timestamp": 1409802544.564, "parameters": {"source-sheet": "DepDelays cause ArrDelays", "shelf-drop-target-position": {"shelf-type": "rows-shelf", "shelf-pos-index": 0, "is-override": false}, "drop-target": "drag-drop-viz", "shelf-selection": [2], "drag-description": "Columns", "field-encodings": [{"encoding-type": "invalid-encoding", "fn": "[textscan.41885.855447187503].[ArrDel15 (group)]"}], "shelf-drop-context": "none", "target-sheet": "DepDelays cause ArrDelays", "is-right-drag": "false", "shelf-drag-source-position": {"shelf-type": "columns-shelf", "shelf-drop-action": "replace", "shelf-pos-index": 1, "is-override": false}, "drag-source": "drag-drop-viz", "is-copy": "false", "is-dead-drop": "false"}}')
        drop2 = json.loads('{"action": "tabui:drop-ui", "timestamp": 1409793364.019, "parameters": {"shelf-drop-target-position": {"shelf-type": "rows-shelf", "shelf-pos-index": 2, "is-override": false}, "drop-target": "drag-drop-viz", "drag-description": "", "field-encodings": [{"encoding-type": "invalid-encoding", "fn": "[On_Time_On_Time_Performance_2001_9 Extract].[sum:Calculation_6530903181331686:qk]"}], "shelf-drop-context": "none", "target-sheet": "Sheet 1", "is-right-drag": "false", "shelf-drag-source-position": {"is-override": false}, "drag-source": "drag-drop-schema", "is-copy": "false", "is-dead-drop": "false"}}')
        add1 = json.loads('{"action": "tabdoc:add-to-sheet", "timestamp": 1409802161.001, "parameters": {"fn": "[textscan.41885.855447187503].[DepDel15 (group)]"}}')
        self.drop1 = registre.shelf.Shelved(drop1)
        self.drop2 = registre.shelf.Shelved(drop2)
        self.add1 = registre.shelf.Shelved(add1)

    def test_aggregates(self):
        assert self.drop1.aggregates == [None]
        assert self.drop2.aggregates == ["sum"]
        assert self.add1.aggregates == [None]
    
    def test_base_columns(self):
        assert self.drop1.base_columns == ["ArrDel15 (group)"]
        assert self.drop2.base_columns == ["Calculation_6530903181331686"]
        assert self.add1.base_columns == ["DepDel15 (group)"]

    def test_column_tableau_types(self):
        assert self.drop1.column_tableau_types == [None]
        assert self.drop2.column_tableau_types == ["qk"]
        assert self.add1.column_tableau_types == [None]

if __name__ == '__main__':
    unittest.main()
