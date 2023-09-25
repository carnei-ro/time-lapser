#!/usr/bin/env python
import argparse
import os
import sys

import requests

apiurl = 'https://api.telegram.org/bot{token}/{method}'.format


class EnvDefault(argparse.Action):
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def getUpdates(options):
    url = apiurl(token=options.token, method='getUpdates')
    response = requests.get(url)

    sys.stdout.write(response.content)
    sys.stdout.write('\n')

    response.raise_for_status()


def sendMessage(options):
    payload = {
        'chat_id': options.chat_id,
        'disable_notification': options.silent,
        'parse_mode': options.parse_mode,
    }
    files = {}
    method = 'sendMessage'

    if options.text:
        if options.text.startswith('gps:'):
            value = options.text.strip().split('gps:', 1).pop(1)
            try:
                latitude, longitude = value.split(',')
            except ValueError:
                pass
            else:
                method = 'sendLocation'
                payload['latitude'] = latitude
                payload['longitude'] = longitude
        elif options.text.startswith('url:'):
            endswith = options.text.endswith
            url = options.text.strip().split('url:', 1).pop(1)
            if any(map(endswith, ['.jpg', '.png', '.gif'])):
                method = 'sendPhoto'
                payload['photo'] = url
            elif any(map(endswith, ['.mp3'])):
                method = 'sendAudio'
                payload['audio'] = url
            elif any(map(endswith, ['.ogg'])):
                method = 'sendVoice'
                payload['voice'] = url
            elif any(map(endswith, ['.mp4'])):
                method = 'sendVideo'
                payload['video'] = url
            else:
                method = 'sendDocument'
                payload['document'] = url
        elif options.text.startswith('sticker:'):
            file_id = options.text.strip().split('sticker:', 1).pop(1)
            method = 'sendSticker'
            payload['sticker'] = file_id
        else:
            payload['text'] = options.text
    else:
        endswith = options.file.name.endswith
        del payload['parse_mode']
        if any(map(endswith, ['.jpg', '.png', '.gif'])):
            method = 'sendPhoto'
            files['photo'] = options.file
        elif any(map(endswith, ['.mp3'])):
            method = 'sendAudio'
            files['audio'] = options.file
        elif any(map(endswith, ['.ogg'])):
            method = 'sendVoice'
            files['voice'] = options.file
        elif any(map(endswith, ['.mp4'])):
            method = 'sendVideo'
            files['video'] = options.file
        else:
            method = 'sendDocument'
            files['document'] = options.file

    if options.verbose > 1:
        import logging

        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
    if options.verbose > 2:
        import httplib

        httplib.HTTPConnection.debuglevel = 1


    if options.aspect_ratio is not None:
        payload['width'] = options.aspect_ratio.split('x')[0]
        payload['height'] = options.aspect_ratio.split('x')[1]
    url = apiurl(token=options.token, method=method)
    response = requests.post(url, data=payload, files=files)

    sys.stdout.write(str(response.content))
    sys.stdout.write('\n')

    response.raise_for_status()


def main():
    description = """Use to send text messages. On success, the sent Message is returned."""

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('-i', '--chat-id',
                        help='Unique identifier for the target chat or username of the target channel (in the format @channelusername)',
                        required=False)
    action.add_argument('-l', '--list-updates',
                        help='Use this to receive incoming updates using long polling.', action='store_true',
                        default=False,
                        required=False, dest='list_updates')

    message = parser.add_mutually_exclusive_group(required=False)
    message.add_argument('-t', '--text', help='Text of the message to be sent')
    message.add_argument('-f', '--file', help='File to send (photo, audio, video, etc.)', dest='file',
                         type=argparse.FileType('rb'), required=False)

    parser.add_argument('-s', '--silent',
                        help="Sends the message silently. iOS users will not receive a notification, Android users will receive a notification with no sound.",
                        dest='silent', action='store_true', default=False)

    parser.add_argument('-p', '--parse-mode',
                        help="Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your bot's message.",
                        dest='parse_mode', choices=['markdown', 'html'], default='markdown')

    parser.add_argument('-v', '--verbose', help='Verbose mode', dest='verbose', action='count', default=0)
    parser.add_argument('--pre', '--preformatted', help='Format the message as a pre formatted string',
                        dest='preformatted', action='store_true', default=False)
    parser.add_argument('--token', action=EnvDefault, envvar='TELEGRAM_ACCESS_TOKEN', help='Your telegram access token',
                        dest='token')
    parser.add_argument('--video-aspect-ratio', action=EnvDefault, envvar='VIDEO_ASPECT_RATIO', help='Aspec ratio of video',
                        dest='aspect_ratio', default="1920x1080", required=False)
    options = parser.parse_args()

    if options.list_updates:
        getUpdates(options)
    else:
        sendMessage(options)


if __name__ == '__main__':
    main()
