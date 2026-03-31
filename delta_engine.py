def analyze_scenario(user_text, response):

    text = (user_text + " " + response).lower()

    move_keywords = [
        "run","leave","evacuate","exit","escape", "safe to exit"
    ]

    shelter_keywords = [
        "stay","hide","lock","secure","remain","lockdown","shelter"
    ]

    abort_keywords = [
        "avoid","stop","do not", "low chance of survival",
    ]

    # Count keyword occurrences
    move_score = sum(text.count(word) for word in move_keywords)
    shelter_score = sum(text.count(word) for word in shelter_keywords)
    abort_score = sum(text.count(word) for word in abort_keywords)

    # Base values
    proceed = 20 + (move_score * 25)
    wait = 20 + (shelter_score * 25)
    abort = 10 + (abort_score * 25)

    # Prevent everything being zero
    if move_score == shelter_score == abort_score == 0:
        proceed = 34
        wait = 33
        abort = 33

    # Normalize
    total = proceed + wait + abort

    proceed = int((proceed / total) * 100)
    wait = int((wait / total) * 100)
    abort = int((abort / total) * 100)

    return {
        "Proceed": proceed,
        "Wait": wait,
        "Abort": abort
    }