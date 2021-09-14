#!/bin/bash

sed  "s/imagename/$1\/$2/g" ../deployment/email-notification.yaml > ../deployment/$2.yaml