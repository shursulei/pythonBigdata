#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pandas as pd

from ... import INPUT_DIR, set_delimiter, OUTPUT_DIR


def readwrite(input_file,output_file):
    df = pd.read_csv(input_file,usecols=[0, 1],names=["ym", "uid"])
    print(df)
    df.to_csv(output_file, sep=',', header=True, index=False,encoding="UTF-8")


if __name__ == '__main__':
    readwrite(INPUT_DIR+'company_active.csv',OUTPUT_DIR+'company_active.csv')
    readwrite(INPUT_DIR + 'yiye_active.csv', OUTPUT_DIR + 'yiye_active.csv')
    readwrite(INPUT_DIR + 'insurance_active.csv', OUTPUT_DIR + 'insurance_active.csv')