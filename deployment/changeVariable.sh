#!/bin/bash

sed  "s/imagename/$1\/$2:$3/g" deployment/email-notification.yaml > deployment/$2:$3.yaml
sed  "s/nodeport/$4/g" deployment/rabbitmq-deploy.yaml > deployment/$5-rabbitmq-deploy.yaml

echo $3
echo $2:$3