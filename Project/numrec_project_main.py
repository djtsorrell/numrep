"""
NumRec Porject main
Dominic Sorrell
"""
import math as m
import numpy as np
import winsound as ws

from numrec_project_1 import Decay
from numrec_project_2 import Likelihood
    
def f(x, y, z):
    
    """This function calculates the first component of the PDF for the decay of
    particle X.
    """
    norm = 3.0*m.pi*z*(1.0 - np.exp(-10.0/z))
    return (1.0/norm)*(1.0 + (np.cos(x))**2.0)*np.exp(-y/z)

def g(u, v, w):
    """Calculates the second component of the PDF."""
    norm = 3.0*m.pi*w*(1.0 - np.exp(-10.0/w))
    return (1.0/norm)*(3.0*(np.sin(u))**2.0)*np.exp(-v/w)

def h(y, z):
    """Calculates the marginalised PDF (first component) for y."""
    norm = 3.0*m.pi*z*(1.0 - np.exp(-10.0/z))
    return (1.0/norm)*3*m.pi*np.exp(-y/z)

def i(v, w):
    """Calculates the marginalised PDF (second component) for y."""
    norm = 3.0*m.pi*w*(1.0 - np.exp(-10.0/w))
    return (1.0/norm)*3*m.pi*np.exp(-v/w)

def main(f, g, h, i):
     
    tau1 = 1.0
    tau2 = 2.0
    n = 10000
    frac = 0.5
    limit = np.array([[0,2*m.pi],[0,10]])
    decay = Decay(f, g, tau1, tau2, n, frac)
    #decay.data(limit, frac, 0.17)
    #decay.graph()
    
    filename = "datafile-Xdecay.txt"
    like = Likelihood(f, g, h, i, tau1, tau2, filename)
    task = input("Task (2/3) = ")
    like.minimise(task)
    #like.error_simple(task, 0.0001)
    like.error_proper(task, 'tau1', 0.0001)
    ws.Beep(500,1000)
    
    
main(f, g, h, i)