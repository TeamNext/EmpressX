PENDING = 'PENDING'
STARTED = 'STARTED'
SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'

ALL_STATES = frozenset([
    PENDING,
    STARTED,
    SUCCESS,
    FAILURE,
])

ARCHIVED_STATES = frozenset([
    SUCCESS,
    FAILURE,
])

_TRANSITION = {
    PENDING: frozenset([STARTED, FAILURE]),
    STARTED: frozenset([SUCCESS, FAILURE]),
    SUCCESS: frozenset([]),
    FAILURE: frozenset([]),
}

def can_transit(from_state, to_state):
    """Test if :param:`from_state` can transit to :param:`to_state`::

        >>> can_transit(PENDING, STARTED)
        True

        >>> can_transit(PENDING, SUCCESS)
        False
    """
    if from_state in _TRANSITION:
        if to_state in _TRANSITION[from_state]:
            return True
    return False