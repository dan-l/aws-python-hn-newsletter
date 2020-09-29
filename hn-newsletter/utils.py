"""General util functions.
"""
import datetime


def timeAgo(then):
  """Return a formatted text of the difference between a given time and the current time.
  """
  now = int(datetime.datetime.utcnow().strftime('%s'))
  diff = int(abs(now - then))

  suffix = None
  if then < now:
    suffix = 'ago'
  else:
    suffix = 'from now'

  value = None
  unit = None

  if diff < 60:
    value = diff
    unit = 'second'
  elif diff < 60*60:
    value = diff // 60
    unit = 'minute'
  elif diff < 60*60*24:
    value = (diff // (60 * 60))
    unit = 'hour'
  elif diff < 60*60*24*7:
    value = (diff // (60 * 60 * 24))
    unit = 'day'
  elif diff < 60*60*24*30:
    value = (diff // (60 * 60 * 24 * 7))
    unit = 'week'
  elif diff < 60*60*24*365:
    value = (diff // (60 * 60 * 24 * 30))
    unit = 'month'
  else:
    value = (diff // (60 * 60 * 24 * 365))
    unit = 'year'

  if value != 1:
    unit += 's'

  return '%s %s %s' % (value, unit, suffix)
