# SYSC 4005 Project

## RUN Instructions
Have python3 installed first.

Install the dependencies from main project directory.
```
pip install -r requirements.txt
```

Run:
```
python rng_tests.py
```
To perform uniform and autocorrelation tests on RNG.

### RUN SIMULATION 

Run:
```
python rvg.py
```
To generate a sequence of random variates as an input for the model.

<span style="color:red"> NOTE: It's important that the random variates are generated first.</span>


Change working directory to /src and run:
```
python facility.py
```
To simulate the manufacturing facility.

<span style="color:red"> NOTE: To change simulation configurations, locate to /src/constants.py.</span>

NOTE: Little's Law stats is only generated when the simulation type is NORMAL


## REMINDERS WHEN READING THROUGH CODE
buffer1 = C1 Buffer of Workstation 1
buffer2 = C1 Buffer of Workstation 2
buffer3 = C2 Buffer of Workstation 2
buffer4 = C1 Buffer of Workstation 3
buffer5 = C3 Buffer of Workstation 3
