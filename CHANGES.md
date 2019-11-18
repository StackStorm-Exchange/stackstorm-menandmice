# Change Log

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
