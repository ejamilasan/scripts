#!/bin/bash

# this script will return the names of the instances with non-encrypted ebs volumes by providing the aws account and region that you want to survey.


profile=$1  # aws alias
region=$2   # aws region

instances=`aws ec2 describe-volumes --profile $profile --region $region  --filters Name=encrypted,Values=false Name=attachment.status,Values=attached | jq -r '.Volumes[].Attachments[] | [.InstanceId] | @csv' | sort -n | uniq`

for instance in $instances;
do
        name=`aws ec2 describe-tags --profile $profile --region $region --filters Name=resource-id,Values=$instance Name=key,Values=Name --query Tags[].Value | jq -r '.[0]'`
        echo "$instance,$name"
done
