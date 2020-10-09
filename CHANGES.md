# Change Log

## v1.3.0

* test_ip_address - ping_address input added to decide if the address should be pinged before claiming the address.
* dns_record_claim - ping_address input added to decide if the address should be pinged before claiming the address.
  Contributed by Bradley Bishop (Encore Technologies)

## v1.2.0

* Test_range workflow updated utilization logic and added address reservation checking
  Contributed by Alex Chrystal (Encore Technologies)

## v1.1.2

* Fixed entry point in login action.
  Contributed by Bradley Bishop (Encore Technologies)

## v1.1.1

* Added test_range action and workflow to test if range has available addresses
* Added test_ip_address action and workflow to test if a given ip address is available for use
* Updated dns_record_claim to test ip addresses if given and test range before claiming.
* Updated dns_record_claim to flush dns cache after new record is created.
  Contributed by Bradley Bishop (Encore Technologies)

## v1.0.2

* Fixed issue with test_credentials and remove_dns_record where name filter was not correct.
  Contributed by Bradley Bishop (Encore Technologies)

## v1.0.1

* Fixed issue with test_credentials not exiting with fail.
  Contributed by Bradley Bishop (Encore Technologies)

## v0.1.4

* Added action/workflow to get all dns records and related records in a given dns zone.
* Added action/workflow to claim a dns record.
* Converted all workflows to orquesta.
  Contributed by Bradley Bishop (Encore Technologies)

## v0.1.3

* Added action/workflow to delete dns record and all associated related records and PTR records.
* Added action/workflow to return FQDN based on name and DNS Zone Reference.
* Added action/workflow to test if a hostname is available or not
* Added action/workflow to test credentials against the Men&Mice server.

## v0.1.2

* Added support for self-signed SSL certificates.

## v0.1.1

* Updated the required parameter to use the proper capitalization of `false` for use in JSON schema
* Merged our latest makefile
* Fixed an issue in the `wf_add_dns_zone` example workflow where it was trying to call another workflow instead of an action

## v0.1.0

Initial Revision.
Generated actions from Men&Mice v8.1
