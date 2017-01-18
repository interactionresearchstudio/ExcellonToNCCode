# ExcellonToNCCode
A script that converts Excellon drill data to CNC-able Roland NC code. We use this for performing the drill operations on our homebrew printed circuit boards with our Roland iModela mini CNC. 

## Input file
We have currently tested this with CircuitMaker's Excellon drill files, but it should work with most other Excellon files. They seem to be pretty standardised. 

## Usage
Run the python script as follows:
        
        python ExcellonToNCCode.py /path/to/excellon

The script will process the file and spit out an NC code file with the same name, but the `*.nc` extension. 

## A note on machines
We have only tried this with our iModela machine, but most Roland CNCs accept NC code. However, *please be cautious*. Use at your own risk and always supervise your CNC!
