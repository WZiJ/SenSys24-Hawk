# README for SenSys AE submission \#77 Hawk

## Project Overview

Hawk is an efficient non-intrusive sensing system capable of accurately identifying low-power appliances. In this Artifact Evaluation step, we will assess the items listed in the TODO List below.

Our goal is to earn three badges, and we welcome reviewers to raise any questions regarding the AE content through HotCRP at any time, as well as any issues encountered during execution or shortcomings in our AE process.

Due to the tight deadline, we will prioritize functional validation.

## TODO List

- [x] Sampling Synchronization
- [x] Dataset Balance Statistics
- [x] Algorithm Validation on HawkDATA
  - [x] Ablation Study: Impact of Differential Intervals
  - [x] Ablation Study: Impact of Dataset Balance
  - [x] Final Accuracy
- [x] BLUED Dataset

## Hardware and Software Requirements

### Hardware Requirements

Our validation is primarily functional, and we have already passed real-time validation on devices listed in Table 3 of the paper, including the Raspberry Pi 4B. Thus, similar or even better platforms should be supported.

- **CPU**: ARM A76 (Raspberry Pi 4B), Intel i7 or similar.
- **Memory**: At least 2GB RAM
- **Storage**: At least 10GB of free space. (For validation data)

### Software Requirements

The model in our project is in the standard XGBoost storage format. If reviewers wish to retrain the model, that is also possible, although they will need to upload our augmented training data (8-10.6GB). The training code does not have any particularly tricky aspects.

- **Project code**: You should clone this project at first.

- **Dataset download link**: Has been published anonymously [here]( https://www.kaggle.com/datasets/anonymous4data/ae-data-hawk). Please download the dataset (about 5.9G) at first. Then put the "HawkDATA" in project file. The dataset consist of two parts: HawkDATA for algorithm evaluation and raw data in `SPT-at-13m` during sampling synchronization for the following validation.

- **Operating System**: Linux (Ubuntu)

- **Python Version**: 3.9+

- **Necessary Libraries For Python**:
  - NumPy
  - XGBoost (version >= 2.0.3, pass on the 2.0.3 and 2.1.1)
  - Scikit-learn

## Experimental Validation Steps and Expected Results

### Experiment 1: Sampling Synchronization

- **Steps**:

  1. After downloading the complete dataset from the link, place the `SPT-at-13m` data file from downloaded dataset into the `./AE-process/1-SamplingSync/` folder.
  2. In the "./AE-process/1-SamplingSync/" folder, run `chmod +x ./run-stat.sh` and `./run-stat.sh`.
  3. After about 2 minutes, the maximum error from the 413 comparison samples (measured in sampling intervals, with each being 62.5µs at 16KHz) will be printed in the console. All absolute errors will be output to “./AE-process/1-SamplingSync/Result/syncErrList.txt”.

- **Expected Results**:

  - After running for about 2 minute, the maximum synchronization error should be displayed, aiming for a value below 1 sampling point (62.5µs), and it should align with "Our strategy(~13m)" in Figure 10 of the paper.

### Experiment 2: Dataset Balance Statistics

- **Steps**:

  1. Run the command `python ./StatDataBalance.py [path to hawkDATA]/hawkDATA/` directly in the `./Hawk/AE-process/2-DatasetBalance/` folder.

- **Expected Results**:
  - The final output shows an event BR rate of 0.214 (as the old detection program could not be found, the updated detection program differs slightly from the paper, but the impact is minor). The appliance ON BR is 0.877, and the average ON-OFF BR is 0.424, consistent with the results in Section 6.2 of the paper.

### Experiment 3: Algorithm Validation on HawkDATA

#### Experiment 3.1 Ablation Study: Impact of Differential Intervals

This parts are collected in  `./AE-process/3-Algorithm/`

- **Steps**:
  1. Modify line 7 in `tryPred.sh` to set the path: `python ./DiffLenInf.py [Path-to-HawkDATA]/HawkDATA/`.
  2. Run`chmod +x ./tryPred.sh` and `tryPred.sh` (this may take around 10 minutes) to calculate the recognition accuracy for each dataset at different differential intervals, and average the results to measure the impact of differential intervals on final accuracy.
  3. The full data output is located in the "./Result" folder, with summary results in `./Result/XGBoost-{differential interval}.txt`. Trend data will be printed in the console.
  4. Compare the output with Figure 15.

- **Expected Results**:
  - The output should match the results in Figure 15.

#### Experiment 3.2 Ablation Study: Impact of Dataset Balance

- **Overview**

- **Steps**:
  1. Modify line 7 in `tryPred.sh`: `python ./DiffLenInf.py [Path-to-HawkDATA]` to set the correct HawkDATA path.
  2. Run`chmod +x ./tryPred.sh` and  `./tryPred.sh` and wait for the calculation across 18 test sets, with results output.
  3. The final full results will be output in the "./Result" folder, with summary results in `./Result/XGBoost-30.txt`. Overall results will be printed in the console.

- **Expected Results**:
  - Compare the results with Figure 14. The FFT-XGBoost approach and the results with real imbalanced data should perform worse than in `./1-ImpactOfDI/Result/XGBoost-30.txt` (92.71%). We later discovered a small detail in training with imbalanced data that slightly improved accuracy compared to Figure 14, but the difference is small.

#### Experiment 3.3 Final Accuracy

  Please refer to the final output from Experiment 3.1 in "./Result/XGBoost-30.txt".
  
### Experiment 4 Evaluation on BLUED Dataset

- **Overview**

  For us, a significant challenge has been the lack of open-source code for some high-frequency NILM algorithms that claim strong performance on high-frequency datasets like BLUED. As a result, we did not directly compare with these SOTA methods on HawkDATA.

  Many related works divide validation on the BLUED dataset into Detection and Classification phases. Our comparison focuses on the performance in the second phase, while also validating our recognition of multi-state appliances.

- **Steps**:
  
  1. Navigate to the folder `./Hawk/AE-process/4-BLUED/` and run `python ./tryPredictEvent.py`.

- **Expected Results**:
  
  The program's output in the command line should match the results presented in Table 2.

#### We hope the AE process goes smoothly and feel free to ask any questions