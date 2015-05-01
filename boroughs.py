#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A module for boroughs."""

import csv
import pprint 

grades = {
    'A': float(1),
    'B': float(.9),
    'C': float(.8),
    'D': float(.7),
    'F': float(.6),
}

def get_score_summary(filename):
    fhandler = open(filename, 'r')
    reader = csv.reader(fhandler)
    data = {}
    
    for line in reader:
        camis = line[0]
        grade = line[10]
        boro = line[1]
        if grade != 'P' and grade != '':
            data[camis]=[grade, boro]
    pprint.pprint(data)
    fhandler.close()

    restsum = {}
    
    for grade in data.itervalues():
        pprint.pprint(data)
        letter = grade[0]
        boros = grade[1]
        restsum = {boros: letter}
        print restsum
        
        
  















#if __name__ == '__main__':
 #   test = get_score_summary('inspection_results.csv')
