#!/bin/bash

sed  "s/imagename/$1\/$2/g" deployment/email-notification.yaml > deployment/$2.yaml
sed  "s/nodeport/$3/g" deployment/rabbitmq-deploy.yaml > deployment/$2-rabbitmq-deploy.yaml