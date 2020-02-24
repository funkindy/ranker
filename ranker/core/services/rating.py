MAX_NONZERO_DIFFERENCE = 100


def calculate_new_rating(winner_rating: float, loser_rating: float, coef: float) -> tuple:
    delta = ((MAX_NONZERO_DIFFERENCE - (winner_rating - loser_rating)) / 10) * coef

    if winner_rating - loser_rating > MAX_NONZERO_DIFFERENCE:
        delta = 0
    else:
        winner_rating = winner_rating + delta
        loser_rating = max(1, loser_rating - delta)

    return winner_rating, loser_rating, delta
