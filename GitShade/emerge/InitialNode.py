class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __dict__(self):
        return {"x": self.x, "y": self.y}


class Data:
    def __init__(self, icon="CaretDownFill", label="None"):
        self.icon = icon
        self.label = label

    def __dict__(self):
        return {"icon": self.icon, "label": self.label}
    
class Style:
    def __init__(self, height=0, width=0):
        self.height = height
        self.width = width

    def __dict__(self):
        return {"height": self.height, "width": self.width}


class InitialNode:
    def __init__(self, id='', position=Position(), type="custom", data=Data(), parentNode="box", extent="parent", style=Style(), hidden=True):
        self.id = id
        self.position = position
        self.type = type
        self.data = data
        self.parentNode = parentNode
        self.extent = extent
        self.style = style
        self.hidden = hidden
    
    def getType(self):
        return self.type

    def __dict__(self):
            return {
                "id": self.id,
                "position": self.position.__dict__(),
                "type": self.type,
                "data": self.data.__dict__(),
                "parentNode": self.parentNode,
                "extent": self.extent,
                "style": self.style.__dict__(),
                "hidden": self.hidden
            }

