from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import Logger, LoggerConfig

logger = Logger(
    config=LoggerConfig(
        info_color="green",
        debug_color="blue",
        warning_color="yellow",
        critical_color="red",
        fatal_color="magenta",
    )
)


def output_log_msg(
    info_msg: str = "info message",
    debug_msg: str = "debug message",
    warning_msg: str = "warning message",
    critical_msg: str = "critical message",
    fatal_msg: str = "fatal message",
):

    logger.info(info_msg)
    logger.debug(debug_msg)
    logger.warning(warning_msg)
    logger.critical(critical_msg)
    logger.fatal(fatal_msg)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(output_log_msg)
    adapter.run()
