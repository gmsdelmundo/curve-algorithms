# Curve Algorithms

## Introduction
Simple programs were made to approximate a curve using the Ramer-Douglas-Peucker algorithm, and to evaluate a Bezier curve using DeCasteljau's algorithm. THey were made using Python 3.2.3.

## DeCasteljau's Algorithm and Bezier curve (Beziercurve.py)
This program uses DeCasteljau's algorithm to evaluate a Bezier curve.

## Ramer-Douglas_Peucker algorithm and Decasteljau's Algorithm (RDP-DCJ.py)
Using http://codereview.stackexchange.com/questions/49809/python-implementation-of-the-ramer-douglas-peucker-algorithm, I modified it to include DeCasteljau's algorithm after approximating a curve, and to draw out the curves using turtle. This was made for the 2015 Internal Robotics Competition to simulate a linear CCD reading and to tell a robot where to go based on the linear CCD reading.