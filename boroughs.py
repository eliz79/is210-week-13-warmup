#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A module for boroughs."""

import json

GRADE_SCALE = {
    'A': float(1.0),
    'B': float(0.9),
    'C': float(0.8),
    'D': float(0.7),
    'F': float(0.6)
}


def get_score_summary(filename):
    """To open and reads csv file and return a summary of data.

    Args:
        fhandler: opens a file in read form.
        line: skips top line from file
        data(dict): a dict for score data.

    Returns:
        None

    Examples:
        >>> get_score_summary('inspection_results.csv')
        >>> {'BRONX': (156, 0.9762820512820514), 'BROOKLYN':
        (417, 0.9745803357314141), 'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331531), 'QUEENS':
        (414, 0.9719806763285017)}
    """
    fhandler = open(filename, 'r')
    data = {}

    fhandler.readline()
    line = fhandler.readline()

    while line:
        lineparts = line.split(',')
        grade = lineparts[10].strip().upper()
        if grade in GRADE_SCALE:
            data[lineparts[0].strip()] = {'boro': lineparts[1].strip().upper(),
                                          'grade': GRADE_SCALE[grade]}
        line = fhandler.readline()
    fhandler.close()

    summary = {}
    for values in data.itervalues():
        if values['boro'] not in summary:
            summary[values['boro']] = {'count': 1, 'grade': values['grade']}
        else:
            summary[values['boro']]['count'] += 1
            summary[values['boro']]['grade'] += values['grade']

    result = {}
    for boro, data in summary.iteritems():
        result[boro] = (data['count'], data['grade'] / data['count'])

    return result


def get_market_density(filename):
    """Opens a file using json to store data in a dict.
    Args:
        fhandler: opens file in read form.
        data: to loads json file
        boros(dict): new dict for market density.

    Returns:
        market_data (dict) = Market density data.

    Examples:
        >>> get_market_density('green_markets.json')
        {u'STATEN ISLAND': 2, u'BROOKLYN': 48, u'BRONX': 32,
        u'MANHATTAN': 39, u'QUEENS': 16}
    """
    fhandler = open(filename)
    data = json.load(fhandler)['data']
    fhandler.close()

    boros = {}

    for market in data:
        boro = market[8].strip().upper()
        if boro not in boros:
            boros[boro] = 1

        else:
            boros[boro] += 1

    return boros


def correlate_data(restaurants, green_markets, outfile):
    """Combines data for restaurants and markets.
    Args:
        rdata:(dict): restaurant score summary.
        mdata(dict):market density summary.

    Returns:
        correlated(dict): a combined dict.

    Example:
        {'BRONX': (0.9762820512820514, 0.1987179487179487)}
    """
    rdata = get_score_summary(restaurants)
    mdata = get_market_density(green_markets)

    correlated = {}
    for boro, data in rdata.iteritems():
        if boro in mdata:
            density = float(mdata[boro]) / data[0]
            correlated[boro] = (data[1], density)
    fhandler = open(outfile, 'w')
    json.dump(correlated, fhandler)
    fhandler.close()

    return correlated
