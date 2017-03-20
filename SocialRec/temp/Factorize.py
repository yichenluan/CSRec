from Data import *
import numpy as np
import sys

class MF(object):
    '''
    implement Matrix Factorization(data-U*M) for Recommend System
    '''
    def __init__(self,min=0,max=1):
        '''
        
        '''
        
        self._data = Data()
        self.min = min
        self.max = max
        
        
    def _init_U(self,force = False,num=1,k=100):
        '''
        initialization matrix U
        
        Parameter:
            force : if you want to specify the shape of U or not
            num : number of users
            k : number of features
        '''
        if not force:
            if (not self._u_num) or (not self._f_num):
                raise ValueError('You should run ')
            else:
                #TODO : what kind of initalization is suitable?
                self.U = 0.02*np.random.random((self._u_num,self._f_num))/np.sqrt(self._f_num)
        else:
            print 'Warning: you should have specified users number and features number.'
            self.U = 0.02*np.random.random( (num, k) )/np.sqrt(k)
            
    def _init_M(self,force = False,num=1,k=100):
        '''
        initialization matrix M
        
        Parameter:
            force : if you want to specify the shape of M or not
            num : number of items
            k : number of features
        '''
        if not force:
            if (not self._m_num) or (not self._f_num):
                raise ValueError('You should run ')
            else:
                self.M = 0.02*np.random.random((self._m_num,self._f_num))/np.sqrt(self._f_num)
        else:
            print 'Warning: you should have specified items number and features number.'
            self.M = 0.02*np.random.random( (num, k) )/np.sqrt(k)
    
    def _init_Y(self,force=False,num=1,k=100):
        '''
        initialization matrix Y
        
        Parameter:
            force : if you want to specify the shape of Y or not
            num : number of items
            k : number of features
        '''
        if not force:
            if (not self._m_num) or (not self._f_num):
                raise ValueError('You should run ')
            else:
                self.Y = 0.02*np.random.random((self._m_num,self._f_num))/np.sqrt(self._f_num)
        else:
            print 'Warning: you should have specified items number and features number.'
            self.Y = 0.02*np.random.random( (num, k) )/np.sqrt(k)
           
    def load_data(self, path, force=True, sep='\t', format=None, pickle=False,split=False):
        '''
        Loads data from a file
        
        Pamameter:
            path: file path
            force: Clearn already added data or not
            sep: Seperator among file
            format:Format of the file content. 
                Default format is 'value': 0 (first field), then 'row': 1, and 'col': 2.
                E.g: format={'row':0, 'col':1, 'value':2}. The row is in position 0, 
                then there is the column value, and finally the rating. 
                So, it resembles to a matrix in plain format
            pickle: if input file is a pickle file
        '''
        self._data.load(path, force, sep, format, pickle)
    
    def update(self,alpha = 0.001,remeda=0.05):
        '''
        update for every iteration.
        '''
        U = self.U
        M = self.M
        b_U = self.b_U
        b_M = self.b_M
        mask = self.mask
        mE = (self.data-np.dot(U,M.T)-self.overall_mean-b_U.repeat(self._m_num,axis=1)-b_M.repeat(self._u_num,axis=1).T)
        self.U = U + alpha*( np.dot(mask*mE,M) - remeda*U )
        self.M = M + alpha*( np.dot((mask*mE).T,U) - remeda*M )
        self.b_U = b_U + alpha*( (mask*mE).sum(axis=1).reshape(b_U.shape) - remeda*b_U)
        self.b_M = b_M + alpha*( (mask*mE).sum(axis=0).reshape(b_M.shape) - remeda*b_M)
        return ((mask*mE)**2).sum()
        

    def update_pp(self,alpha = 0.001,remeda=0.05):
        '''
        update for every iteration.
        '''
        U = self.U
        M = self.M
        Y = self.Y
        b_U = self.b_U
        b_M = self.b_M
        Ru = self.Ru
        mask = self.mask
        mE = (self.data-np.dot(U,M.T)-self.overall_mean-b_U.repeat(self._m_num,axis=1)-b_M.repeat(self._u_num,axis=1).T)
        Sum = (np.dot((mask*mE),M) * Ru.repeat(self._f_num,axis=1))
        self.U = U + alpha*( np.dot(mask*mE,M) - remeda*U )
        self.M = M + alpha*( np.dot((mask*mE).T,U + np.dot(self.data,Y)*(Ru.repeat(self._f_num,axis=1)) ) - remeda*M )
        self.b_U = b_U + alpha*( (mask*mE).sum(axis=1).reshape(b_U.shape) - remeda*b_U)
        self.b_M = b_M + alpha*( (mask*mE).sum(axis=0).reshape(b_M.shape) - remeda*b_M)
        for i in range(self._u_num):
            temp = np.dot(self.data[i].reshape(-1,1),Sum[i].reshape(1,-1))
            self.Y = Y + alpha *( temp - remeda*Y )
        return ((mask*mE)**2).sum()        
        
    def factorize(self,k=50,iter=100,alpha=0.001,remeda=0.05,descent=False,descent_rate=0.9,pp=False):
        '''
        Apply SGD for MF
        
        Parameter:
            k : number of features
            iter : number of iteration
            alpha : 
            remeda :
            descent : whether change alpha after every iteration
            descent_rate : 
            pp : run SVD++ algrithm or not
        '''
        
        try:
            self._u_num = self._data.row_max + 1
            self._m_num = self._data.col_max + 1
            self._f_num = k
        except:
            raise ValueError('you sould run MF.load_data first.')
        #TODO : what if users specify U and M's shape?
        if not hasattr(self,'U'):
            print('Init U')
            self._init_U()
        if not hasattr(self,'M'):
            print('Init M')
            self._init_M()
        if ( not hasattr(self,'Y') ) and pp:
            print('Init Y')
            self._init_Y()
        self.data = self._data.get_in_numpy_format()
        self.mask = self._data.get_mask()
        if ( not hasattr(self,'Ru') ) and pp:
            print('Init Ru')
            self.Ru = (( self.data.sum(axis=1) )** 0.5).reshape(-1,1)
        if not hasattr(self,'overall_mean'):
            print('Init overall_mean')
            self.overall_mean = self.data.sum()/self.mask.sum()
        #TODO : test if these expression is correct
        #self.b_U = data.sum(axis=0)/mask(axis=0)-self.overall_mean
        #self.b_M = data.sum(axis=1)/mask(axis=1)-self.overall_mean
        if not hasattr(self,'b_U'):
            print('Init b_U')
            self.b_U = np.zeros( (self._u_num,1) )
        if not hasattr(self,'b_M'):
            print('Init b_M')
            self.b_M = np.zeros( (self._m_num,1) )
        prvs = 1e12
        for i in range(iter):
            if not pp:
                cost = self.update(alpha,remeda)
            else:
                cost = self.update_pp(alpha,remeda)
            if( descent == True):
                alpha = alpha * descent_rate
            print 'Iteration:' + str(i+1) +': cost is ' + str(cost)
            sys.stdout.flush()
            if cost>prvs:
                print("model has converged.")
                break
            prvs = cost
            if (i%100 == 0) and (i != 0) :
                self.save_weight('tempweight_'+str(i)+'.pkl')
                
    def predict(self,user=None,item=None):
        '''
        Predict score given a user and a item.
        
        Parameter:
            user : user's id
            item : item's id
        '''
        #TODO : here assuming that user and item are given in integer form.
        try:
            assert user<=self._data.row_max
            assert item<self._data.col_max
        except:
            #self.CFpredict(user,item)
            None
        try:
            assert hasattr(self,'U')
            assert hasattr(self,'M')
            assert hasattr(self,'overall_mean')
            assert hasattr(self,'b_U')
            assert hasattr(self,'b_M')
        except:
            raise ValueError('You should run MF.factorize first to train the model.')
            
        try:
            score = self.overall_mean + self.b_U[user] + self.b_M[item] + np.dot(self.U[user],self.M[item].T)
        except:
            raise ValueError('user and item should be specified as integer.')
            
        score = max(score,self.min)
        score = min(score,self.max)
        
        return float(score)
        
        
    def CFpredict(self,user=None,item=None):
        '''
        predict score given a user and a item if the user or item is new here.
        
        Parameter:
            user : user's id
            item : item's id
        '''
        
        if user>self._data.row_max:
            #TODO : function userCF()
            users = userCF()
        else:
            users = [user]
        if item > self._data.col_max:
            #TODO : function itemCF()
            items = itemCF()
        else:
            items = [item]
        score = 0
        for u in users:
            for i in items:
                # TODO : how to meature weight
                score = score + weight*self.predict(i,u)
        
        return score

    def save_weight(self,path):
        pickle.dump([self.U, self.M, self.overall_mean, self.b_U, self.b_M],open(path,'w'))
    
    def load_weight(self,path):
        self.U, self.M, self.overall_mean, self.b_U, self.b_M = pickle.load(open(path,'r'))
