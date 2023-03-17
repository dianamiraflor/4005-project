# SYSC 4005 Project

## RUN Instructions
Have python3 installed first.

Install the dependencies from main project directory.
```
pip install -r requirements.txt
```

Change working directory to /src and run:
```
python facility.py
```
To simulate the manufacturing facility.

<span style="color:red"> NOTE: To change simulation configurations, locate to /src/constants.py.</span>

Run:
```
python rng_tests.py
```
To perform uniform and autocorrelation tests on RNG.

Run:
```
python rvg.py
```
To generate a sequence of random variates as an input for the model.