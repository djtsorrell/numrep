"""
NumRep Project: Parts 2 & 3
Dominic Sorrell
"""
import numpy as np
from iminuit import Minuit
import matplotlib.pylab as plt

class Likelihood(object):
    
    def __init__(self, f, g, h, i, tau1, tau2, filename):
        
        data = np.loadtxt(open(filename, "r"))
        self.x = data[:,1]
        self.y = data[:,0]
        self.f = f
        self.g = g
        self.h = h
        self.i = i
        self.tau2 = tau2
        
    def log_partial(self, F, tau1, tau2):
            
        pdf1 = self.h(self.y, tau1)
        pdf2 = self.i(self.y, tau2)
        pdf_total = np.add((F*pdf1) , ((1.0 - F)*pdf2))
        return -1.0*(np.sum(np.log(pdf_total)))
    
    def log_full(self, F, tau1, tau2):
        
        pdf1 = self.f(self.x, self.y, tau1)
        pdf2 = self.g(self.x, self.y, tau2)
        pdf_total = (F*pdf1) + ((1.0 - F)*pdf2)
        return -1.0*(np.sum(np.log(pdf_total)))
    
    def minimise(self, task):
        
        if task == 2:
            m = Minuit(self.log_partial, F=0.5, tau1=1.0, tau2=2.0,
                       limit_F=(0,1), limit_tau1=(0.000001,10),
                       limit_tau2=(0.000001,10), errordef=0.5, pedantic=False)            
        if task == 3:
            m = Minuit(self.log_full, F=0.5, tau1=1.0, tau2=2.0, limit_F=(0,1),
                   limit_tau1=(0.000001,10), limit_tau2=(0.000001,10),
                   errordef=0.5, pedantic=False)
        fmin, param = m.migrad()    # Runs the minimiser.
        #m.minos()    # Calculates the errors.
        #print(m.values)
        print(m.errors)
        self.param = m.values
        self.param_no = len(m.values)
        
        # The rest of this method is a specific plotting procedure for Minuit.
        
        plt.figure()
        m.draw_profile('F')
        
        plt.figure()
        m.draw_profile('tau1')
        
        plt.figure()
        m.draw_profile('tau2')
        
        plt.show()
        
    def error_simple(self, task, increment):
        
        if task == 2:
            
            log_base = self.log_partial(self.F, self.tau1, self.tau2)
            
            for i in range(self.param_no):
                
                param_new = [self.param[0], self.param[1], self.param[2]]
                
                while True:
                    
                    param_new[i] += increment
                    log = self.log_partial(param_new[0], param_new[1],
                                           param_new[2])
                    diff = log - log_base
                
                    if diff > 0.5:
                        
                        break
                
                error = param_new[i] - self.param[i]
                print("Error " +str(i) +" = " +str(error))
        
        if task == 3:
            
            log_base = self.log_full(self.F, self.tau1, self.tau2)
            
            for i in range(self.param_no):
                
                param_new = [self.param[0], self.param[1], self.param[2]]
                
                while True:
                    
                    param_new[i] += increment
                    log = self.log_full(param_new[0], param_new[1],
                                           param_new[2])
                    diff = log - log_base
                
                    if diff > 0.5:
                        
                        break
                
                error = param_new[i] - self.param[i]
                print("Error " +str(i) +" = " +str(error))
                
    def error_proper(self, task, parameter, increment):
        
         if task == 2:
            
            print 
            log_base = self.log_partial(self.param[0], self.param[1],
                                        self.param[2]) 
            param_new = [self.param[0], self.param[1], self.param[2]]
                
            if parameter == 'F':
                while True:
                    
                    param_new[0] += increment
                    m = Minuit(self.log_partial, F=param_new[0],
                               tau1=param_new[1], tau2=param_new[2], 
                               fix_F=True, limit_F=(0,1), 
                               limit_tau1=(0.000001,10), 
                               limit_tau2=(0.000001,10), errordef=0.5, 
                               pedantic=False)
                    fmin, param = m.migrad()
                    param_new = m.values
                    log = self.log_partial(param_new[0], param_new[1],
                                           param_new[2])
                    diff = log - log_base
                
                    if diff > 0.5:
                        
                        break
                
                error = param_new[0] - self.param[0]
                print("Error = " +str(error))
                
            if parameter == 'tau1':
                while True:
                    
                    param_new[1] += increment
                    m = Minuit(self.log_partial, F=param_new[0],
                               tau1=param_new[1], tau2=param_new[2], 
                               fix_tau1=True, limit_F=(0,1), 
                               limit_tau1=(0.000001,10), 
                               limit_tau2=(0.000001,10), errordef=0.5, 
                               pedantic=False)
                    fmin, param = m.migrad()
                    param_new = m.values
                    log = self.log_partial(param_new[0], param_new[1],
                                           param_new[2])
                    diff = log - log_base
                
                    if diff > 0.5:
                        
                        break
                
                error = param_new[1] - self.param[1]
                print("Error = " +str(error))
    