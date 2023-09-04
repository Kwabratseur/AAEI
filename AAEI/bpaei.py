from paraview.simple import *
from paraview.vtk.numpy_interface import dataset_adapter as dsa
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

Folders = ["STL_Var_1_inf_VH_TH_OH_LH",
           "STL_Var_2_inf_VH_TL_OL_LH",
           "STL_Var_3_std_VL_TH_OL_LH",
           "STL_Var_4_std_VH_TL_OH_LH",
           "STL_Var_5_std_VL_TL_OH_LH",
           "STL_Var_6_inf_VL_TL_OH_LH",
           "STL_Var_7_std_inf_VL_TH_OL_LL"]

#load norm_csv

layout1 = GetLayoutByName("Layout #1")


aEI_Normcsv = CSVReader(registrationName='AEI_Norm.csv', FileName=['/home/jeroen/OpenFOAM/jeroen-9/run/Thesis/AEI_Variation_cases/STL_Var_1_inf_VH_TH_OH_LH/AEI_Norm.csv'])
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024

aEI_NormcsvDisplay = Show(aEI_Normcsv, spreadSheetView1, 'SpreadSheetRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=0)

def ExportData(Folder = "STL_Var_1_inf_VH_TH_OH_LH",Filename = "var_1.foam",TS = []):
    #Load .foam
    #run aei macro code (paste in here I guess)
    #setup screens
    #make exports
    #do screen cleanup (go to base state)
    #delete everything in pipeline
    FolderName = "/home/jeroen/OpenFOAM/jeroen-9/run/Thesis/AEI_Variation_cases/"+Folder+"/"+Filename
    var_1foam = OpenFOAMReader(registrationName=Filename, FileName=FolderName)
    var_1foam.MeshRegions = ['internalMesh']
    var_1foam.CellArrays = ['C10H16', 'C10H16_0', 'CH2O', 'CH2O_0', 'CO2', 'CO2_0', 'Co', 'Cprod', 'Cprod_0', 'H2O', 'H2O_0', 'N2', 'N2_0', 'O2', 'O3', 'O3_0', 'Qdot', 'T', 'U', 'U_0', 'alphat', 'ddt0(p)', 'ddt0(p_rgh)', 'ddt0(rho)', 'ddt0(rho,C10H16)', 'ddt0(rho,CH2O)', 'ddt0(rho,CO2)', 'ddt0(rho,Cprod)', 'ddt0(rho,H2O)', 'ddt0(rho,K)', 'ddt0(rho,N2)', 'ddt0(rho,O3)', 'ddt0(rho,U)', 'ddt0(rho,epsilon)', 'ddt0(rho,h)', 'ddt0(rho,k)', 'ddtCorrDdt0(rho,U)', 'epsilon', 'epsilon_0', 'k', 'k_0', 'nut', 'p', 'p_0', 'p_rgh', 'p_rgh_0']
    GenAEI(FOAMName = Filename)

    animationScene1 = GetAnimationScene()
    animationScene1.UpdateAnimationUsingDataTimeSteps()
    renderView1 = CreateView('RenderView')
    renderView1.AxesGrid = 'GridAxes3DActor'
    renderView1.StereoType = 'Crystal Eyes'
    renderView1.CameraFocalDisk = 1.0

    aEI = FindSource('AEI')
    plotDataOverTime1 = PlotDataOverTime(registrationName='PlotDataOverTime1', Input=aEI)
    o3_AEI = FindSource('O3_AEI')
    quartileChartView1 = CreateView('QuartileChartView')
    plotDataOverTime1Display = Show(plotDataOverTime1, quartileChartView1, 'QuartileChartRepresentation')
    plotDataOverTime1Display.AttributeType = 'Row Data'
    plotDataOverTime1Display.UseIndexForXAxis = 0
    plotDataOverTime1Display.XArrayName = 'Time'
    AssignViewToLayout(view=quartileChartView1, layout=layout1, hint=0)
    plotDataOverTime1Display.SeriesVisibility = ['AEI ( block=1)']
    plotDataOverTime1Display.ShowMedian = 1
    plotDataOverTime1Display.ShowMinimum = 1
    plotDataOverTime1Display.ShowMaximum = 1
    plotDataOverTime1Display.ShowAverage = 1
    plotDataOverTime1Display.ShowRanges = 1
    plotDataOverTime1Display.ShowQuartiles = 1
    SetActiveView(quartileChartView1)
    layout1.SetSize(893, 1014)
    SaveScreenshot('/home/jeroen/OpenFOAM/jeroen-9/run/Thesis/AEI_Variation_cases/{}/AEI_{}_sot.png'.format(Folder,Filename.split(".")[0]), quartileChartView1, ImageResolution=[500, 500])


    spreadSheetView1 = FindViewOrCreate('SpreadSheetView1', viewtype='SpreadSheetView')
    SetActiveView(spreadSheetView1)
    SetActiveSource(plotDataOverTime1)
    plotDataOverTime1Display_1 = Show(plotDataOverTime1, spreadSheetView1, 'SpreadSheetRepresentation')
    ExportView('/home/jeroen/OpenFOAM/jeroen-9/run/Thesis/AEI_Variation_cases/{}/AEI_Statistics_{}.csv'.format(Folder,Filename.split(".")[0]), view=spreadSheetView1)
    SetActiveView(quartileChartView1)
    layout1.SplitVertical(2, 0.5)
    SetActiveView(None)

    quartileChartView2 = CreateView('QuartileChartView')
    AssignViewToLayout(view=quartileChartView2, layout=layout1, hint=6)
    plotDataOverTime1Display_2 = Show(plotDataOverTime1, quartileChartView2, 'QuartileChartRepresentation')
    plotDataOverTime1Display_2.AttributeType = 'Row Data'
    plotDataOverTime1Display_2.UseIndexForXAxis = 0
    plotDataOverTime1Display_2.XArrayName = 'Time'
    plotDataOverTime1Display_2.SeriesVisibility = ['C10H16_AEI ( block=1)']
    plotDataOverTime1Display_2.ShowMedian = 1
    plotDataOverTime1Display_2.ShowMinimum = 1
    plotDataOverTime1Display_2.ShowMaximum = 1
    SetActiveView(quartileChartView2)
    layout1.SetSize(893, 1014)
    SaveScreenshot('/home/jeroen/OpenFOAM/jeroen-9/run/Thesis/AEI_Variation_cases/{}/C10H16_AEI_sot_{}.png'.format(Folder,Filename.split(".")[0]), quartileChartView2, ImageResolution=[500, 500])


    plotDataOverTime1Display_2.SeriesVisibility = ['CH2O_AEI ( block=1)']
    plotDataOverTime1Display_2.ShowMedian = 1
    plotDataOverTime1Display_2.ShowMinimum = 1
    plotDataOverTime1Display_2.ShowMaximum = 1
    SetActiveView(quartileChartView2)
    layout1.SetSize(893, 1014)
    SaveScreenshot('/home/jeroen/OpenFOAM/jeroen-9/run/Thesis/AEI_Variation_cases/{}/CH2O_AEI_sot_{}.png'.format(Folder,Filename.split(".")[0]), quartileChartView2, ImageResolution=[500, 500])

    plotDataOverTime1Display_2.SeriesVisibility = ['O3_AEI ( block=1)']
    plotDataOverTime1Display_2.ShowMedian = 1
    plotDataOverTime1Display_2.ShowMinimum = 1
    plotDataOverTime1Display_2.ShowMaximum = 1
    SetActiveView(quartileChartView2)
    layout1.SetSize(893, 1014)
    SaveScreenshot('/home/jeroen/OpenFOAM/jeroen-9/run/Thesis/AEI_Variation_cases/{}/O3_AEI_sot_{}.png'.format(Folder,Filename.split(".")[0]), quartileChartView2, ImageResolution=[500, 500])

#By not selecting something, do we retain the user selection??
# create a new 'Python Calculator'

# find source

def GenAEI(CSVName='AEI_Norm.csv',FOAMName="var_1.foam",Chems = ["C10H16","CH2O","O3"]):
    aEI_normcsv = FindSource(CSVName)
    smarttinylabfoam = FindSource(FOAMName)
    Raw = servermanager.Fetch(aEI_normcsv)
    Data = dsa.WrapDataObject(Raw).RowData
    Keys = Data.keys()[1:] # Drop name column
    NameKeys = Chems# Change this when you want to solve for other and more chemicals!
    #NameKeys = input("Give comma separated chemicals to take into account:").split(",")
    ExprKeys = []# Same for this, should have similar length!
    for i in NameKeys:
        ExprKeys.append("")
    c = 0
    Calculators = []
    VariableNames = []
    Dependency = smarttinylabfoam
    for i, x in enumerate(Keys):
        for j, y in enumerate(Data[x]):
            chem = Data["Formula"].GetValue(j)
            if chem in NameKeys:
                if y > 0:
                    Calculators.append(PythonCalculator(registrationName='{}_{}_{}'.format(c,chem,x), Input=Dependency))
                    Calculators[-1].Expression = '({}/max({}))*{}'.format(chem,chem,y)
                    VariableNames.append('{}_{}_norm'.format(chem, x))
                    Calculators[-1].ArrayName = '{}_{}_norm'.format(chem, x)
                    Dependency = Calculators[-1]
                c += 1

    for i in VariableNames:
        Chem, Test, nan = i.split("_")
        for j, x in enumerate(NameKeys):
            if x == Chem:
                ExprKeys[j] += "{}+".format(i)

    AEI_chemcalc = []
    AEI_EXPR = ""
    for i, x in enumerate(ExprKeys):
        AEI_chemcalc.append(PythonCalculator(registrationName='{}_AEI'.format(NameKeys[i]), Input=Dependency))
        AEI_chemcalc[-1].Expression = "({})/6".format(x[:-1])
        AEI_EXPR += '{}_AEI+'.format(NameKeys[i])
        AEI_chemcalc[-1].ArrayName = '{}_AEI'.format(NameKeys[i])
        Dependency = AEI_chemcalc[-1]

    AEI = PythonCalculator(registrationName='AEI', Input=Dependency)
    AEI.Expression = "({})/{}".format(AEI_EXPR[:-1],len(NameKeys))
    AEI.ArrayName = 'AEI'

ExportData()

# trace generated using paraview version 5.9.1
def DeleteTreeItem(Names=None):
    if Names == None:
        Names = ['AEI','O3_AEI','CH2O_AEI','C10H16_AEI','17_O3_SUB',
                 '16_CH2O_SUB','15_C10H16_SUB','14_O3_SAC','13_CH2O_SAC','12_C10H16_SAC',
                 '8_O3_MGR','7_CH2O_MGR','6_C10H16_MGR','5_O3_DEV','4_CH2O_DEV',
                 '3_C10H16_DEV','2_O3_CHR','1_CH2O_CHR','0_C10H16_CHR']
    Oldname = Names[0]
    Oldtemp = FindSource(Oldname)
    for i, x in enumerate(Names[1:]):
        setActiveSource(Oldtemp)
        Temp = FindSource(Name)
        Delete(Oldtemp)
        del Oldtemp
        Oldtemp = Temp
        Oldname = x
    layout1 = GetLayoutByName("Layout #1")
    RemoveLayout(layout1)



def stuff():
  aEI = FindSource('AEI')
  SetActiveSource(aEI)
  plotDataOverTime1 = FindSource('PlotDataOverTime1')
  spreadSheetView1 = FindViewOrCreate('SpreadSheetView1', viewtype='SpreadSheetView')
  Hide(plotDataOverTime1, spreadSheetView1)
  quartileChartView2 = GetActiveViewOrCreate('QuartileChartView')
  Hide(plotDataOverTime1, quartileChartView2)
  quartileChartView1 = FindViewOrCreate('QuartileChartView1', viewtype='QuartileChartView')
  Hide(plotDataOverTime1, quartileChartView1)
  Delete(plotDataOverTime1)
  del plotDataOverTime1
  SetActiveSource(aEI)
  o3_AEI = FindSource('O3_AEI')
  SetActiveSource(o3_AEI)
  Delete(aEI)
  del aEI
  cH2O_AEI = FindSource('CH2O_AEI')
  SetActiveSource(cH2O_AEI)
  Delete(o3_AEI)
  del o3_AEI
  c10H16_AEI = FindSource('C10H16_AEI')
  SetActiveSource(c10H16_AEI)
  Delete(cH2O_AEI)
  del cH2O_AEI
  a17_O3_SUB = FindSource('17_O3_SUB')
  SetActiveSource(a17_O3_SUB)
  Delete(c10H16_AEI)
  del c10H16_AEI
  a16_CH2O_SUB = FindSource('16_CH2O_SUB')
  SetActiveSource(a16_CH2O_SUB)
  Delete(a17_O3_SUB)
  del a17_O3_SUB
  a15_C10H16_SUB = FindSource('15_C10H16_SUB')
  SetActiveSource(a15_C10H16_SUB)
  Delete(a16_CH2O_SUB)
  del a16_CH2O_SUB
  a14_O3_SAC = FindSource('14_O3_SAC')
  SetActiveSource(a14_O3_SAC)
  Delete(a15_C10H16_SUB)
  del a15_C10H16_SUB
  a13_CH2O_SAC = FindSource('13_CH2O_SAC')
  SetActiveSource(a13_CH2O_SAC)
  Delete(a14_O3_SAC)
  del a14_O3_SAC
  a12_C10H16_SAC = FindSource('12_C10H16_SAC')
  SetActiveSource(a12_C10H16_SAC)
  Delete(a13_CH2O_SAC)
  del a13_CH2O_SAC
  a8_O3_MGR = FindSource('8_O3_MGR')
  SetActiveSource(a8_O3_MGR)
  Delete(a12_C10H16_SAC)
  del a12_C10H16_SAC
  a7_CH2O_MGR = FindSource('7_CH2O_MGR')
  SetActiveSource(a7_CH2O_MGR)
  Delete(a8_O3_MGR)
  del a8_O3_MGR
  a6_C10H16_MGR = FindSource('6_C10H16_MGR')
  SetActiveSource(a6_C10H16_MGR)
  Delete(a7_CH2O_MGR)
  del a7_CH2O_MGR
  a5_O3_DEV = FindSource('5_O3_DEV')
  SetActiveSource(a5_O3_DEV)
  Delete(a6_C10H16_MGR)
  del a6_C10H16_MGR
  a4_CH2O_DEV = FindSource('4_CH2O_DEV')
  SetActiveSource(a4_CH2O_DEV)
  Delete(a5_O3_DEV)
  del a5_O3_DEV
  a3_C10H16_DEV = FindSource('3_C10H16_DEV')
  SetActiveSource(a3_C10H16_DEV)
  Delete(a4_CH2O_DEV)
  del a4_CH2O_DEV
  a2_O3_CHR = FindSource('2_O3_CHR')
  SetActiveSource(a2_O3_CHR)
  Delete(a3_C10H16_DEV)
  del a3_C10H16_DEV
  a1_CH2O_CHR = FindSource('1_CH2O_CHR')
  SetActiveSource(a1_CH2O_CHR)
  Delete(a2_O3_CHR)
  del a2_O3_CHR
  a0_C10H16_CHR = FindSource('0_C10H16_CHR')
  SetActiveSource(a0_C10H16_CHR)
  Delete(a1_CH2O_CHR)
  del a1_CH2O_CHR
  var_1foam = FindSource('var_1.foam')
  SetActiveSource(var_1foam)
  Delete(a0_C10H16_CHR)
  del a0_C10H16_CHR
  Delete(var_1foam)
  del var_1foam
  animationScene1 = GetAnimationScene()
  animationScene1.UpdateAnimationUsingDataTimeSteps()
  Delete(spreadSheetView1)
  del spreadSheetView1
  Delete(quartileChartView2)
  del quartileChartView2
  Delete(quartileChartView1)
  del quartileChartView1
  layout1 = GetLayoutByName("Layout #1")
  RemoveLayout(layout1)
  layout1_1 = CreateLayout(name='Layout #1')
  RemoveLayout(layout1_1)
  layout1_2 = CreateLayout(name='Layout #1')
