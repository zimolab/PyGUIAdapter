from pyguiadapter.adapter import GUIAdapter, uoutput


def output_log_msg(
    info_msg: str = "info message",
    debug_msg: str = "debug message",
    warning_msg: str = "warning message",
    critical_msg: str = "critical message",
    fatal_msg: str = "fatal message",
):
    uoutput.info(info_msg)
    uoutput.debug(debug_msg)
    uoutput.warning(warning_msg)
    uoutput.critical(critical_msg)
    uoutput.fatal(fatal_msg)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(output_log_msg)
    adapter.run()
