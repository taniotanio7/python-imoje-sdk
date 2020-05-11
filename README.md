# imoje-sdk

SDK for imoje payment gateway provided by ING Bank.

Please note that this client library is a Work In Progress and should not be used in production applications.

## Description

This package implements communication with the payment gateway API described here: https://data.imoje.pl/docs/api-transaction.pdf

## Implemented API features

- [x] Transactions
  - [x] Creating new transactions
  - [x] Retrieving transaction data
  - [x] Handling refunds
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
