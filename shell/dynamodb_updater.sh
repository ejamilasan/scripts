#!/bin/bash

# Writes a timestamp to each item in a DynamoDB table

table=$1

itemIds=$(aws dynamodb scan --table-name "$table" --query "Items[*].[itemId.S]" --output text)

for itemId in $itemIds; do
  echo "Updating $itemId"

  aws dynamodb update-item \
    --table-name "$table" \
    --key "{\"itemId\":{\"S\":\"${itemId//[$'\t\r\n ']}\"}}" \
    --update-expression "SET timestamp = :current_time" \
    --expression-attribute-values "{\":current_time\": {\"S\": \"$(date '+%F-%H-%M-%S')\"}}" \
    --return-values UPDATED_NEW

  echo "Completed $itemId"
  echo ""
done

