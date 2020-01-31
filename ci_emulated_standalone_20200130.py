"""
Created on Jan. 26, 2020
@author: whyang

present the emulated CI(Comfort Index) of the running biji
 
"""

###
# USAGE (example of command)
# python ci_emulated_20200130.py --query one -p1 p1 -p2 p2 -p3 p3 -p4 p4 -p5 p5 -p6 p6 -p7 p7 -t temp
# python ci_emulated_20200130.py --query all -p1 1 -p2 1 -p3 1 -p4 1 -p5 1 -p6 1 -p7 1 -t 20
##

# -*- coding: utf-8 -*-
import pandas as pd
import argparse
import datetime

###
# declare functions
#

# query the CI based on the specific set of the parameters combination 
def queryCI(p1, p2, p3, p4, p5, p6, p7, temp, grade, rank, x1, x2, x3, x4):  
    # set initial value of the used variables
    CI = ''
    _rule = f1 = f2 = fci = 0
   
    # iterative loop of checking up on the three rules
    # check up on the rule 1
    if (p1 <= grade[4]) | (p2 <= grade[4]) | (p3 <= grade[4]) | (p4 <= grade[4]) | (p5 <= grade[4]) | (p6 <= grade[4]) | (p7 <= grade[4]):
        _rule = 1
        CI = rank[4]
    else:
        # check up on the rule 2
        if (
            ((p1 <= grade[3]) & (p2 <= grade[3])) | ((p1 <= grade[3]) & (p3 <= grade[3])) | ((p1 <= grade[3]) & (p4 <= grade[3])) | ((p1 <= grade[3]) & (p5 <= grade[3])) | ((p1 <= grade[3]) & (p6 <= grade[3])) | ((p1 <= grade[3]) & (p7 <= grade[3]))
            | ((p2 <= grade[3]) & (p3 <= grade[3])) | ((p2 <= grade[3]) & (p4 <= grade[3])) | ((p2 <= grade[3]) & (p5 <= grade[3])) | ((p2 <= grade[3]) & (p6 <= grade[3])) | ((p2 <= grade[3]) & (p7 <= grade[3]))
            | ((p3 <= grade[3]) & (p4 <= grade[3])) | ((p3 <= grade[3]) & (p5 <= grade[3])) | ((p3 <= grade[3]) & (p6 <= grade[3])) | ((p3 <= grade[3]) & (p7 <= grade[3]))
            | ((p4 <= grade[3]) & (p5 <= grade[3])) | ((p4 <= grade[3]) & (p6 <= grade[3])) | ((p4 <= grade[3]) & (p7 <= grade[3]))
            | ((p5 <= grade[3]) & (p6 <= grade[3])) | ((p5 <= grade[3]) & (p7 <= grade[3]))
            | ((p6 <= grade[3]) & (p7 <= grade[3]))) :
                _rule = 2
                CI = rank[3]
        else:
            # check up on the rule 3
            
            # get f1 
            minimum = lambda m, n: m if m <= n else n
            f1 = minimum(p1, p2)
            
            # get f2 
            f2 = minimum(p3*p4*p7, p5*p6*p7)
            
            if temp > 40:
                f2 = 0.0001
            else:
                if temp >12:
                    f2 = p3 * p4 * p7
                else:
                    if temp >= 0:
                        f2 = p5 * p6 * p7
                    else:
                        f2 = 0.0001
            
            # get fci                        
            fci = f1 * f2
            
            # indicate the qualified rule number
            _rule = 3 
            if (fci > x1):
                CI = rank[0]
            else:
                if (fci > x2):
                    CI = rank[1]
                else:
                    if (fci > x3):
                        CI = rank[2]
                    else:
                        if (fci > x4):
                            CI = rank[3]
                        else:
                            CI = rank[4]
    # end of the iterative loop of checking up on the three rules
    
    # present the checking result
    '''
    print('p1 = ', p1)
    print('p2 = ', p2)
    print('p3 = ', p3)
    print('p4 = ', p4)
    print('p5 = ', p5)
    print('p6 = ', p6)
    print('p7 = ', p7)
    print('temp = ', temp)
    print('x1 = ', x1)
    print('x2 = ', x2)
    print('x3 = ', x3)
    print('x4 = ', x4)
    print('p3*p4*p7 = ', p3*p4*p7)
    print('p5*p6*p7 = ', p5*p6*p7)    
    print('f1 = ', f1)
    print('f2 = ', f2)
    print('fci = ', fci)  
    print('**** rule = ', _rule)
    print('**** CI = ', CI)
    '''
    
    return CI, _rule
##
# end of queryCI(..)
#

# query the CIs based on the all sets of the parameters combination 
def queryallCI(grade, rank, x1, x2, x3, x4):    
    ##
    # seperate to five parts to gather the emulated results depending on the element of the parameter p1
    #
    df = ['df0', 'df1', 'df2', 'df3', 'df4'] # dataframe's name corresponding to each part
    name = datetime.datetime.now().strftime("%Y%m%d") # get the date of today
    df_filename = ['AQI=優_'+name, 'AQI=好_'+name, 'AQI=普通_'+name, 'AQI=不良_'+name, 'AQI=劣_'+name] # filename of each partg
 
    i = 0
    # iterative loop based on the p1
    for p1 in grade:
        filename = 'ci_emulated_'+df_filename[i]+'.csv'
        print('**** p1 = ', p1)
        # given the column names of the table
        df[i] = pd.DataFrame(columns=('p1(AQI)', 'p2(PM2.5)', 'p3(HI)', 'p4(UVI)', 'p5(WCI)', 'p6(WR)', 'p7(RF)', 
                                      'temperature', 'CI(Rank)','qualified_rule'))
        # iterative loop
        for p2 in grade:
            for p3 in grade:
                for p4 in grade:
                    for p5 in grade:
                        for p6 in grade:
                            for p7 in grade:
                                for temp in temp_period:
                                    _CI, _rule = queryCI(p1, p2, p3, p4, p5, p6, p7, temp, grade, rank, x1, x2, x3, x4)
                                    # construct the content of a row in the table
                                    s = pd.Series({'p1(AQI)':p1,
                                                   'p2(PM2.5)':p2,
                                                   'p3(HI)':p3,
                                                   'p4(UVI)':p4,
                                                   'p5(WCI)':p5,
                                                   'p6(WR)':p6,
                                                   'p7(RF)':p7,
                                                   'temperature':temp,
                                                   'CI(Rank)':_CI,
                                                   'qualified_rule':_rule})
                                    df[i] = df[i].append(s, ignore_index=True)
        # end of iterative loop
        ##
        # drop out to store as a file
        #
        df[i].to_csv(filename, index=False, encoding='cp950')
        i += 1
    # end of iterative loop based on the p1
    
    return True
##
# end of queryallCI(..)
#
   
###
# main program
#

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True, help="query one CI or all of the CIs based on the set of parameters combination")
ap.add_argument("-p1", "--parameter1", required=True, help="p1: AQI")
ap.add_argument("-p2", "--parameter2", required=True, help="p2: PM 2.5")
ap.add_argument("-p3", "--parameter3", required=True, help="p3: HI")
ap.add_argument("-p4", "--parameter4", required=True, help="p4 UVI")
ap.add_argument("-p5", "--parameter5", required=True, help="p5: WCI")
ap.add_argument("-p6", "--parameter6", required=True, help="p6: WR")
ap.add_argument("-p7", "--parameter7", required=True, help="p7: RF")
ap.add_argument("-t", "--temperature", required=True, help="temp: temperature")
args = vars(ap.parse_args())

if __name__ == '__main__':
    ##
    # query specific parameter combination for the emulated CI
    # set the value of the each parameter
    grade = [1, 0.9, 0.8, 0.4, 0.2] # g1, g2, g3, g4 and g5 w.r.t. 優, 好, 普通, 不良 and 劣
    rank = ['優', '好', '普通', '不良', '劣']
    temp_period = [41, 13, 0, -1]
    x1 = pow(grade[1], 4)
    x2 = pow(grade[2], 4)
    x3 = pow(grade[3], 4)
    x4 = pow(grade[4], 4)
    
    if args['query'] == 'all':
        ##
        # query all parameters combination for the emulated CI 
        queryallCI(grade, rank, x1, x2, x3, x4)
        print('**** finished')
    elif args['query'] == 'one':   
        p1 = float(args['parameter1']) 
        p2 = float(args['parameter2'])
        p3 = float(args['parameter3'])
        p4 = float(args['parameter4'])
        p5 = float(args['parameter5'])
        p6 = float(args['parameter6'])
        p7 = float(args['parameter7'])
        temp = float(args['temperature'])
        # call queryCI() to get the result        
        _CI, _rule = queryCI(p1, p2, p3, p4, p5, p6, p7, temp, grade, rank, x1, x2, x3, x4)
        # present the query result
        print(_CI)
        print(_rule)
        print('**** finished')
    else:
        print('**** error: input argument')
    
    print('== end of query ==')
                    
#######################################################################################
# end of file                                                                         #
#######################################################################################