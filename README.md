# imoje-sdk

SDK for iMoje payment gateway provided by ING Bank

## Description

This package implements comunication with the payment gateway API described here:
  - https://data.imoje.pl/docs/api-transaction.pdf
  - https://data.imoje.pl/docs/api-paywall.pdf

## Implemented API features

- [ ] Transactions
  - [ ] Creating new transactions
  - [ ] Retrieving transaction data
  - [ ] Handling refunds
- [ ] Stats
  - [ ] Listing all transactions
  - [ ] Listing transactions – grouped by status
- [ ] Payment links
  - [ ] Creating payment links
  - [ ] Retrieving payment link data
  - [ ] Handling refunds
- [ ] Handling notifications
  - [ ] Method for handling webhook notifications (to be used with webserver) with source validation
- [ ] Other methods
  - [ ] Retrieving shops
  - [ ] Retrieving shop details
  - [ ] Setting trusted IPs


## Note

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
