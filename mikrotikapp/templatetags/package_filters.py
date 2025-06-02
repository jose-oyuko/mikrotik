from django import template

register = template.Library()

@register.filter
def format_period(minutes):
    minutes = int(minutes)
    if minutes >= 1440:  # 24 hours
        days = minutes // 1440
        remaining_minutes = minutes % 1440
        if remaining_minutes >= 60:
            hours = remaining_minutes // 60
            remaining_minutes = remaining_minutes % 60
            if remaining_minutes > 0:
                return f"{days} Day{'s' if days != 1 else ''} {hours} Hour{'s' if hours != 1 else ''} {remaining_minutes} Minute{'s' if remaining_minutes != 1 else ''}"
            return f"{days} Day{'s' if days != 1 else ''} {hours} Hour{'s' if hours != 1 else ''}"
        elif remaining_minutes > 0:
            return f"{days} Day{'s' if days != 1 else ''} {remaining_minutes} Minute{'s' if remaining_minutes != 1 else ''}"
        return f"{days} Day{'s' if days != 1 else ''}"
    elif minutes >= 60:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if remaining_minutes > 0:
            return f"{hours} Hour{'s' if hours != 1 else ''} {remaining_minutes} Minute{'s' if remaining_minutes != 1 else ''}"
        return f"{hours} Hour{'s' if hours != 1 else ''}"
    else:
        return f"{minutes} Minute{'s' if minutes != 1 else ''}" 