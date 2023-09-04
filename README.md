# Work In Progress!

# Dynamic Adverse Effect Index (DAEI/DynAEI)

## Introduction
In this repository, the python code to calculate a Dynamic Adverse Effect Index is presented. The Comptox **Generalized Read-Across Database** [GenRA](https://comptox.epa.gov/genra/) applies Read-Across methodology on a large database of toxicological values for many chemicals. Gaps can be filled, and a report on confidence of the results is given, plus a likeliness that this effect is positive (present). This tool can provide up to 15 *analog* chemicals, which toxicological properties will be extrapolated to the chemical of interest. This extrapolation can be exported, this is the input-format for the **DAEI** tool.

Additionally, files for four **OpenFOAM** simulations are made available. It is explained how these files can be run and how the post-processing steps can be applied to calculate the DAEI.

see [Openfoam ParaView instructions ](OpenFOAM_ParaView.md) for how to apply DynAEI there, and some general usage tips.
See [Openfoam Tutorial](https://github.com/Kwabratseur/STL-Thermal-Paraview-tutorial) for an in depth thermal simulation tutorial

#### Installation
* Through Github:
 * Download the .tar.gz from **Releases**
 * Install allowable python
 * Install DAEI:
  * `sudo pip3.x install aaei-1.x.x.tar.gz[Viz]`
  * Without the Viz label, visualization tools will not be installed (Matplotlib, Seabornd and Plotly)
* Through [Pypi](https://pypi.org/project/aaei/) Package index:
 * `pip install aaei[Viz]`

## Dynamic Adverse effect index

 The table below shows the presence of a certain *health/target effect* per row, related to the *test group* it is categorized under in [GenRA](https://comptox.epa.gov/genra/).  
 This categorization is used as an intermediate step before calculating the total sum or average.

 <img src=gfx/Toxicity_Effects.png width="600" height="700">

 <img src=gfx/Weights.png width="450" height="150" align = "right">

 The sum or average is normalized, and a matrix can be created with chemical species against test-types or effect-types.  
 See the image to the right for an example (colored with LibreOffice)

 ### Method

 <img src=gfx/Paraview_AEI.png width="100" height="300" align="right">

  1. go to [GenRA](https://comptox.epa.gov/genra/)
  2. go through the 5 steps:
      * Select target chemical
      * select analogs
      * generate read-across prediction
      * export read-across prediction
      * rename export to **genra_\<formula\>.csv**, in the case of CO2: **genra_CO2.csv**
  3. do this for every chemical you are interested in, or in your simulation (Names need to match!)
  4. By running the script in the following way:
 ```bash
     AEI CopyExamples
     AEI Run viz piv=Batch_Report_Target.csv
 ```
      * GenRA files O3, C10H16 and CH2O will be *copied*, including *AEI.py* ParaView macro script
      * GenRA files O3, C10H16 and CH2O will be processed
      * Files *Batch_Report_Target.csv* ,*Batch_Report_Meta.csv* and one file per input file will be generated in the folder it was run
      * viz will generate a 3D-bubble plot, with X = Effectgroup, Y = species, Z = Testgroup. And bubble-size = positive effect magnitude
      * piv=Batch_Report_Target.csv will generate and open a pivot pivottablejs interactive pivot table in the browser for the file mentioned.
  5. **AEI_Norm.csv** Follows from this step and can be applied however desired. [General usage](#General-usage) shows how this can be applied and interpreted for generic .csv files.
  6. Follow the steps under [ParaView DAEI applications script/Macro](#ParaView-DAEI-applications-script/Macro) to apply the results to a run simulatin
  7.The resulting normalized AEI can be applied to any dataset
      * To averages over time, to determine the **relative** effect on different effect-groups
      * To spatial data, this can locate the more healthier or less healthy locations.
      * To see the contribution to AEI by different **gases**, **test-types** or **effect-types**
      * To the right the ParaView source-tree is shown, the different effect categories are visible.

## Software

A list of software used in this project

### Jupyter notebook
[Jupyter](https://jupyter.org/) notebooks have been used to do all major data-processing, visualization and analysis. It is also used as an IDE, the **GenRA AEI** scripts have been developed in Jupyter.
 * Installation instructions can be found on website

### Python

#### Case-copy script
To ease the copying and management of OpenFOAM cases, a simple script has been written and provided, to copy and clean cases on a per-case basis, it will put the cleaned cases in /CleanCases relative from where you are.
 * Simply make sure it is executable, and run CopyCase \<CaseName\>.

#### DAEI calculation script
it provides standard methods to calculate an output file **AEI_Norm.csv**
It provides the following methods:
 * Filter out Metadata from the GenRA files, calculate statistical values and export as **genra_\<formula\>_\<chemical_name\>_metadata.csv** for example `genra_O3_Ozone_metadata.csv`
     * List of all found **Target** afflictions + statistics is exported as **Batch_Report_Target.csv**
     * list of all found **Test** groups + statistics and metadata from original genra file is exported as **Batch_Report_Meta.csv**
 * Batch process a group of chemicals in one go
     * Visualizations can be exported with a flag `viz`
     * Total summary from this step, **AEI_Norm.csv** needs to be opened in [Paraview](https://www.paraview.org/), if the automatic application wants to be followed for a OpenFOAM simulation.
     * The resulting normalized AEI can be applied to any dataset
         * To averages over time, to determine the **relative** effect on different effect-groups
         * To spatial data, this can locate the more healthier or less healthy locations.
         * To see the contribution to AEI by different **gases**, **test-types** or **effect-types**

##### DAEI commandline help and arguments
By running `AEI help` you will get the following output.:
```
Run this script in a folder with genra_<chemical>.csv files.
Use the flags shown below to control the output
You can use fcn: sum, avg, med for the different normalization schemes
Use pivot=file.csv flag to open a .html interactive pivot table in your browser. This works for any .csv with categorical data (text flags in rows)
Argument viz generates 6 graphs to aid in data analysis.
Argument Run runs the script with default filenames in the current folder
possible arguments are:
arg:  filename  - Batch_Report
arg:  viz  - False
arg:  pivot  - Batch_Report_Target.csv
arg:  fcn  - sum
arg:  piv  - False
arg:  help  - True
arg:  Run  - False
arg:  CopyExamples  - False
arg:  version  -  V2
```
Where the first item in the column is the argument, and the second the default state.  
For example: `AEI filename=Export_2 pivot=Export_2_Target.csv viz fcn=avg`

## General usage
The philosophy of this method is to use the most recent and state of the art toxicology knowledge for a data driven dynamic health index. With this approach, all chemical species can be taken into account. Since it is data driven, stability in results is ensured.

To show how this works, the EU Air Quality Index is used as a comparison. We generate data suitable for the EUAQI, but also some more data which will be omitted. The DynAEI will be able to use all data. The results follow coarsely the same patterns for now. But this difference might change significantly depending on the samples, but also new studies in the future.

The function mentioned in these subparagraphs are all found in AEI_PV.py. AAEI must be imported for these to work.
### Example function demo

The function RunFcnDemo() found in AEI_PV.py shows an example implementation of how to generate and apply DynAEI, and make a comparison to EUAQI.

* It can be run with the following code:
```
Import AAEI
From AEI_PV import *
RunFcnDemo()
```
Below I will explain the function calls in this demo function to show how it can be applied to your data.

#### Procedure to generate DynAEI for (later) use
Since this is a fully data driven approach where no limits are determined ahead of time it needs to be generated for each unique set of compounds that need to be compared.

Since the chemistry matters for lookup purposes, it is important to follow the naming conventions.

You can simply start with importing the libraries.
```
Import AAEI
From AEI_PV import *
```

The function `AAEI.BatchReport` does all the heavy lifting and generates the dynamic index for you. Below you can see it's input arguments. In general, you set the fileNames to a list of "genra_[chemical_name]", the output filename, you indicate which values to merge and which additional entries to add. More about the last 2 below.
```
BatchReport(fileNames,
            filename,
            fcn="sum",
            viz = False,
            ext = False,
            merge="None",
            entries = "None",
            version="v2")
```

##### Adding entries as a function of other data
This approach can only work with pure chemicals, things like particulate matter in general have an unknown chemical composition, therefore there is no exposure assay data that can be generalized and found in GenRA. To solve this problem, PM10 or PM25 can be expressed as a function of another compound. In this case, a linear correlation was established with the limit values of Ozone and PM10 found in the EUAQI, the same was done for Ozone and PM2.5.
We pass the keyword `entries` a dictionary with the linear coefficient found, like shown below.
```
entries= {"PM10":["O3",0.3330015744489429],
          "PM25":["O3",0.6382530176938073]}
```
##### Merging multiple entries into a single entry
In certain chemistry models, simplifications are made and chemical reactions can be binned into a term like resultant reaction product, which is a certain composition of other known compounds. To facilitate these models, below syntax can be used to merge the GenRA data of multiple compounds into one product. Below CH3CHO, C10H16O2 and C8H14O are merged into one term called Cprod
`merge="CH3CHO,C10H16O2,C8H14O-Cprod"`

##### Generate the DynAEI

The example below would assume that 6 genra_[chemical].csv files are available, no data will be merged but 2 entries will be added since entries are passed to the function.
```
MetaBlobs, TargetBlobs, analogBlobs, PVTable, target_DF = AAEI.BatchReport(["genra_C10H16",
                                                                            "genra_CH2O",
                                                                            "genra_O3",
                                                                            "genra_SO2",
                                                                            "genra_NO2",
                                                                            "genra_CO2"],
                                                                            entries=entries,
                                                                            filename="Batch_Report")
```
Only PVTable is further used, this contains the per-assay-group and aggregated toxicity for each compound, this can be applied with relative ease.
A lot of files will be exported in this step.
Now we have a working index loaded, let's proceed with either generating or loading data and applying the index.

#### load data or generate samples
Here we will use the sample generator to generate at least all required samples for EUAQI and some more. The sample instantiator dictionary below shows values in ppb, except for pm10 and pm25 (pm2.5) (both in ug/m3).
```
sampleInstantiator = {"C10H16":{"min":0,"max":66872},
                      "CH2O":{"min":0,"max":1339},
                      "O3":{"min":0,"max":300},
                      "NO2":{"min":0,"max":300},
                      "SO2":{"min":0,"max":800},
                      "PM10":{"min":0,"max":150},
                      "PM25":{"min":0,"max":200},
                      "CO2":{"min":4000000,"max":500000}}
```
Then Either load or generate data into a pandas dataframe with the column names: "O3" "NO2" "SO2" "PM10" "PM25" "CO2" "C10H16" "CH2O":
##### Generate
10 samples are generated `df = sampleGenerator(sampleInstantiator,10)`

<img src=gfx/Original_Samples.png width="400" height="300" align="right">


##### Or Load
 In this edge case, PM10 and PM25 have to be in ug/m3 for the EUAQI comparison, otherwise make sure that everything is in the same units.
```
df = pd.read_csv("data.csv")
df.columns = ["O3", "NO2", "SO2", "PM10", "PM25", "CO2", "C10H16", "CH2O"]

```
And set the columns to the right name.

Note that the 3 (CO2, limonene and formaldehyde are not implemented in EUAQI)

##### Prepare data for later reversibility
This allows for later reversibility, but also to express toxicity equivalence over all species in the sample.

`invStats = df.describe().drop(["count","25%","50%","75%"])`

#### procedure to apply to csv data

1. Extract statistics for later reversibility
2. Apply DynAEI to samples `res, normStats = impactSampling(df,PVTable)`

##### Reversing function or expressing equivalence

reverses the function, since it is not fully reversible this is only a approximation
`res.T.iloc[len(df.T):len(df.T)*2].T.apply(directInverser, args=(invStats,res["sAgg"],PVTable))`

<img src=gfx/Recovered_Concentration_DynAEI.png width="400" height="300" align="right" >

The nice thing about this feature is the posibility to express Any toxicity into another, we can transponate everything to CO2 values, creating a CO2_Equivalent for all samples in the set.
Do this with the following oneliner:
`res.T.iloc[len(df.T):len(df.T)*2].T.apply(directInverser,args=(invStats,res["sAgg"],PVTable,"CO2"))`
To explain this oneliner further:
 * `res.T.iloc` transponate the result, work with number indices
 * `len(df.T):len(df.T)*2` take a slice from the length of the original data upto twice original data (all DynAEI indices)
 * `.T.apply(directInverser,` Transponate it back and Apply the directInverser function
 * with the input arguments `args=(invStats,res["sAgg"],PVTable,"CO2"))` from which `CO2` is optional, when nothing is given, the function tries to reverse the index. If a chemical name is given that is found in the index, all data is converted to that order of magnitude.

##### Calculate EUAQI for sample

```
euaqi = DF_Apply_EUAQI(df)
euaqi.plot()
```
<img src=gfx/calculated_EUAQI.png width="400" height="300" >

##### Heatmap comparing EUAQI with DynAEI
To make a fair comparison, DynAEI was scaled to the min and max of EUAQI; the result of each group is shown next to each other and the non-available chemicals in EUAQI are shown at the right.
```
df_DynAEI_EUAQI = pd.concat([(res.T.iloc[8:].T*7),pd.DataFrame.from_records(euaqi)],axis=1)[Nice_Col_Order]
stdHM(df_DynAEI_EUAQI)
```
<img src=gfx/Compared_EUAQI_DynAEI_hm.png width="400" height="300" align="right">

# Note To Self:
:tada: :fireworks::tada:
```bash
python setup.py sdist
pip install .  # dry-run from folder
pip uninstall aaei # uninstall
pip install -e # install with symlink
twine upload dist/* #because pip doesn't work anymore for some magical reason.
```

:fireworks::tada: :fireworks:
