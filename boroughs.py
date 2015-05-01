#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A module for boroughs."""

import csv
import pprint

GRADES = {
    'A': float(1.0),
    'B': float(.9),
    'C': float(.8),
    'D': float(.7),
    'F': float(.6)
}


def get_score_summary(filename):
    """Docstring.

    """
    fhandler = open(filename, 'r')
    reader = csv.reader(fhandler)
    next(reader) #removes top line in csv file
    data = {}    
    for line in reader:
        camis = line[0]
        grade = line[10]
        boro = line[1]
        if grade != 'P' and grade != '':
            data[camis] = [grade, boro]
    fhandler.close()

    restsum = {}
    for boro in data.values():
        if boro[1] not in restsum:
            restsum[boro[1]] = [1, GRADES[boro[0]]]
        else:
            restsum[boro[1]][0] += 1
            restsum[boro[1]][1] += GRADES[boro[0]]

    final = {}
    for boro, grade in restsum.iteritems():
        final[boro] = (grade[0], grade[1] / grade[0])
    return final




if __name__ == '__main__':
    test = get_score_summary('inspection_results.csv')
