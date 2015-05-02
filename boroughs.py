#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A module for boroughs."""

import csv
import json
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
    next(reader)
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


def get_market_density(filename):
    """Docstring.

    """
    fhandler = open(filename, 'r')
    jdata = json.load(fhandler)['data']
    final_data = {}
    fhandler.close()

    for data in jdata:
        data[8] = data[8].strip()
        if data[8] not in final_data.iterkeys():
            val = 1
        else:
            val = final_data[data[8]] + 1

        final_data[data[8]] = val
        final_data.update(final_data)

    return final_data


def correlate_data(csv='inspection_results.csv',
                   markets='green_markets.json',
                   combine='overall_data.json'):
    """Docstring.

    """
    score_data = get_score_summary(csv)
    market_data = get_market_density(markets)
    combine_data = {}

    for item2 in market_data.iterkeys():
        for item1 in score_data.iterkeys():
            if item1 == str(item2).upper():
                val1 = score_data[item1][1]
                val2 = float(market_data[item2]) / (score_data[item1][0])
                combine_data[item2] = (val1, val2)
                combine_data.update(combine_data)
    jdata = json.dumps(combine_data)
    pprint.pprint(combine_data)

    fhandler = open(combine, 'w')
    fhandler.write(jdata)
    fhandler.close()





if __name__ == '__main__':
    test = get_score_summary('inspection_results.csv')
    test2 = get_market_density('green_markets.json')
