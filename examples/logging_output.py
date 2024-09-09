from pyguiadapter.adapter import GUIAdapter, ulogging


def output_log_msg(
    info_msg: str = "info message",
    debug_msg: str = "debug message",
    warning_msg: str = "warning message",
    critical_msg: str = "critical message",
    fatal_msg: str = "fatal message",
):
    ulogging.info(info_msg)
    ulogging.debug(debug_msg)
    ulogging.warning(warning_msg)
    ulogging.critical(critical_msg)
    ulogging.fatal(fatal_msg)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(output_log_msg)
    adapter.run()
