"""Util file housing email related functions.
"""
import logging
import os
import boto3

SENDER = os.environ.get('AWS_SES_SENDER')
AWS_REGION = os.environ.get('AWS_REGION')
# The character encoding for the email.
CHARSET = "UTF-8"
BUCKET_NAME = os.environ.get('BUCKET_NAME')


def get_recipients():
  """Fetch recipients to send email to which is a text file on s3.
  """
  if not BUCKET_NAME:
    logging.warning('No bucket')
    return []

  try:
    # get the emails from s3
    s3 = boto3.resource('s3')
    obj = s3.Object(BUCKET_NAME, 'emails.txt')
    text = obj.get()['Body'].read().decode('utf-8')
    recipients = text.split('\n')
    logging.info('Recipients %s', recipients)
    return recipients
  except Exception as err:
    logging.error('Cannot get recipients: %s', err)

def send(subject, recipients, data):
  """Send email using AWS SES.
  """
  if not SENDER:
    logging.warning('No sender')
    return

  if not recipients:
    logging.warning('No recipients')
    return

  if not data:
    logging.warning('No data')
    return

  try:
    # Send email with SES
    client = boto3.client('ses', region_name=AWS_REGION)
    response = client.send_email(
      Source = SENDER,
      Destination = {
        'ToAddresses': recipients
      },
      Message = {
        'Body': {
          'Html': {
            'Charset': CHARSET,
            'Data': data,
          },
          'Text': {
            'Charset': CHARSET,
            'Data': 'HN newsletter in HTML'
          },
        },
        'Subject': {
          'Charset': CHARSET,
          'Data': subject,
        }
      },
    )
  except Exception as err:
    logging.error('Cannot send email: %s', err)
  else:
    logging.info('Email sent! Message ID: %s', response.get('MessageId'))
