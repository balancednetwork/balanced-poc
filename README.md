# Balanced Contracts

## Basic Loans PoC on Testnet

Running the Balanced Clean Install Jupyter notebook will install all contracts necessary to try out this release if you would like to do that locally on tbears.

### Functions Available
* Deposit ICX Collateral and Originate an ICD Loan in one transaction
* Deposit ICX Collateral
* Originate an ICD Loan
* Repay an ICD Loan
* Withdraw Some Collateral as sICX

This release was tested on the current latest tbears Docker image.

If you have Docker running on your system, you can install and run the latest tbears Docker image from the terminal using the command

`docker run -it --name tbears-container -p 9000:9000 iconloop/tbears:1.7.1&`
