"""
NumRec Project: Part 1
Dominic Sorrell
"""
import numpy as np
import matplotlib.pylab as pl

class Decay(object):
    
    """This class generates & plots a set of random events. 
    
    The distribution of x, y is given by a PDF, which itself is a combination 
    of two other PDFs.
    """
    
    def __init__(self, f, g, tau1, tau2, n, frac):
        
        self.tau1 = tau1
        self.tau2 = tau2
        self.n = n
        self.frac = frac
        self.f = f
        self.g = g

    def generate(self, limit, frac, func_max):
        
        """This method executes the "in the box" approach. 
        
        The method calculates random values for x and y and evaluates pdf1 and 
        pdf2 at these points.The total PDF is found and then a test is 
        performed on this value. If the value of the PDF exceeds the test 
        value, it is returned for storage; otherwise, the "generate" method 
        repeats.
        """
        a = np.random.uniform()
        b = np.random.uniform()
        
        # The values for x and y are determined by bringing a random number 
        # from 0 to 1 into the range dictated by "limit" (a 2D array 
        # containing the limits on x and y).
        
        self.x = limit[0,0] + (limit[0,1] - limit[0,0])*a
        self.y = limit[1,0] + (limit[1,1] - limit[1,0])*b
        
        pdf1 = self.f(self.x, self.y, self.tau1)
        pdf2 = self.g(self.x, self.y, self.tau2)
        self.pdf_total = (frac*pdf1) + ((1.0 - frac)*pdf2)    # Weighted sum of pdf1/2.
        
        
    def compare(self, limit, frac, func_max):
        
        """test = func_max*np.random.uniform()
        self.generate(limit, frac, func_max)
        while test > self.pdf_total:
            self.generate(limit, frac, func_max)
            test = func_max*np.random.uniform()
        else:
            return self.pdf_total, self.x, self.y"""

        while True:
        
            x = limit[0,0] + (limit[0,1] - limit[0,0])*np.random.uniform()
            y = limit[1,0] + (limit[1,1] - limit[1,0])*np.random.uniform()
            test = func_max*np.random.uniform()
            pdf1 = self.f(x, y, self.tau1)
            pdf2 = self.g(x, y, self.tau2)
            pdf_total = (frac*pdf1) + ((1.0 - frac)*pdf2)    # Weighted sum of pdf1/2.
            
            if test < pdf_total:
                break
        return pdf_total, x, y
        
    def data(self, limit, frac, func_max):
        
        """This method stores the values of the pdf.
        
        It creates a numpy array of length n and fills it with 
        zeros. As numbers are collected from the generate method, they are 
        placed in the array as a way of storing the lifetime data.
        """		
        self.store = np.zeros(self.n)
        self.x_data = np.zeros(self.n)
        self.y_data = np.zeros(self.n)
        for i in range(self.n):
            self.store[i], self.x_data[i], self.y_data[i] = self.compare(limit,
                      frac, func_max)
            print(str((float(i)/self.n)*100)+'%')
        #print(self.store)
       
    def graph(self):
        
        """Plots histograms with x, y and z."""
        
        pl.figure()
        pl.xlabel('theta')
        pl.hist(self.x_data, bins=100)
        
        pl.figure()
        pl.xlabel('t')
        pl.hist(self.y_data, bins=100)
        
        pl.figure()
        pl.xlabel('PDF')
        pl.hist(self.store, bins=100)
        
        pl.show()
