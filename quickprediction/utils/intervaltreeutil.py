from intervaltree import IntervalTree

def findLatestInterval(intervals):
  """
    Find the latest interval.
  """
  latest = intervals[0]
  for interval in intervals:
    if interval.begin > latest.begin:
      latest = interval
  return latest

def orIntervals(intervalListA, intervalListB):
  return list(set(intervalListA) | set(intervalListB))

def conflictPath(interval, intervalTree):
  """
    @param interval The interval to find conflicts with.
    @param intervalTree The intervalTree that contains all intervals
    @param exclude Any intervals to exclude from conflict detection.
    Finds the longest number of intervals that are all overlapping (conflicting).
      For example:
        if A and B conflict and B and C conflict and A is the
        interval we're looking for conflicts with, the returned
        intervals will be A, B, C.
      Another example:
        if D and E conflict and F and G conflict, and we're looking
        for all conflicts with D, only D and E will be returned as
        F and G are not overlapping with either D and E.
  """
  intervals = list(intervalTree.search(interval))
  # if only one interval, check if its the one we're
  # trying to find conflicts with.
  if len(intervals) == 1 and intervals[0] == interval:
    return []
  # now find the latest of all the intervals and get all conflicts
  # with and keep going until there are no more conflicts.
  latestInterval = findLatestInterval(intervals)
  # remove all the conflicts, we dont need to check them again.
  intervalTree.remove_overlap(interval)
  # put the latest conflict back into the tree and find its conflicts
  intervalTree.add(latestInterval)
  # now go find all conflicts with the latest interval until there are none.
  return orIntervals(intervals, conflictPath(latestInterval, intervalTree))

def intervalConflictAlreadyDetected(interval, conflicts):
  """
    Checks to see if interval was already detected to conflict.
  """
  for conflict in conflicts:
    for ival in conflict:
      if ival == interval:
        return True
  return False


def findConflicts(intervalTree, begin=None, end=None):
  if not begin and not end:
    begin = intervalTree.begin()
    end = intervalTree.end()
  conflicts = [] # intervals that conflict
  nonConflicts = [] # intervals that do no conflict.
  intervals = sorted(intervalTree[begin:end])
  tempTree = IntervalTree(intervals) # new tree with only the intervals between the point.
  for interval in intervals:
    # check first if this interval was already detected to conflict
    if intervalConflictAlreadyDetected(interval, conflicts):
      continue
    conflictIntervals = conflictPath(interval, tempTree)
    if len(conflictIntervals) > 0: # there was a conflict.
        conflicts.append(conflictIntervals)
    else:
      nonConflicts.append(interval)
  return conflicts, nonConflicts
