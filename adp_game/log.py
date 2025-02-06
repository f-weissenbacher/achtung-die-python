import logging
import coloredlogs

default_log_format = "%(relativeCreated)d %(levelname)s [%(module)s.%(funcName)s:%(lineno)d] - %(message)s"

# Configure logging style
# logging.basicConfig(format="%(levelname)s:[%(filename)s:%(lineno)s - %(funcName)s()] %(message)s", level=logging.DEBUG)
def setup_colored_logs(level, fmt=None, do_basic_setup=False):
    log_field_styles = dict(
        asctime=dict(color='green'),
        module=dict(color='magenta'),
        levelname=dict(color='yellow', bold=True),
        funcName=dict(color='blue'),
    )
    log_level_styles = dict(
        spam=dict(color='green', faint=True),
        debug=dict(color='green', faint=True),
        verbose=dict(color='blue'),
        info=dict(color='white', faint=False, bright=False),
        notice=dict(color='magenta'),
        warning=dict(color='yellow', bold=True),
        success=dict(color='green', bold=True),
        error=dict(color='red'),
        critical=dict(color='red', bold=True),
    )

    if isinstance(level, str):
        level = level.lower()
        if level == "debug":
            level = logging.DEBUG
        elif level == "info":
            level = logging.INFO
        elif level == "warning":
            level = logging.WARNING
        elif level == "error":
            level = logging.ERROR
        else:
            raise ValueError

    if fmt is None:
        fmt = default_log_format

    if do_basic_setup:
        logging.basicConfig(level=level, format=fmt)

    coloredlogs.install(level=level, fmt=fmt, field_styles=log_field_styles, level_styles=log_level_styles)
