# timelapser

<!-- markdownlint-disable line-length no-space-in-code -->

Cronjob to download pictures from a Storj bucket, convert them to a video, upload it to a Storj bucket, and send it to telegram (optional).

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| buckets.accessKeyId | string | `""` | Access Key ID to populate the env var AWS_ACCESS_KEY_ID |
| buckets.photosBucketName | string | `"photos"` | Name of the bucket that contains the snapshots |
| buckets.s3Endpoint | string | `"https://gateway.storjshare.io"` | Endpoint of the bucket, useful when bucket is not at AWS |
| buckets.secretAccessKey | string | `""` | Secret Access Key to populate the env var AWS_SECRET_ACCESS_KEY |
| buckets.videosBucketName | string | `"videos"` | Name of the bucket to store the videos |
| cronjob.concurrencyPolicy | string | `"Forbid"` | One of `Allow`, `Forbid`, `Replace` - [read more](https://kubernetes.io/docs/tasks/job/automated-tasks-with-cron-jobs/#concurrency-policy) |
| cronjob.failedJobsHistoryLimit | int | `3` | Number of failed ended pods to keep |
| cronjob.schedule | string | `"@daily"` | A cron format string (such as `0 * * * *` or `@hourly`) to schedule the job creation and execution |
| cronjob.successfulJobsHistoryLimit | int | `2` | Number of successefully ended pods to keep |
| cronjob.suspend | bool | `false` | Toggle to control the scheduling of the jobs |
| env | list | `[]` | Environment variables for the container |
| fullnameOverride | string | `""` | Overrides the name |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"ghcr.io/carnei-ro/time-lapser"` | Image name |
| image.tag | string | `"sha-637dbdd"` | Image tag |
| nameOverride | string | `""` | Overrides the release name |
| podAnnotations | object | `{}` | Map of additional annotations for the pod |
| podLabels | object | `{}` | Map of additional labels for the pod |
| process.imagesFromDay | string | `"yesterday"` | The relative day to process the images |
| process.imagesResolution | string | `"2592x1520"` | The resolution of the images |
| process.sendToBucket | bool | `true` | Toggle to send the video to the bucket |
| resources.limits.cpu | string | `"400m"` | How much CPU a container never goes above |
| resources.limits.memory | string | `"2Gi"` | How much memory a container never goes above |
| resources.requests.cpu | string | `"50m"` | How much CPU a container is guaranteed to get |
| resources.requests.memory | string | `"128Mi"` | How much memory a container is guaranteed to get |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.name | string | `"timelapser"` | The name of the service account to use. |
| telegram.botToken | string | `""` | Telegram bot token |
| telegram.chatId | string | `""` | Telegram chat ID |
| telegram.enabled | bool | `false` | Toggle to enable sending the video to telegram |
