"""Fetches stories from HN using firebase API and creates a HTML newsletter from it.
"""
import asyncio
import logging
import utils
from aiohttp import ClientSession

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.aiohttp.client import aws_xray_trace_config

HN_BEST_STORIES = 'https://hacker-news.firebaseio.com/v0/beststories.json'
HN_STORY        = 'https://hacker-news.firebaseio.com/v0/item/%s.json'
HN_POST         = 'https://news.ycombinator.com/item?id=%s'
NUM_STORIES = 30

@xray_recorder.capture_async('create_newsletter')
async def create_newsletter():
  """Create a HTML newsletter from the fetched stories.
  """
  stories = await _fetch_stories()

  if not stories:
    return logging.warning('No stories')

  return _make_stories_html(stories)

async def _fetch_stories():
  trace_config = aws_xray_trace_config()
  # Use a single session for connection pooling
  async with ClientSession(trace_configs=[trace_config]) as session:
    story_ids = await _fetch_story_ids(session)

    if not story_ids:
      return []

    # fetch stories in parallel with async tasks
    tasks = [_fetch_story(session, story_ids[i]) for i in range(NUM_STORIES)]
    return await asyncio.gather(*tasks)

async def _fetch_story_ids(session):
  try:
    r = await session.request('GET', HN_BEST_STORIES)
    r.raise_for_status()
    return await r.json()
  except Exception as err:
    logging.error('Fetch story id error: %s', err)

async def _fetch_story(session, story_id):
  try:
    r = await session.request('GET', HN_STORY % story_id)
    r.raise_for_status()
    story = await r.json()
    story['comment_url'] = HN_POST % story_id
    return story
  except Exception as err:
    logging.error('Fetch story error: %s', err)

#pylint: disable=line-too-long
def _make_stories_html(stories):
  html_string = ('<header>'
  '<div style="font-family: Verdana; font-size: 13.33px; color: black; text-decoration: none; background-color: #ff6600">'
  '<a href="https://news.ycombinator.com/news" style="color: black"><b>Hacker Newsletter</b></a>'
  '</div>'
  '</header>'
  '<ul style="background-color: #f6f6ef; list-style:none">'
  )

  for story in stories:
    url = story.get('url')
    title = story.get('title')
    score = story.get('score')
    story_type = story.get('type')
    time = utils.timeAgo(story.get('time'))
    comment_url = story.get('comment_url')
    descendants = story.get('descendants')

    html_string += ('<li style="padding: 15px">'
    f'<span><a href={url} style="color: black; text-decoration: none">{title}</a></span>'
    '<div><small style="color: #666d74">'
    f'<span style="padding-right: 10px">{score} points </span>'
    f'<span style="padding-right: 10px">{story_type}</span>'
    f'<span style="padding-right: 10px">{time}</span>'
    f'<a href="{comment_url}" style="color: #666d74; text-decoration: none">'
    f'| {descendants} Comments'
    '</a>'
    '</small></div>'
    '</li>'
    )

  html_string += '</ul>'

  logging.info('Newsletter:')
  logging.info(html_string)
  return html_string
