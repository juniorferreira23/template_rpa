def seconds_formatting(duration: int):
    hours = duration // 3600
    minutes = duration % 3600 // 60
    seconds = duration % 60
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
