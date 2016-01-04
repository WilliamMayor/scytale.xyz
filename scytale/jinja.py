def ordinal(n):
    return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def display(text):
    return text.replace(" ", "_")


def init_app(app):
    app.jinja_env.filters["ordinal"] = ordinal
    app.jinja_env.filters["display"] = display
