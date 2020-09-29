#!/bin/bash
set -eo pipefail
aws cloudformation package --template-file template.yml --s3-bucket $ARTIFACT_BUCKET --output-template-file out.yml
aws cloudformation deploy --template-file out.yml --stack-name $AWS_STACK_NAME --capabilities CAPABILITY_NAMED_IAM