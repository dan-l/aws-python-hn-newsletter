"""AWS lambda function that creates HN newsletter and send them via AWS SES.
"""
import asyncio
import logging

import email_client
import hn

# Start logging
logging.getLogger().setLevel(logging.INFO)

#pylint: disable=unused-argument
def run_lambda(event, context):
  """Entry point lambda function.
  """
  asyncio.run(main())

async def main():
  """Main function.
  """
  newsletter = await hn.create_newsletter()
  recipients = email_client.get_recipients()
  subject = 'HN Newsletter'
  email_client.send(subject, recipients, newsletter)

if __name__ == '__main__':
  asyncio.run(main())
