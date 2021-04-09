# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 17:55:26 2021

@author: pjdys
"""

import pandas as pd

#%% read and combine datasets
data_f = pd.read_csv(r'freMTPLfreq.csv').set_index('PolicyID').drop('Unnamed: 0', axis='columns')
data_s = pd.read_csv(r'freMTPLsev.csv').set_index('PolicyID').drop('Unnamed: 0', axis='columns')

data_ult = data_f.join(data_s)


#%% 'CURRENT IBNR POLICY SET' create sample of claims for givent policies

incurred_to_ultimate = 0.65 # by claim count

data_s_sample = data_s.sample(int(incurred_to_ultimate*len(data_s)))
data_sample = data_f.join(data_s_sample)

#%% summarise output

ult_claim_value = data_ult['ClaimAmount'].sum()
ult_claim_count = data_ult['ClaimAmount'].count()

inc_claim_value = data_sample['ClaimAmount'].sum()
inc_claim_count = data_sample['ClaimAmount'].count()

summary = pd.DataFrame.from_dict({'ultimate calim value': ult_claim_value,
           'ultimate claim count': ult_claim_count,
           'incurred claim value': inc_claim_value,
           'incurred claim count': inc_claim_count,
           'ibnr value': ult_claim_value-inc_claim_value,
           'ibnr count': ult_claim_count-inc_claim_count}, orient='index')

print(summary)

#%% write output

data_ult.to_csv('data ultimate policy data.csv')
data_sample.to_csv('data incurred claims only.csv')
summary.to_csv('data summary.csv')



