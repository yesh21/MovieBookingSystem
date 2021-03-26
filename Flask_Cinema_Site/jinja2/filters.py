def format_datetime_generator(datetime_generator, format_str="%%a %d/%m/%y"):
    for val in datetime_generator:
        if val is None:
            yield ""
        yield val.strftime(format_str)
