#!/bin/bash

sed  "s/imagename/$1\/$2/g" deployment/email-notification.yaml > deployment/hhhh.yaml
sed  "s/nodeport/$4/g" deployment/rabbitmq-deploy.yaml > deployment/$5-rabbitmq-deploy.yaml

echo $3
echo $2:$3