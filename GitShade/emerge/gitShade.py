from GitShade.emerge.InitialNode import Position,Data,InitialNode,Style
from GitShade.emerge.Edges import Edge
import json
class gitShade:
    def __init__(self, graphRootNode="src"):
        # set root node easier computation
        self._graphRootNode: str = graphRootNode
        # making nodes and edges of graph 
        self._gitShadeResult: dict[str, list[str]] = {}
        self._graphInitNodes: list[InitialNode] = []
        self._graphEdges: list[Edge] = []
        # used for assigning dynamic height and width for each folder
        self._graphAdjListFolders: dict[str,list[str]] = {}
        self._graphAdjListFiles: dict[str,list[str]] = {}
    
    def structurize_basicFormat(self, _result:any):
        for item in _result.items():
            depd = str(item[1])
            depdList = []
            start = -1
            end = -1
            for ele in range(0,len(depd)):
                if depd[ele] == '[':
                    start = ele
                elif depd[ele] == ']':
                    end = ele
            depd = depd[start+1:end]
            depdList = depd.split(", ")
            for dependency in depdList:
                dependency = dependency[1:len(dependency)-1]
            self._gitShadeResult[item[0]] = depdList
    
    def structurize_desiredFormat(self, _rootNode: str):
        # structuring json data for gitShade
        folderDict: dict[str,str] = {}
        EdgeIds = 1
        for item in self._gitShadeResult.items(): 
            keys: list = item[0].split("/")
            position = Position()
            data = Data("CaretDownFill",keys[len(keys)-1])
            boxList : list = []
            # making folder objects
            parentNode = None
            for key in range(0,len(keys)-1):
                if folderDict.get(keys[key]) != None:
                    parentNode = keys[key]
                    continue
                boxNode: InitialNode = InitialNode(keys[key],position,"group",Data("CaretDownFill",keys[key]),parentNode,"parent",Style())
                folderDict[keys[key]]=keys[key]
                parentNode = keys[key]
                self._graphInitNodes.append(boxNode)
                boxList.append(boxNode)
            
            initial_node = InitialNode(item[0], position, "custom", data, parentNode)
            self._graphInitNodes.append(initial_node)
            for edge in item[1]:
                if len(edge)!= 0 and (len(edge.split("/")) == 1 or edge[1] == "@"):
                    boxNode: InitialNode = InitialNode(edge[1:len(edge)-1],position,"custom",Data("CaretDownFill",edge[1:len(edge)-1]),"modules","parent",Style())
                    self._graphInitNodes.append(boxNode)
                if edge[1:len(edge)-1] != "" and edge[1:len(edge)-1].startswith(_rootNode) == True:
                    initialEdge = Edge(EdgeIds,item[0],edge[1:len(edge)-1])
                    self._graphEdges.append(initialEdge)
                    EdgeIds = EdgeIds + 1
        self._graphInitNodes.append(InitialNode("modules",Position(),"group",Data(),None,"parent",Style()))
        
    def exportDataToFile(self):
        json_data_initNodes = json.dumps(gitShade.convertToDict(self._graphInitNodes))
        json_data_Edges = json.dumps(gitShade.convertToDict(self._graphEdges))
        print('came here')
        print(json_data_initNodes)
        f = open("/tmp/initNodes.json", "w")
        f.write(json_data_initNodes)
        f = open("/tmp/initEdges.json","w")
        f.write(json_data_Edges)
        f.close()
    
    def calculate_dimensions(self):
        self.create_graphAdjListFolders()
        self.create_graphAdjListFilesInFolder()
        #self.calculate_HeightWidh(self._graphRootNode)
        self.make_parentAndChilds_hidden_false()
        self.exportDataToFile()
        pass

    def calculate_HeightWidh(self, rootNode: str):
        #base condition
        if len(self._graphAdjListFolders[rootNode]) == 0:
            return self.calculate_relativeHeight(rootNode)
        
        hht = 1
        wht = 1
        # recursive condition
        for folder in self._graphAdjListFolders[rootNode]:
            hwObj = self.calculate_HeightWidh(folder)
            hht = hht + hwObj["h"]
            wht = wht + hwObj["w"]
        
        return self.calculate_relativeHeight(rootNode,hht,wht)
        
    def calculate_relativeHeight(self, rootNode:str, hht=1, wht=1):
        try:
            totalChilds = len(self._graphAdjListFiles[rootNode])
            initNodeIndex: int
            for i in range(0,len(self._graphInitNodes)):
                if self._graphInitNodes[i].id == rootNode:
                    initNodeIndex = i
                    break
            self._graphInitNodes[initNodeIndex].style.height = hht + 10*totalChilds
            self._graphInitNodes[initNodeIndex].style.width = wht + 10*totalChilds
            return {"h":hht + 10*totalChilds,"w":wht + 10*totalChilds}
        except ValueError:
            print("That item does not exist")
            return {"h":10,"w":20}
        
    def make_parentAndChilds_hidden_false(self):
        for initNode in self._graphInitNodes:
                if initNode.id == self._graphRootNode:
                    initNode.hidden = False
        
        for folder in self._graphAdjListFolders[self._graphRootNode]:
            for initNode in self._graphInitNodes:
                if initNode.id == folder and initNode.type == "group":
                    initNode.hidden = False
        
        for file in self._graphAdjListFiles[self._graphRootNode]:
            for initNode in self._graphInitNodes:
                if initNode.id == file and initNode.type == "custom":
                    initNode.hidden = False
        
    def create_graphAdjListFolders(self):
        # traversing on folders and making its graph
        for node in self._graphInitNodes:
            if node.type == "group":
                if self._graphAdjListFolders.get(node.id) == None:
                    self._graphAdjListFolders[node.id] = []
                if self._graphAdjListFolders.get(node.parentNode) == None:
                    self._graphAdjListFolders[node.parentNode] = [] 
                self._graphAdjListFolders[node.parentNode].append(node.id)
        self._graphAdjListFolders["modules"] = []

    def create_graphAdjListFilesInFolder(self):
        for node in self._graphInitNodes:
            if node.type == "group":
                for file in self._graphInitNodes:
                    if file.type == "custom" and file.parentNode == node.id:
                        if self._graphAdjListFiles.get(node.id) == None:
                            self._graphAdjListFiles[node.id] = []
                        self._graphAdjListFiles[node.id].append(file.id)

    @staticmethod
    def convertToDict(ls: list):
        result: list = []
        for item in ls:
            result.append(item.__dict__())
        return result
