# Time-lapser

Download snapshots from a Storj bucket, stitch them together in a video, and upload the result to another bucket.

## Configuration

All the configurations are set through environment variables.

| Variable | Description | Default |
| -------- | ----------- | ------- |
| `AWS_ACCESS_KEY_ID` | AWS access key ID | |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key | |
| `AWS_ENDPOINT_URL` | AWS compatible endpoint URL | `https://gateway.storjshare.io` |
| `PHOTOS_BUCKET_NAME` | Name of the bucket where the photos are stored | `photos` |
| `VIDEOS_BUCKET_NAME` | Name of the bucket where the videos will be stored | `videos` |
| `RESOLUTION` | Resolution of the photos | `2592x1520` |
| `DAY_OF_THE_IMAGES` | Day of the images to download | `yesterday` (for the same day, use `today`) |
| `TELEGRAM_SEND_VIDEO_ENABLED` | Whether to send the video to Telegram or not | `false` |
| `TELEGRAM_CHAT_ID` | Telegram chat ID | |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | |
