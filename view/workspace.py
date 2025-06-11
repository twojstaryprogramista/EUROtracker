
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
import sys
from PyQt5.QtWidgets import QApplication
from view.map import MapView

class Workspace(QWidget):
    def __init__(self, initial_workspace_name, initial_workspace):
        super().__init__()
        self.__names = []
        self.__workspaces =[]
        self.add_workspace(initial_workspace_name,initial_workspace)
        self.__current_workspace = self.__workspaces[0]
        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)   
        self.__layout.addWidget(self.__current_workspace)
        self.setLayout(self.__layout)
        
    def add_workspace(self,name,workspace):
        self.__names.append(name)
        self.__workspaces.append(workspace)

    def set_workspace(self, name):
        self.__current_workspace.setParent(None)
        index = self.__names.index(name)
        workspace = self.__workspaces[index]
        self.__layout.insertWidget(0,workspace)
        self.__current_workspace=workspace

    def get_current_workspace(self):
        return self.__current_workspace
    
    def get_workspace(self,name):
        self.__current_workspace.setParent(None)
        index = self.__names.index(name)
        workspace = self.__workspaces[index]
        return workspace

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    b =QPushButton("HEHE")
    b.clicked.connect(lambda: w.set_workspace("button2"))
    w= Workspace("button",b)
    w.add_workspace("button2",MapView())
    w.show()
    sys.exit(app.exec_())

class SliderPart(Workspace):
    def __init__(self, initial_workspace_name, initial_workspace):
        super().__init__(initial_workspace_name, initial_workspace)

        
