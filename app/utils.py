def format_duration(seconds: int) -> str:
    if not seconds:
        return "0h00m"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h{minutes:02d}m"