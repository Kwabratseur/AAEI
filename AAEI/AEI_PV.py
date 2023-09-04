import AAEI, re, random
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from IPython.core.display import display, HTML
import seaborn as sns

##############----------------Chemistry processing functions----------------##############
def getNumbers( input ):
    compile = ""
    complete = []
    for letter in input:
        if compile:
            if compile.isdigit() == letter.isdigit():
                compile += letter
            else:
                complete.append( compile )
                compile = letter
        else:
            compile = letter
    if compile:
        complete.append( compile )
    numbers = [ word for word in complete if word.isdigit() ]
    strings = [ word for word in complete if not word.isdigit() ]
    return numbers, strings

def expandChemistryString(Str):
    for i in re.findall('[A-Z][a-z]*', Str):
        if Str.find(i)+1 < len(Str):
            if not Str[Str.find(i)+1].isdigit():
                Str = Str.replace(i,"{}1".format(i))
        elif not Str[Str.find(i)].isdigit():
            Str = Str.replace(i,"{}1".format(i))
    return Str

def EUAQI(NO2=50,O3=10,PM10=35,PM25=24,SO2=187): # All units ug/m3
    NO2_limits = [0, 40, 90, 120, 230, 340, 1000]
    O3_limits = [0, 50, 100, 130, 240, 380, 800]
    PM10_limits = [0, 10, 20, 25, 50, 75, 800]
    PM25_limits = [0, 20, 40, 50, 100, 150, 1200]
    SO2_limits = [0, 100, 200, 350, 500, 750, 1250]
    bin_list = [NO2_limits, O3_limits, PM10_limits, PM25_limits, SO2_limits]
    Result = [0,0,0,0,0,0]
    for i,x in enumerate([NO2,O3,PM10,PM25,SO2]):
        for j,y in enumerate(bin_list[i]):
            if x > y:
                Result[i] = j+1
    Result[-1] = max(Result)
    return Result

def EUAQIDF(df):
    O3 = Element("O3")
    CH2O = Element("CH2O")
    C10H16 = Element("C10H16")
    SO2 = Element("SO2")
    NO2 = Element("NO2")
    return EUAQI(NO2.ppbtoug(df["NO2"]),O3.ppbtoug(df["O3"]),df["PM10"],df["PM25"],SO2.ppbtoug(df["SO2"]))

def DF_Apply_EUAQI(df):
    return pd.DataFrame.from_records(df.apply(EUAQIDF,axis=1),columns=["NO2","O3","PM10","PM25","SO2","EUAQI"])

class Element(object):
    def __init__(self,formula = None, LUT="PubChemElements_all.csv", DEBUG=False):
        if formula is not None:
            self.formula = formula
        self.ChemStruct = {}
        self.Temperature = 273.15
        self.T = self.Temperature
        self.Pressure = 101325
        self.P = self.Pressure
        self.Volume = 22.41
        count = 0
        ElementaryLUT = pd.read_csv(LUT,index_col="Symbol")
        if DEBUG:
            print("Chemical formula: {}".format(self.formula))
        numbers,elements = getNumbers(expandChemistryString(self.formula))
        self.Mass = 0
        for i, x in enumerate(elements):
            self.ChemStruct[x] = ElementaryLUT.T[x]["AtomicMass"]*int(numbers[i])
            self.Mass += self.ChemStruct[x]
        if DEBUG:
            print("Molecular mass: {} U".format(self.Mass))
        
    def LMol(self):
        return self.Volume*(self.T/self.Temperature)*(self.P/self.Pressure)
    
    def setT(self,T,k=True):
        if not k:
            self.T = T + 273.15
            print("set Temperature to {} K".format(self.T))
        else:
            self.T = T
            print("set Temperature to {} K".format(self.T))
            
    def setP(self,P):
        self.P = P
        print("set pressure to {} mbar".format(self.P))
        
    def ugtoppb(self,ug):
        self.ug = ug
        self.ppb = ug/(self.Mass/self.LMol())
        return self.ppb
    
    def ppbtoug(self,pp):
        self.ppb = pp
        self.ug = pp*(self.Mass/self.LMol())
        return self.ug
    

##############----------------AQI application functions----------------##############
def norm(df):
    return df/max(df.max().values)

def df_normalize(df):
    return df/df.max()

def dfSumAggregate(df,PVTable):
    agg = 0
    for i,x in enumerate(df):
        agg += x*PVTable.T.sum()[i]
    return agg

def dfSumAggregator(df,PVTable):
    samps_norm = df_normalize(df)
    samps_norm
    samps_norm["sAgg"] = df_normalize(samps_norm.apply(dfSumAggregate, axis=1 ,args=(PVTable,)))
    return samps_norm

def dfScaledImpact(df,df_norm,PVTable):
    for i, x in enumerate(df):
        df[i] = 1+(df_norm["sAgg"][i])*df[i]*PVTable.T.sum()[df.name]
    df.name = "{}_sI".format(df.name)
    return df

def impactSampling(df,PVTable):
    df_norm = dfSumAggregator(df,PVTable)
    preRes = df_norm[df.columns].apply(dfScaledImpact, args=(df_norm,PVTable))
    normStats = preRes.describe().drop(["count","25%","50%","75%"])
    Result = norm(preRes)
    cols = []
    for i,x in enumerate(Result.columns):
        cols.append("{}_AEI".format(x))
    Result.columns = cols
    Result = pd.concat([df,Result,df_norm["sAgg"]],axis=1)
    stdHM(Result)
    return Result, normStats

def sort(df,colhow={}): # give dataframe, array of columns, and dict of col:method pairs where method can be True for ascending and False for descending
    dfc = pd.DataFrame()
    keys = []
    for i in colhow:
        keys.append(i)
        if colhow[i] == "NaN":
            dfc[i] = df.copy().reset_index()[keys][i]
        else:
            dfc[i] = df.copy().sort_values(by=i,ascending=colhow[i]).reset_index()[keys][i]
        dfc = dfc.reset_index()[keys]
    return dfc

##############----------------AQIEQ application functions----------------##############
def directInverser(df,invStats,hf,PVTable,target=None):
    Name = df.name.split("_")[0]
    if target == None:
        target = Name
    return ((df*PVTable.T.sum()[target]/hf)*((invStats[target]["std"]*0.9) + invStats[Name]["std"]*0.1)) + invStats[target]["mean"]


##############----------------Supporting functions----------------##############
def sampleGenerator(species,samples):
    #generates samples in the desired format. Takes dictionary with dictionaries which indicate the range of values to be generated. 
    Dictionary = {}
    
    for i in species:
        Min = species[i]["min"]
        Max = species[i]["max"]
        s = []
        for j in range(samples):
            s.append(random.uniform(Min,Max))
        Dictionary[i] = s
    return pd.DataFrame.from_dict(Dictionary)

def stdHM(df): #standardized heatmap
    sns.heatmap(df, annot=True)
    
# NO2_limits = [0, 40, 90, 120, 230, 340, 1000]
# O3_limits = [0, 50, 100, 130, 240, 380, 800]
# PM10_limits = [0, 10, 20, 25, 50, 75, 800]
# PM25_limits = [0, 20, 40, 50, 100, 150, 1200]
# SO2_limits = [0, 100, 200, 350, 500, 750, 1250]

def runFcnDemo():# it vorks
    Nice_Col_Order = ["NO2","NO2_AEI","O3","O3_AEI","PM10","PM10_AEI","PM25","PM25_AEI","SO2","SO2_AEI","EUAQI","sAgg","CO2_AEI","CH2O_AEI","C10H16_AEI"]
    sampleInstantiator = {"C10H16":{"min":0,"max":66872},
                      "CH2O":{"min":0,"max":1339},
                      "O3":{"min":0,"max":300},
                      "NO2":{"min":0,"max":300},
                      "SO2":{"min":0,"max":800},
                      "PM10":{"min":0,"max":150},
                      "PM25":{"min":0,"max":200},
                      "CO2":{"min":4000000,"max":500000}}
    entries= {"PM10":["O3",0.3330015744489429],"PM25":["O3",0.6382530176938073]}
    merge="CH3CHO,C10H16O2,C8H14O-Cprod"
    MetaBlobs, TargetBlobs, analogBlobs, PVTable, target_DF = AAEI.BatchReport(["genra_C10H16",
                                                                                "genra_CH2O",
                                                                                "genra_O3",
                                                                                "genra_SO2",
                                                                                "genra_NO2",
                                                                                "genra_CO2"],
                                                                                entries=entries,
                                                                                filename="Batch_Report")
    df = sampleGenerator(sampleInstantiator,10)
    #df = sort(df,{"C10H16":True,"CH2O":False,"O3":False,"SO2":True,"NO2":False,"CO2":True,"PM10":"NaN","PM25":"NaN"})
    invStats = df.describe().drop(["count","25%","50%","75%"])
    res, normStats =impactSampling(df,PVTable)
    plt.savefig("Calculated_DynAEI_hm.png")
    res.T.iloc[len(df.T):len(df.T)*2].T.apply(directInverser, args=(invStats,res["sAgg"],PVTable)).plot(logy=True) # plot normalized recovered sets
    plt.savefig("Recovered_Concentration_DynAEI.png")
    df.plot(logy=True)
    plt.savefig("Original_Samples.png")
    res.T.iloc[len(df.T):len(df.T)*2].T.apply(directInverser, args=(invStats,res["sAgg"],PVTable,"O3")).plot(logy=True)
    plt.savefig("O3_eq_DynAEI.png")
    res.T.iloc[len(df.T):len(df.T)*2].T.apply(directInverser, args=(invStats,res["sAgg"],PVTable,"CH2O")).plot(logy=True)
    plt.savefig("CH2O_eq_DynAEI.png")
    res.T.iloc[len(df.T):len(df.T)*2].T.apply(directInverser, args=(invStats,res["sAgg"],PVTable,"C10H16")).plot(logy=True)
    plt.savefig("C10H16_eq_DynAEI.png")
    res.T.iloc[len(df.T):len(df.T)*2].T.apply(directInverser, args=(invStats,res["sAgg"],PVTable,"CO2")).plot(logy=True)
    plt.savefig("CO2_eq_DynAEI.png")
    
    euaqi = DF_Apply_EUAQI(df)
    euaqi.plot()
    plt.savefig("calculated_EUAQI.png")
    pd.concat([(res.T.iloc[8:].T*7),pd.DataFrame.from_records(euaqi)],axis=1)[Nice_Col_Order].plot(logy=True)
    plt.savefig("Compared_EUAQI_DynAEI_line.png")
    plt.clf()
    stdHM(pd.concat([(res.T.iloc[8:].T*7),pd.DataFrame.from_records(euaqi)],axis=1)[Nice_Col_Order])
    plt.savefig("Compared_EUAQI_DynAEI_hm.png")
    
    
    
    
#runFcnDemo()