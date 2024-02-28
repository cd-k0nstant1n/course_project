from django import template

register = template.Library()

@register.filter(name='last_n_words')
def last_n_words(value, arg):
    """
    Returns the last 'arg' words of the string 'value'.
    """
    try:
        # Ensure the argument is an integer
        num_words = int(arg)
    except ValueError:
        # If not, return the original value
        return value

    words = value.split()
    # Return the last 'num_words' words joined by space
    return ' '.join(words[-num_words:])
