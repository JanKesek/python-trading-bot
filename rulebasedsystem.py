from simpleindicators import SimpleIndicators as SI
import pickle
import json

si =None
def set_data_for_si(data):
    global si
    si=SI(data,25)
class RBS:
    def __init__(self):
        #si=SI(data,25)
        #obj=self.load_from_file()
        #self.returns=obj['returns']
        #self.volumereturns=obj['volumereturns']
        #self.wbb=obj['wbb']
        self.groups=[]
        #self.returns = si.returns()
        #self.volumereturns=si.volumereturns()
    def calculate_rv(self,data):
        set_data_for_si(data)
        global si
        self.returns = si.returns()
        self.volumereturns=si.volumereturns()

    def calculate_wbb(self):
        global si
        self.wbb=si.deltawbb()
        wbbdifference=len(self.returns)-len(self.wbb)
        self.returns=self.returns[wbbdifference:]
        self.volumereturns=self.volumereturns[wbbdifference:]
        self.volatilitychange=self.volatilitychange[wbbdifference:]
        #arr2=[len(arr2)-len(arr1):]
    def calculate_volatilty(self):
        global si
        self.volatilitychange=si.volatility_change()
    def start(self):
        self.classify([self.returns,self.volumereturns,self.wbb, self.volatilitychange])
        print(self.groups)
        #print(self.returns)
        #print(self.volumereturns)
        #print(self.wbb)
    def classify(self,indicators):
        for i in range(len(indicators[0])):
            dayGroup=[]
            if indicators[0][i]>400:
                dayGroup.append("Plus_C_Big")
            elif indicators[0][i]<(-400):
                dayGroup.append("Minus_C_Big")
            else:
                dayGroup.append("C_Normal")
            if indicators[1][i]>1000:
                dayGroup.append("Minus_V_Big")
            elif indicators[1][i]<(-1000):
                dayGroup.append("Plus_V_Big")
            else:
                dayGroup.append("V_Normal")
            if indicators[2][i]>0 and indicators[2][i]<50:
                dayGroup.append("Plus_WBB_Medium")
            if indicators[2][i]>=50:
                dayGroup.append("Plus_WBB_Big")
            if indicators[2][i]<=0:
                dayGroup.append("Plus_WBB_Low") 
            if indicators[3][i]>=400:
                dayGroup.append("Plus_ETA_Big")
            elif indicators[3][i]<=(-400):
                dayGroup.append("Minus_ETA_Big")
            else:
                dayGroup.append("ETA_Normal")
            self.groups.append(dayGroup)
    def save_rbs_obj_to_json(self):
        #assert(len(self.returns)==len(self.volumereturns)==len(self.wbb))
        #jsonObj=[]
        #wbbday=len(self.returns)-len(self.wbb)
        #j=0
        #if len(self.returns)!=len(self.wbb):
        #    print("UWAGA DLUGOSC TABLIC JEST ROZNA WBB {} PRICES {}".format(len(self.wbb),len(self.returns)))
        if len(self.returns)!=len(self.volatilitychange):
            print("UWAGA DLUGOSC TABLIC JEST ROZNA ETA {} PRICES {}".format(len(self.volatilitychange),len(self.returns)))
        assert(len(self.returns)==len(self.volumereturns)==len(self.volatilitychange))
        print(self.__dict__)
        with open("indicators.json", "w") as write_file:
            json.dump(self.__dict__, write_file)
        #for i in range(len(self.returns)):
        #    dic={"pricedelta":self.returns[i], "volumedelta": self.volumereturns[i]}
        #    if i>=wbbday:
        #        dic["wbbdelta"]=self.wbb[j]
        #        j+=1
         #   jsonObj.append(dic)
        
        #for price in data:
    def find_in_groups(self, group):
        k=0
        for i in range(len(self.groups)):
            for j in range(len(self.groups[0])):
                if self.groups[i][j]==group: 
                    k+=1
                   #print("FOUND {} GROUP IN DELTA VALUE {} : {}".format(group,self.returns[i],self.volatilitychange[i]))
        print("{} OCCURENCES OF GROUP {}".format(k,group))
    def load_from_file(self):
        with open('indicators.json','r') as ifile:
            objdic=json.load(ifile)
        print(objdic['returns'])
        self.returns=objdic['returns']
        self.volumereturns=objdic['volumereturns']
        self.wbb=objdic['wbb']
        self.volatilitychange=objdic['volatilitychange']
