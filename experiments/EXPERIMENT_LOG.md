# Experiment Log

While it would be nice to have a more automized system, 
instead we are going to manually record experiment runs
here. You might be tempted to skip this step because you
have confidence that you will remember later, or because
you're just mucking around. DO NOT SKIP THIS STEP. 

## Template
**Experiment name**:
**Commit hash before the experiment**:
**Description**:

## Logs

**Experiment name**: test_datalad
**Commit hash before the experiment**: 2c99e06
**Description**: Running some Ohio data through the base model just 
to test how datalad is working. 

**Experiment name**: test_datalad
**Commit hash before the experiment**: 9203e09
**Description**: Running some Ohio data through the polynomial 
model to test if datalad is working correctly through Erin's
user account. BAD PRACTICE TO HAVE ONE EXPERIMENT NAME FOR 
MULTIPLE VERSIONS OF THE CODE.

**Experiment name**: all_sap100
**Commit hash before the experiment**: 32e2d63
**Description**: The goal is to run all of De Bois's models on all of the SAP100
Tidepool data. We are not modifying the models in any way, so some of them might
fail. The big picture idea is to see if we get different results from a larger 
quantity of data.

**Experiment name**: sap100_6w
**Commit hash before the experiment**: 556e677
**Description**: Part 1/3 for the paper that we are writing in 
Spring 2024. In this experiment, we are running each of the SAP100
patients through all of De Bois's models, at all three PHs, 
with only 6 weeks of training (includes validation because of the
fancy cross-fold validation?) data to mimic the length of the Ohio
data. We are still using 60 days of test data for consistency across
all three time spans. Also, we only plotted the first 5 days for 
each patient to save space. We haven't yet figured out how to 
generate plots after the fact, though.

**Experiment name**: sap100_6w_gap
**Commit hash before the experiment**: 57a0000
**Description**: Based on discussions about sap100_6w, we decided to 
see if the performance of the model is affected by when the training
data is in relation to the test data. For consistency, in this 
experiment we are taking the 6 weeks of data at the start of the data
that will be used for the sap100_1y experiment. Patients will error
out if they do not have enough data. The hypothesis is that this experiment
will have worse RMSEs than sap100_6w because humans change over time. 

**Experiment name**: sap100_6w_early
**Commit hash before the experiment**: de735af
**Description**: To make the sap100_6w_gap experiment more meaningful,
we are testing if that same train dataset does better on the 60
days of data immediately after it as test data. This will also tell 
us if the accuracy changes wildly between different timeframes of
the same patient (baby cross validation). We expect RMSEs to be roughly
the same as sap100_6w, and better than sap100_6w_gap. 

**Experiment name**: sap100_4m
**Commit hash before the experiment**: 14f5299
**Description**: This experiment is a part of the original idea for 
comparisons on different lengths of training data. The test days 
are the last 60 days of the dataset, same as for sap100_6w (so that 
comparisons are fair). The training set is 4 months long. If the 
benefit of more data outweighs the downside of using old data, 
we expect to see improvements from sap100_6w.

**Experiment name**: run_ohio
**Commit hash before the experiment**: 52bbf47
**Description**: Run Ohio data using datalad to replicate De Bois's results
and compare to ours.
