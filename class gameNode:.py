class gameNode:
    def init(self, scoreFirst, scoreSecond, scoreBank
                 , currentValue):

        #Punktu skaita glabāšana
        self.scoreFirst  :int = scoreFirst
        self.scoreSecond :int = scoreSecond
        self.scoreBank   :int = scoreBank

        #Skaitlis
        self.currentValue :int = currentValue

        #Nākamie iespējamie soļi
        self.nodeTwo    :gameNode = None
        self.nodeThree  :gameNode = None
        self.nodeFour   :gameNode = None

        #kam ir kārta?
        #self.Turn :bool

        #self.previousNode :gameNode

        