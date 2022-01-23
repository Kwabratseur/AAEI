# Work In Progress!

# Air Adverse Effect Index (AAEI)

## Introduction
In this repository, the python code to calculate an Air Adverse Effect Index is presented. The Comptox **Generalized Read-Across Database** [GenRA](https://comptox.epa.gov/genra/) applies Read-Across methodology on a large database of toxicological values for many chemicals. Gaps can be filled, and a report on confidence of the results is given, plus a likeliness that this effect is positive (present). This tool can provide up to 15 *analog* chemicals, which toxicological properties will be extrapolated to the chemical of interest. This extrapolation can be exported, this is the input-format for the **AAEI** tool.

Additionally, files for four **OpenFOAM** simulations are made available. It is explained how these files can be run and how the post-processing steps can be applied to calculate the AAEI.

#### Installation
* Through Github:
 * Download the .tar.gz from **Releases**
 * Install allowable python
 * Install AAEI:
  * `sudo pip3.x install aaei-1.0.x.tar.gz[Viz]`
  * Without the Viz label, visualization tools will not be installed (Matplotlib, Seabornd and Plotly)
* Through [Pypi](https://pypi.org/project/aaei/) Package index:
 * `pip install aaei[Viz]`

## Adverse effect index

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
  5. **AEI_Norm.csv** Follows from this step and can be applied however desired.
  6. Follow the steps under [ParaView AAEI applications script/Macro](#ParaView-AAEI-applications-script/Macro) to apply the results to a run simulatin
  7.The resulting normalized AEI can be applied to any dataset
      * To averages over time, to determine the **relative** effect on different effect-groups
      * To spatial data, this can locate the more healthier or less healthy locations.
      * To see the contribution to AEI by different **gases**, **test-types** or **effect-types**
      * To the right the ParaView source-tree is shown, the different effect categories are visible.

## Software

A list of software used in this project

### OpenFoam
[OpenFoam](https://openfoam.org/) .org version 9 has been used to run the simulation in this repository.
I would recommend installing OpenFOAM V9 through docker, following the guide at https://openfoam.org/download/9-linux/. For linux this leads to a straight-forward setup, which is easily accessible.
There are no instructions on Windows, but this is fairly easy.:
 1. Download and install Docker: https://docs.docker.com/desktop/windows/install/. You might need to setup WSL.
 2. Once setup, go to https://hub.docker.com/r/openfoam/openfoam9-paraview56 and use the docker pull command to start installing the docker.
 3. Run the docker and access it through a terminal, set up some-sort of shared folder in order to work efficiently.

After an installation like this, you access the docker image first and then execute OpenFOAM specific commands.  
All commands use a certain naming convention, so they are easy to find with autocompletion.  
To give you a head-start, see the cheat-sheet below.

<img src=https://s3.studylib.net/store/data/025453706_1-bd2eaeb6355a6e966ae4632a763f7e10-768x994.png width="600" height="800">

[Solver capability matrix](https://www.openfoam.com/documentation/guides/latest/doc/openfoam-guide-applications-solvers.html) *(Note: for openfoam.com version, mostly the same but might differ!)*

### PyFoam
[PyFoam](https://pypi.org/project/PyFoam/) Very convenient library which adds functionality and tools for [OpenFoam](https://openfoam.org/)
 * Used to monitor every simulation with: *pyFoamPlotWatcher --with-all log*
 * Opens number of real-time plots to monitor residuals, specific values
 * *customRegExp* found under some simulation is also shown every timestep, in this case it calculates the total *average gas concentration [ppm]* using functionObjects

### ParaView
[Paraview](https://www.paraview.org/) has been used for analysis of simulation results. A post-processing script is provided to automatically apply the results of the **AAEI**
 * Installation instructions can be found on the website
 * Make sure that you install a version of paraview **with python!** Otherwise the macro-script will not work.

### Jupyter notebook
[Jupyter](https://jupyter.org/) notebooks have been used to do all major data-processing, visualization and analysis. It is also used as an IDE, the **GenRA AEI** scripts have been developed in Jupyter.
 * Installation instructions can be found on website

### Python

#### Case-copy script
To ease the copying and management of OpenFOAM cases, a simple script has been written and provided, to copy and clean cases on a per-case basis, it will put the cleaned cases in /CleanCases relative from where you are.
 * Simply make sure it is executable, and run CopyCase \<CaseName\>.

#### AAEI calculation script
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

##### AAEI commandline help and arguments
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
```
Where the first item in the column is the argument, and the second the default state.  
For example: `AEI filename=Export_2 pivot=Export_2_Target.csv viz fcn=avg`

#### ParaView AAEI applications script/Macro

First this script needs to be imported into ParaView:
 * To get the script: install this library and run `AEI CopyExamples`, the scripty AEI.py copied in your active directory is the ParaView macro.
 * Or download it [here](/AAEI/AEI.py) from the git manually
Once the AAEI script is imported:
 * Import the script it in ParaView by copying it to the macro folder, or through the macro toolbar option.
 * Select the source-simulation (*.foam* file in the source-tree)
 * Make sure that there is a **AEI_Norm.csv** available in the ParaView source-tree, values are directly read and applied from there.
 * Run the script [AEI.py](/AAEI/AEI.py), A pop-up will open
     * give the text-box a comma-separated list of chemicals, such as: **"C10H16","CO2","O3"**
     * press ok/apply/enter, almost instantly many calculators will be added to the source-tree. The final result is put into the **AEI** calculator, all the other ones are appropriately named.

## Simulations

<img src=gfx/Openfoam_files.png width="150" height="280" align=right>

### General case setup

To run the steps a few things need to be prepared, all the following steps need to be run in an installation where OpenFOAM commands are available. So in the docker, or load your environment variables.
#### Preparing Mesh
* Mesh files describing the geometry, located in `<case>/constant/geometry/*.stl` or originating from `<case>/system/blockMeshDict`
  * in the case of `*.stl` files you have to run do a few things:
    * run `blockMesh` to generate the base block, that needs to bigger then the geometry.
    * run `surfaceFeatures` to extract surface features from the files.
    * run `snappyHexMesh -overwrite` to generate the final geometry, this might take a while.
      * In some cases snappyHexMesh generates folders like `<case>/0.001/` and `<case>/0.002/`, copy the folder polyMesh to constant and the other files to the `<case>/0/` folder
      ```
      cd <case>/
      blockMesh | tee log.blockMesh
      surfaceFeatures | tee log.surfaceFeatures
      snappyHexMesh | tee log.snappyHexMesh
      cp -r 0.002/polyMesh constant/polyMesh
      cp 0.002/*Level 0/
      ```
  * in the case of `blockMeshDict` simulations simply run `blockMesh`


  Now for sanity, we want to run the simulation a bit more optimized and use all our processors in parallel.

<img src=gfx/Plane_Definitions_STL.png width="400" height="300" align=right>

  * Edit `<case>/system/decomposeParDict`
    * Change the line `numberOfSubdomains 16;` to the amount of **physical** cores your processor has (not threads). You can check this in task-manager on Windows.
  * Now run `decomposePar` in the `<case>/` folder, this will split the simulation in subdomains.

As a last step you can check if everything works with Paraview:

* make a file with `.foam` extension in the `<case>/` directory and open it with openfoam:
    ```
    touch <case>/simulation.foam
    paraview <case>/simulation.foam &
    ```
* You can also open the case through the paraview interface.
* You can inspect the generated geometry, and see how `decomposePar` split the problem in sub-domains. By using the wireframe or Surface with edges visualization, the mesh can be visualized.

#### Running simulation and monitoring
<img src=gfx/Sim_Overview_Kazuhide.png width="400" height="300" align=right>

Most cases here use the `buoyantReactingFoam` solver, so this general description is written for those cases.

* Go to the `<case>/` directory in your openFOAM environment
* run `mpirun -np <No_Cores> buoyantReactingFoam -parallel | tee log`
  * where `<No_Cores>` is the `numberOfSubdomains` you set before in `<case>/system/decomposeParDict`
  ```
  cd <case>/
  mpirun -np 16 buoyantReactingFoam -parallel | tee log
  ```

With [PyFoam](https://pypi.org/project/PyFoam/) you can monitor the
simulation visually by graphing the log in realtime.

  * first you need to install it on your **system**, so not in the      **docker** with the command `pip install PyFoam` or your package manager of choice for python.
  * `pyFoamPlotWatcher --with-all log`
  * Now a bunch of plots pop-up, among others: residuals, some concentrations changing over time (`customRegExp`), courant number, etc.
* While running, you can open the `*.foam` file with Paraview. Set the case to decomposed and you can view any new timesteps after refreshing.
* Stop the simulation with CTRL+C in the command-line window.
* If you want a nicer view, and the decomposed case to be restored:
  * `reconstructPar` to reconstruct all timesteps
  * `reconstructPar --latestTime` to only reconstruct the last available timestep.

<img src=gfx/X3_Overview_Geom.png width="400" height="300" align=left>

<img src=gfx/AEI_opaq.png width="400" height="300" align=right>
