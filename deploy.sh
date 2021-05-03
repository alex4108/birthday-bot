#!/usr/bin/env 
set -ex

if [[ "${TRAVIS}" == "true" ]]; then
    AWS_PROFILE_NAME="default"
else
    AWS_PROFILE_NAME="aschittko"
fi

timestamp=$(date +%s)
pkg_name="birthday-bot.zip"

func_pkg_s3key="${timestamp}-birthday-bot.zip"
func_pkg_s3bucket="aschittko-lambda"

echo "Uploading package to S3..."
aws s3 cp ./${pkg_name} s3://${func_pkg_s3bucket}/${func_pkg_s3key} --profile ${AWS_PROFILE_NAME}

if [[ "${TRAVIS}" != "true" ]]; then
    source .env
fi

# Run cloudformation
echo "Deploying CloudFormation template..."
aws cloudformation deploy\
    --template-file cfn.yaml\
    --profile ${AWS_PROFILE_NAME}\
    --stack-name "birthday-bot"\
    --capabilities "CAPABILITY_NAMED_IAM"\
    --parameter-overrides "FunctionPackageS3Key=${func_pkg_s3key}" "FunctionPackageS3Bucket=${func_pkg_s3bucket}" "DiscordChannelId=${DISCORD_CHANNEL_ID}" "DiscordGuildId=${DISCORD_GUILD_ID}" "DiscordBotToken=${DISCORD_BOT_TOKEN}" "IcalUrl=${ICAL_URL}" "Timestamp=${timestamp}"

echo "Complete!"
