#!/bin/sh

set -e -o pipefail

export PHOTOS_BUCKET_NAME="${PHOTOS_BUCKET_NAME:-photos}"
export VIDEOS_BUCKET_NAME="${VIDEOS_BUCKET_NAME:-videos}"
export AWS_ENDPOINT_URL="${AWS_ENDPOINT_URL:-https://gateway.storjshare.io}"
export RESOLUTION="${RESOLUTION:-2592x1520}"
export DAY_OF_THE_IMAGES="${DAY_OF_THE_IMAGES:-yesterday}"

export TELEGRAM_SEND_VIDEO_ENABLED="${TELEGRAM_SEND_VIDEO_ENABLED:-false}"
export TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"
export TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"

if [ $TELEGRAM_SEND_VIDEO_ENABLED == "true" ]; then
  if [ -z $TELEGRAM_CHAT_ID ]; then
    echo "TELEGRAM_SEND_VIDEO_ENABLED is true, but TELEGRAM_CHAT_ID is not set"
    exit 1
  fi
  if [ -z $TELEGRAM_BOT_TOKEN ]; then
    echo "TELEGRAM_SEND_VIDEO_ENABLED is true, but TELEGRAM_BOT_TOKEN is not set"
    exit 1
  fi
fi

if [ -z $AWS_ACCESS_KEY_ID ]; then
  echo "AWS_ACCESS_KEY_ID is not set"
  exit 1
fi
if [ -z $AWS_SECRET_ACCESS_KEY ]; then
  echo "AWS_SECRET_ACCESS_KEY is not set"
  exit 1
fi

read -r YEAR MONTH DAY < <(date -d "${DAY_OF_THE_IMAGES}" '+%Y %m %d')

HOSTNAMES=$(aws s3 ls s3://${PHOTOS_BUCKET_NAME}/ | grep PRE\ | tr -d "/" | awk '{print $2}')

for HOSTNAME in $HOSTNAMES; do
  echo $HOSTNAME
  mkdir -p $HOSTNAME/${YEAR}${MONTH}${DAY}
  cd "$HOSTNAME/${YEAR}${MONTH}${DAY}"
  aws s3 sync "s3://${PHOTOS_BUCKET_NAME}/$HOSTNAME/${YEAR}${MONTH}${DAY}/" .
  ffmpeg -framerate 30 -pattern_type glob -i "*.jpg" -s:v ${RESOLUTION} -c:v libx264 -crf 17 -pix_fmt yuv420p $HOSTNAME.mp4
  aws s3 cp $HOSTNAME.mp4 s3://${VIDEOS_BUCKET_NAME}/${YEAR}/${MONTH}/${DAY}/$HOSTNAME.mp4
  if [ $TELEGRAM_SEND_VIDEO_ENABLED == "true" ]; then
    python /telegram.py -i "${TELEGRAM_CHAT_ID}" --token "${TELEGRAM_BOT_TOKEN}" -t "Video from $HOSTNAME on ${YEAR}-${MONTH}-${DAY}"
    python /telegram.py -i "${TELEGRAM_CHAT_ID}" --token "${TELEGRAM_BOT_TOKEN}" -f $HOSTNAME.mp4
  fi
  cd -
  rm -fr $HOSTNAME/${YEAR}${MONTH}${DAY}
done
