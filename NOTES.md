# NOTES openfoam tutorials

[Solver capability matrix](https://www.openfoam.com/documentation/guides/latest/doc/openfoam-guide-applications-solvers.html)  
[tutorial material](http://www.wolfdynamics.com/wiki/fvm_crash_intro.pdf)  
[tutorial exercises](http://www.wolfdynamics.com/wiki/fvm_np.pdf)  


## Day( 4:1 )
* recommended for most cases according to FVM crash course

ddtSchemes  
{  
default CrankNicolson 0;  
}  
gradSchemes  
{  
default cellLimited Gauss linear 1;  
grad(U) cellLimited Gauss linear 1;  
}  
divSchemes  
{  
default none;  
div(phi,U) Gauss linearUpwindV grad(U);  
div(phi,omega) Gauss linearUpwind default;  
div(phi,k) Gauss linearUpwind default;  
div((nuEff*dev(T(grad(U))))) Gauss linear;  
}  
laplacianSchemes  
{  
default Gauss linear limited 1;  
}  
interpolationSchemes  
{  
default linear;  
}  
snGradSchemes  
{  
default limited 1;  
}  

### Folder 101FVM -> PureConvection
* encouraged to use all
 *  time discretization schemes
 *  spatial discretization schemes
 * gradient discretization schemes.
 * gradient limiters.
 * different mesh resolution.
 * different time-steps.
* Sample the solutions and compare the results
* try to find best combination of numerical schemes


## Exercises 1: PureConvection

### 1.Which scheme is useless? Upwind, Downwind or linear?
 **A: Downwind is useless, unconditionally unstable**

### 2.Compare with:
* upwind
* linearUpwind
* MUSCL
* QUICK
* cubic
* UMIST  
 **Are they bounded? and second order accurate?**  

 **A: All schemes are second order accurate (error < stepsize^n), but not all are bounded: cubic, QUICK and linear upwind - Least squares are not bounded**  

* 3.Use the linearUpwind method with Gauss linear and leastSquares for gradient computations, which method
is more accurate?    
 **A: Gauss linear is more accurate and bounded, least squares is not bounded**  

* 4.Imagine that you are using the linearUpwind method with no gradient limiters. How will you stabilize the
solution if it becomes unbounded?
 **A: smaller time step or better(more refined) mesh**  

* 5.When using gradient limiters, what is clipping?  
 **A: reduction of the peaks/troughs or reduction of resolution**  

* 6.Use the vanLeer method with a CFL number of 0.1 and a CFL number of 0.9, did both solutions converge?
Are both solutions bounded?  
 **A: Both solutions converged, strangely CFL 0.9 is bounded and CFL 0.1 is not.**  

* 7.By the way, the solver scalarTransportFoam does not report the CFL number on the screen. How will you
compute the CFL number in this case?
(Hint: you can take a look at the post-processing slides or the utilities directory)  
 **A: Took a look at libutilityFunctionObjects.so and implemented the CourantNo, then I noticed that a deltaT of 0.0001 gives Co = 0.1, so deltaT = 0.0009 gives Co = 0.9.**  

* 8.Which one is more diffusive, spatial discretization or time discretization?  
 **A: It seems that spatial discretization is more diffusive, choosing the wrong scheme seems to impact the accuracy in this case more, and in this case, the accuracy of solution is quite related to the diffusiveness, the slope is much closer to the exact solution with the variations on time discretization.**  

* 9.Are all time discretization schemes bounded?  
 **A: No, most of the schemes showed in this example are unbounded**  
* 10.If you are using the Crank-Nicolson scheme, how will you avoid oscillations?  
 **A: Using an appropriate gradient limiter, such as: cellMDLimited Gauss linear, Celllimited LeastSquares**  
* 11.Does the solution improve if you reduce the time-step?  
 **A: Not necessarily, as shown above, the solution found from the higher CFL number simulation is slightly more accurate**  
* 12.Use the upwind scheme and a really fine mesh. Do the accuracy of the solution improve?  
 **A: Yes, this does greatly improve the result, refining the mesh 100x turns upwind in one of the better results!**  
* 13.From a numerical point of view, what is the Peclet number? Can it be compare to the Reynolds number?  
 **A: The peclet number is the ratio between the advective and diffusive transport of a fluid**  
* 14.If the Peclet number is more than 2, what will happen with your solution if you were using a linear scheme?(Hint: to change the Peclet number you will need to change the diffusion coefficient)  
 **A: there is no diffusion, there will be a perfect boundary layer**  
* 15.Pure convection problems have analytical solutions. You are asked to design your own tutorial with an
analytical solution in 2D or 3D.  
 __A: maybe later__
* 16.Try to break the solver using a time step less than 0.005 seconds. You are allow to modify the original mesh
and use any combination of discretization schemes.  
__A: maybe later__

### Exercises 2: Laplace

 - 1. Run the case using all gradient discretization schemes available. Which scheme gives the best results?
 __A: Gauss Linear combined with hexahedral mesh gives best results, grad Ty is by far the smoothest.__  

 - 2. According to the previous results, which element type is the best one? Do you think that the choice of the element type is problem dependent (e.g., direction of the flow)?  
 __A: The best element type is hedahedral for this case!. I think it has to do with the direction of flow, in this case there is more-or less unidirectional phenomena happening, so that's why this mesh performs the best, it is equal in all directions.__  

 - 3. Use the leastSquares method for gradient discretization, and the corrected and uncorrected method for Laplacian discretization. Do you get the same results in all the meshes? How can you improve the results? (Hint: look at the corrections)  
 __A: The hexahedral mesh gives no different results over the different options, the other two meshes are much better when using laplacian corrected or laplacian face-corrected.__

 - 4. Does it make sense to do more non-orthogonal corrections using the uncorrected method?  
 __A: This might be the case if this is computationally less expensive, but for simple cases I think it's better to use the corrected method.__

 - 5. Run a case only 1 iteration. Do you get a converged solution? Is there a difference between 1 and 100
iterations? Compare the solutions.  
__A: the solution is slightly different but very close to the solution at t=100. This is a transient simulation, so it will iterate untill it reaches the desired convergence/residuals. For this reason, the results are very close.__

 - 6. Use a different interpolation method for the diffusion coefficient. Do you get the same results?  
 __A: I used vanLeer, which breaks the simulation. Cubic does give slightly different results, at y=-1 the values of cubic are closer to the best results at t=100, so this method seems better for this case.__  

 - 7. Try to break the solver (this is a difficult task in this case). You are allow to modify the original mesh and use
any combination of discretization schemes.  
__A: it was easy to break, just use vanLeer interpolation method for diffusion coefficient.__  

### Exercises 3: nonorthoCavity

1. After generating the mesh, we will use the utility checkMesh to control the quality of
the mesh. Is it a good mesh?  
__A: According to checkMesh it is relatively good, it passes most checks, and it could be less non-orthogonal__

2. First run the case using the original dictionaries. Did it crash right?  
__A: Yes, it did crash, this was expected after reading the slides and seeing the fvschemes and fvsolutions__

3. Now change the laplacianSchemes and snGradSchemes to limited 1. It crashed again but
this time it ran a few more time-steps, right?  
__A: Yes, it ran for 1 timestep and crashed in the second timestep. No data has been written still.__

4. Now increase the number of nNonOrthogonalCorrectors to 2. It crashed again but it is running
more time-steps, right?
__A: yes, now it crashed after 17 iterations__

5. Now increase the number of PISO corrections to 2 (nCorrectors). Did it run?  
__A: With PISO=2 it finally completes the simulation.__

6. Basically we enabled non-orthogonal corrections, we computed better approximations of the
gradients, and we increased the number of PISO corrections to get better predictions of the field
variables (U and p).

7. Now set the number of nNonOrthogonalCorrectors to 0. Did it crash right? This is telling us
that the mesh is sensitive to the gradients.  
__A: yes, crashes right away__

8. Now change the laplacianSchemes and snGradSchemes to limited 0 (uncorrected). In this
case we are not using non-orthogonal corrections, therefore there is no need to increase the
value of nNonOrthogonalCorrectors.  
__A: this works better and is less diffusive__  


9. We are using a method that uses a wider stencil to compute the Laplacian, this method is more
stable but a little bit more diffusive. Did it run?  
__A: it did run__  

10. At this point, compare the solution obtained with corrected and uncorrected schemes. Which
one is more diffusive?  
__A: The uncorrected variant is more diffusive__

11. Using the non-orthogonal mesh and the original dictionaries, try to run the solver reducing the time-step. Do
you get a solution at all?  
__A: No, if you make the timestep smaller and smaller, at maximum it runs 47 iterations__  

12. Try to get a solution using the method limited 1 and two nNonOrthogonalCorrectors (leave nCorrectors
equal to 1).
(Hint: try to reduce the time-step)  
__A: reducing the timestep by a factor ten (0.001) makes the solver run__  

13. If you managed to get a solution using the previous numerical scheme. How long did it take to get the
solution? Use the robust setup, clock the time and compare with the previous case. Which one is faster? Do
you get the same solution?  
__A: The solution for the small timestep seems to be less diffusive and a bit more accurate, however it takes significantly longer, in the magnitude of 10x longer.__  

14. Instead of using the non-orthogonal mesh, use a mesh with grading toward all edges. How will you stabilize
the solution?
(Hint: take a look at the blockMesh slides in order to add grading to the mesh)  
__A: Didn't do this, but you should use corrected scheme to correct for the grading in the mesh__

15. Try to get a solution using a time-step of 0.05 seconds. Use the original discretization schemes for the gradient
and convective terms.
(Hint: increase nCorrectors and nNonOrthogonalCorrectors)  
__NAN__  

16. Try to break the solver and interpret the output screen. You are allow to modify the original mesh and use any
combination of discretization schemes  
__A: This is not really a challenge, next.__  

### Exercises 4: shockTube

__A: Did these exercises, but not recorded here. See directory for results__

***

### Exercises day 4:3 discretization

1. In this tutorial, we simulate the shocktubes (pitzdaily) with scalartransportfoam. This is done in directory discretization. Goal is to see the difference between diffusion schemes.

2. The first sim, with linear interpolation has relatively high diffusivity

3. The second simulation with upwind has less diffusion but generates strange oscilations at the left.

4. with linearUpwind the oscillations are reduced but still there

5. with QUICK we get no measurable oscillations and also little diffusion, one of the best for this case. (together with linearUpwind)

6. The cubic variant has relatively big oscillations, if the patch type is changed from inletOutlet to zeroGradient, the oscillations add up and become really more problematic.

7. if deltaT is increased for linearUpwind, the solution converges in the same manner but with more diffusion.

8. This does not work for QUICK, it required smaller timestep.

9. linearUpwind is the best compromise in terms of time and accuracy for 90% of cases.

***

### Last video Day 4: finite volume discretization
[video](https://www.youtube.com/watch?v=a4B_oXR5Kzs&ab_channel=KennethHoste)

- The big thing for convection discretization:
There are ~45 TVD and NVD schemes, linearUpwind is good enough for quick results. If you require second order accuracy, just pick one of the TVD and NVD schemes and stick with it! just try to make it work, there is maybe 2~3% difference between all the different schemes.
 - **VanLeer is the favourite of this professor, sounds dutch so good choice**

- **for Hexahedral meshes:**
 - gauss or gauss with limiter gradient scheme
 - for convection:
   - Start with upwind convection scheme, if something goes wrong, there are problems elsewhere in the case
   - momentum equation: start with linearUpwind with optional gradient limiters
   - Use TVD/NVD schemes (vanLeer) for bounded scalars (eg.e turbulence, and NOT speed)
 - for diffusion scheme:
   - if non-orthogonality < 60 deg, gauss linear corrected
   - if non-orthogonality > 70 deg., gauss linear limited 0.5
-  Monitor boundedness of scalars and adjust convection/diffusion schemews to remove bounding messages
  - this means: pressure does not go negative, temperature does not go negative, concentrations are between 0 and 1, etc. sanity checking.  

- **For Tetrahedral meshes:**
 - Gradient schemes: least squares in most cases without limiters
 - Convection scheme:
   - start with upwind, nature of discretisation error changesd due to lack of mesh-to-flow alignment
   - for highly accurate simulations, special reconstructed schemes are used.
 - diffusion scheme:
   - always with non-orthogonality limiters. Control limiter based on boundedness messages of scalars
- Sticking to these defaults should; in most cases, lead to a running simulation and relatively sane results.
- Many things can still go wrong.:
 - inlet and outlet conditions
 - relaxation factors,
 - solver tolerances
 - number of piso correctors
   - optimize by "residual gazing"


### Day 5:1 running my first own case (jozsef nagy)
 - find case in TransportBall
   - modified case from shocktubes
   - uses scalartransportFoam
   - changed mesh to square 10x10
   - used setFieldsDict to make a circle with T=1 in the center
   - changed original U to Vx=1
 - At t=4s stop simulation, remove phi and change U to Vy=1
   - run for another 4s
 - At t=8s stop simulation, remove phi and change u to Vy=-1 and Vx=-1
   - Run for another 4s, circle is back at starting position.
 - I optimized fvsolution and fvschemes for this case
 - Also controldict was changed to latestTime and runtime was updated after each run.

 ### Day 5:2 laminar flow in pipe Re=100
  #### See case laminar_pipe
- In case 1 we initialize speed, from the last timestep we calculate an average inlet pressure.
 - This inlet pressure is used in case 2, the speed is set to zero and the average pressure is set constant on the inlet, this initializes different

### Day 6 Meshing and modelling
 - This day is about Meshing
    - I skip this because of enough experience modelling and partially meshing
    - I will follow/combine a tutorial to my own usecase,
      - Look for reference studies? to repeat
      - I will work with snappyhexmesh to work with .stl files. cfmesh does similar things but I'm using the wrong version (.org instead of .com version) so it doesn't come with cfmesh
      - [this frontend](https://www.idealsimulations.com/applications/hvac/) might be interesting

#### SnappyHexMesh!
* Can run parallel with MPI
* General workflow:
  * Keep top level structure: mesh, geometry, case
  * in mesh: make constant and system dir
  * cp ../geometry/*.stl constant/triSurface //copy STL to mesh folder
  - surfaceFeature(s)(Extract) //depending on version of openfoam, also adjust in system!!!
  - blockMesh // generate top level geometry that will be "snapped" to geometry. Should fit geometry
  - snappyHexMesh -overwrite // generate snappyhexmesh
  - next: copy generated geometry to case folder ->
  - cp -r ../mesh/constant/polyMesh constant
  - setFields
  - foamSimulation!


### Day 7:1 stationary turbulence modelling

 - another joszef nagy tutorial, this time a backward step with different turbulence models.
 - steady state so no partial time derivatives nor physical time
 - laminar/turbulent model
 - single phase model
 - isothermal so no energy equation
 - SIMPLE loop
 - turbulence is the chaotic change of field values in space and time
  - there is a mean velocity, and a oscillation around the mean value
  - the oscillations is what the different models are for, this models the turbulence
  - RANS: we ignore the oscillations, we take the constant value
  - turbulent viscosity: models the transport and dissipation of energy neglected by averaging
  - vortices are not turbulence, laminar flow can have vortices.
 - We need to calculate the inlet velocity
  - we want Re = 44000
   - 44000 = U*nu/L; U = 7.3 m/s
  - we need to calculate  k on the inlet with:
   - 1.5*(U*Ti)^2
   - 1.5*(7.3*0.05)^2 = 0.2
  - we need to calculate epsilon:
   - 0.09^(3/4)*((k^1.5)/L*0.07) = 3.54
 - the 3 models are:
  - kEpsilon model
  - kOmega model
   - calculate specific dissipation rate
   - epsilon/k = omega
  - LRR model

### Day 7:2 Transient turbulence modelling
 * we have RAS (Reynolds averaged blabla) and LES(Large Eddy Simulations) models
 * 4 different turbelence modelling schemes were used:
  * K-Epsilon model (RAS)
    * Use when your region of interest is far away from turbulent phenomena, all eddies are averaged out.
  * smagorinsky model (LES)
    * Use this when you are interested in turbulent phenomena, you will see eddies in transient simulations. The "sub-grid-scale" turbulence is "hidden" in nut
  * dynamic-K-Equation (LES)
    * Seems to be the most accurate of all, the nut value is smallest overall, except for very few hotspots.
  * K-Equation (LES)
    * K-equation model seems to perform similar/ a little bit worse then the smagorinsy model.
 * All above simulations use nut to resolve "neglected" turbulence. It is visible that this is magnitudes bigger in the RAS model (all eddies are ignored). The dynamic-k-eqn performs best, nut is by far lower then other equations, thus assumed to be the most accurate in this case.

### Day 8:1 Theory of turbulence modelling
 * No general description of turbulence
 * Turbulence is a feature of flow, not a property of a fluid.
 * Turbulent flows can originate at walls, this is called bounded turbulence, specific models take this into account.
 * Turbulent flows that arise from "nothing" are called shear free turbulence, other models model this phenomena.
 * Depending on what effects you're interested in, choose your model wisely.
 * There are different scales of eddies:
  * L0
    * Largest scale
    * derive their energy from mean flows
    * size and velocity on the order of mean flow
    * use RANS/URANS simulation to resolve these
  * L1
    * LN < L2 < L1 < L0
    * L1 and L2 derive their energy via vortex stretching of a bigger eddie
    * LES/VLES resolves L1/L2 eddies
  * LN
    * Smallest eddies
    * dissipate kinetic energy to thermal energy via viscous dissipation
    * DNS (direct numerical simulation) resolves all, but has the tightest meshing requirements, compared to RANS and LES
 * Depending on how much details you want to resolve, you can check the graph/table in [energy spectrum and mesh resolution:page 43](http://www.wolfdynamics.com/wiki/advanced_turbulence1.pdf)
 * In LES use ~ 15 cells across L0/L
 * In VLES use 4-6 cells across L0/L
 * L0 can be estimated based on a characteristic length (pipe diameter etc. object size)
  * from correlations
  * from experimental results
  * from RANS simulation
    * use K-epsilon model and apply L0=k^1.5/epsilon
 * Use RANS simulations as a starting point for LES/DES simulations
 * y+ is never known when you start. Run a few iterations and then estimate y+
  * Page 82-90 of last link explains the concept of y+
  *

### Day 8:2 Flow around a cylinder 2D
* different models and meshes, laminar/turbulent, parameter study.
* You can use potentialfoam to generate initialconditions for other solvers
* you can map coarse solutions to finer meshes to speed up initialization
  * Extra fields can be written with arguments to the solver like:
   * potentialFoam  –noFunctionObjects –initialiseUBCs –writep -writePhi
   * where the last to write the pressures and fluxes.
   * nofunctionobjects ignores functionobjects and prevents errors with that
* mapfields ../c4 –consistent –noFunctionObjects –mapMethod cellPointInterpolate -sourceTime 0
 * Map the coarse mesh from c4 potentialFoam run (better init)
 * interpolate it to the finer mesh in c6
* Fixed C8 as an extra exercise, a lot of minor things were wrong. Wrong P and U file patch boundary conditions, missing turbulence properties, wrong defined p Units, too big of a timestep, CFL too high. Errors are insightfull enough though.
* renumbermesh -overwrite
 * improve mesh diagonality, speeds up sim
* run gnuplot scripts0/plot_coeffs to plot coeffs in realtime
* pimpleFoam –postprocess –func yPlus –latestTime -noFunctionObjects
 * calculate yplus for latest time
 * rhoPimpleFoam –postProcess –func MachNo

### Day 8:3 Flow around a square cylinder 3D
* Vortex shedding past square cylinder

### Day 9:1 multiphase physics 2D dambreak
* Joszef nagy tutorial about multiphysics 2d dambreak
* interfoam laminar simulations
* volume of fluid method
* the interface between air and water has a gradient, this gradient becomes smaller when you reduce mesh size.
* a cell with 0.5-0.3% water and density of 500/300 is not realistic, for this reason it's important to simulate different cell sizes or even models to see where the fluid actually goes
 * this is because of conservation of momentum

### Day 9:2 multiphase physics 3D dambreak
* Purely example, but it works well.
* uses turbulent RAS model instead of laminar
* use contour / threshold to visualize in parafoam
 * set to alpha_water=0.5

### Day 9:3 multiphase physics, freeflow over surface
 * bubble in liquid

### Day 10:2 Parralellization Joszef Nagy - Depth charge
* decomposePar decomposes for x cores
 * As defined in decomposeParDict in /system/
* We will use different decomposition methods
 * simple -> divide in 2, 4, 6, 8 pieces
 * scotch <- recommended by wolfdynamics
  * certain algorithm, decide on your own
 * hierarchical
 * manual
 * metis
  * certain algorithm, decide on your own

### Life hacks ---
* To make a video from .png with ffmpeg:
 * ffmpeg -r 30 -i ke_simp_AC.%4d.png -c libx264  -pix_fmt yuv420p -s 1268x1008 output.mp4

 * check internet to make accurate, this is just a list of what is needed. Don't remember exact arguments
 * important: you need square ratio, 1000x637 will cause problems with juvy720p and requires 722p pixel format, which has very bad support
* Don't forget: in Paraview if you integrate variables over time (with extracted selection first, heavy operation!), you see rate of change.
  * allows to plot average concentration over time
  * allows to calculate residence time distribution, if you integrate and plot over a surface.

## Measure CO2 emissions at rest/working (example)
* 2-6 people work sitting in Smart tiny lab.
* A table and enough chairs are placed centrally in the room
* Ventilation is set to minimum level
* Heating is turned off, starting temperature of room is between 18 and 23 C
* Continuous measurements are started 15 minutes prior to experiment (baseline + stabilization)
* For at least 1 hour (2x 30 minutes or 4x 15 minutes) work and fill survey
* Continuous measurements are taken during the working period but also during the breaks.
* Surveys are filled periodically while working
* OPTIONAL: Simulate cleaning conditions by releasing a known amount of cleaning agent
* OPTIONAL: repeat experiment but with increased ventilation to quantify the impact

# Geometry decisions
* * Mesh with persons:
* Accurate mesh: 12556105
* minimal but accurate mesh:3562296
* Factor 3.5 less cells in optimized version. Should also run 3.5x faster..?
type on the __left__, see it _rendered_ on the __right__.

# Added some cases at 08-01-2022
* For Breathing_base use either coarse or fine mesh found under Models, use snappyHexMesh
* copied latest kazuhide case, with latest timestep
* Most complicated CHCO_ke case, including geometry (identical to AC)
* simpler ke_AC_900_3600
  * for this one pay attention:
  * fields are already initialized for pressure and normalVelocity
  * run with mpirun -np 16 buoyantReactingFoam -parallel | tee log
  * stop the simulation at t=900 and run reconstructPar --latestTime
  * copy the 900 (or 901) folder to your new case, name it something like 901_3600
  * go into the controlDict and change the startTime, stopTime and writeInterval as mentioned
  * open the U file in 900/901 folder:
    * scroll all the way down and change emission surface value to uniform (0 0 0);
  * open the C10H16 file in 900/901 folder:
    * scroll all the way down and change emission surface value to uniform 0;
  * run decomposePar
    * after setting the decomposePar settings to your PC's specs optimal settings
  * When it's done, you're ready to run again:
  * mpirun -np <num-processor> buoyantReactingFoam -parallel | tee log
  * and in another window: pyFoamPlotWatcher --with-all log

Links:  
[link](thttps://o_a_website.com).


:tada: :fireworks:
