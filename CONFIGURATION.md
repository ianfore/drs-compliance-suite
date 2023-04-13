# Configuration

The DRS service can be configured with custom properties, affecting behavior at runtime. This includes customization of the DRS database location, contents of the service info response, etc.

This document outlines how to configure the DRS service.

## Overview

The DRS compliance suite uses a user created config file which provides the compliance suite with information on how to test the DRS implementation.

## Config file

Prepare your config file with the service info such as auth_type as well as a few DRS objects you are looking to test with.   

Example config file:
```
{
 "service_info": {
   "auth_type": "basic",
   "auth_token": "dXNlcm5hbWU6cGFzc3dvcmQ="
 },
 "drs_objects" : [
   {
     "drs_id": "697907bf-d5bd-433e-aac2-1747f1faf366",
     "auth_type": "none",
     "auth_token": "",
     "is_bundle": false
   },
   {
     "drs_id": "0bb9d297-2710-48f6-ab4d-80d5eb0c9eaa",
     "auth_type": "basic",
     "auth_token": "dXNlcm5hbWU6cGFzc3dvcmQ=",
     "is_bundle": false
   },
   {
      "drs_id" : "41898242-62a9-4129-9a2c-5a4e8f5f0afb",
      "auth_type": "bearer",
      "auth_token": "secret-bearer-token-1",
      "is_bundle": true
   },
   {
      "drs_id" : "a1dd4ae2-8d26-43b0-a199-342b64c7dff6",
      "auth_type": "passport",
      "auth_token": "43b-passport-a1d",
      "is_bundle": true
   }
 ]
}
```
### Auth types

'none': Requires nothing
'basic': Requires "auth_token" containing username and password
'bearer': Requires "auth_token" containing bearer token
'passport': Requires POST request with "passports" in the body 

As you can see from the example config, different DRS objects may have different requirements of auth type to access. 

### DRS bundles and blobs

A Blob is a single DRS object without a contents array and therefore, no more stored DRS objects.A Blob is a single DRS object without a contents array and therefore, no more stored DRS objects.

DRS bundles are part of the DRS 1.2.0 spec. Bundle objects are DRS objects that have a 'contents' array containing more DRS objects stored as contents objects. These contents objects contain a 'contents' array that may contain more DRS objects.

In the config, a DRS object can be specified to be a bundle by setting the "is_bundle" value to "true"

## serviceInfo

`serviceInfo` supports the following configurable attributes:

| Attribute | Description | Default |
|-----------|-------------|---------|
| id | unique identifier for the service in reverse domain name formant | org.ga4gh.starterkit.drs |
| name | short, human readable service name | GA4GH Starter Kit DRS Service |
| description | longer, human readable description | An open source community-driven implementation of the GA4GH Data Repository Service (DRS) API specification. |
| contactUrl | URL/email address users should contact with questions or issues about the service | mailto:info@ga4gh.org |
| documentationUrl | URL to where documentation about the service is hosted | https://github.com/ga4gh/ga4gh-starter-kit-drs |
| createdAt | timestamp of when the service was first started | 2020-01-15T12:00:00Z |
| updatedAt | timestamp of when the service was last updated | 2020-01-15T12:00:00Z |
| environment | describes what environment the service is running in (e.g. dev, test, prod) | test |
| version | the service version | 0.1.0 |
| organization.name | name of the organization hosting the service | Global Alliance for Genomics and Health |
| organization.url | URL to organization homepage | https://ga4gh.org |

