class PropertiesLogic:
    def __init__(self, selection, propertiesView):
        self.selection = selection
        self.view = propertiesView
        self.selection.addListener(self)

    def onSelectionChanged(self):
        if self.selection.selectedObject() is not None:
            self.view.setProperties(self.selection.selectedObject().properties())

