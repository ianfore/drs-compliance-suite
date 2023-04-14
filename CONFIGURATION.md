# Configuration

The DRS service can be configured with custom properties, affecting behavior at runtime. This includes customization of the DRS database location, contents of the service info response, etc.

This document outlines how to configure the DRS service.

## Overview

The DRS compliance suite uses a user created config file which provides the compliance suite with information to use for testing the DRS server. This config file contains the auth info needed for service info and a list of DRS objects for the compliance suite to use to test with.

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

`none`: Object does not require auth to access. "auth_token" can be set as an empty string

`basic`: Object requires "auth_token" that is created using base64 encoding

`bearer`: Object requires "auth_token" containing bearer token

`passport`: Object requires "auth_token" containing a GA4GH passport


### DRS Objects

`drs_id`: Add the DRS id of the object being tested 

`auth_type`: Specify the auth type for accessing the object

`auth_token`: Supply the auth token for accessing the object

`is_bundle`: Indicate if the object is a bundle with "true" or "false" 

### DRS bundles and blobs

A Blob is a single DRS object without a contents array and therefore, no more stored DRS objects.A Blob is a single DRS object without a contents array and therefore, no more stored DRS objects.

DRS bundles are part of the DRS 1.2.0 spec. Bundle objects are DRS objects that have a 'contents' array containing more DRS objects stored as contents objects. These contents objects contain a 'contents' array that may contain more DRS objects.

In the config, a DRS object can be specified to be a bundle by setting the "is_bundle" value to "true"

