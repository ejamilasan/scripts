#!/bin/bash

profile=$1
region=$2

instances=`aws ec2 describe-volumes \
	--profile $profile \
	--region $region \
	--filters Name=encrypted,Values=false Name=attachment.status,Values=attached | \
	jq -r '.Volumes[].Attachments[] | [.InstanceId] | @csv' | sort -n | uniq`

for instance in $instances;
do
  	name=`aws ec2 describe-tags \
		--profile $profile \
		--region $region \
		--filters Name=resource-id,Values=$instance Name=key,Values=Name \
		--query Tags[].Value | \
		jq -r '.[0]'`
	echo "$instance,$name"
done
