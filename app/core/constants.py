class CoreConstants:
    """CoreConstants"""

    """ Field status ->
    status == 0 -> zero field
    status == 1 -> base field
    status == 2 -> wip field
    status == 3 -> field solved
    """
    STATUS_ZERO = 0
    STATUS_BASE = 1
    STATUS_WIP = 2
    STATUS_SOLVED = 3
    """<- Field status"""

    """ SENTRY ->"""
    SENTRY_MSG_DEBUG = "debug"
    SENTRY_MSG_INFO = "info"
    SENTRY_MSG_WARNING = "warning"
    SENTRY_MSG_ERROR = "error"
    SENTRY_MSG_EXCEPTION = "exception"

    SENTRY_TAG_GENERAL = "General"
    SENTRY_TAG_PROCESSING = "Processing"
    SENTRY_TAG_REQUEST = "Request"
    SENTRY_TAG_DB_MODEL = "DB model"
    SENTRY_TAG_ML = "ML"
    """ <- SENTRY"""
