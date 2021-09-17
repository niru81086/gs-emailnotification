#!/bin/bash

sed  "s/imagename/$1\/$2:$3/g" deployment/email-notification.yaml > deployment/$2.yaml
sed  "s/nodeport/$4/g" deployment/rabbitmq-deploy.yaml > deployment/$5-rabbitmq-deploy.yaml
