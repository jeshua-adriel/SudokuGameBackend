"""
Score formula (kept simple and transparent so it's easy to tune):

    score = base_score(difficulty)
            - (time_completed_seconds * TIME_PENALTY_PER_SECOND)
            - (wrong_inputs * WRONG_INPUT_PENALTY)

    wrong_inputs = total_inputs - correct_inputs

Floored at 0 -- a messy, slow game never goes negative, it just scores low.
Harder difficulties have a higher base score so a clean "hard" game
outranks a clean "easy" game even though it took longer.
"""

BASE_SCORE = {
    "easy": 1000,
    "medium": 2000,
    "hard": 3000,
}

TIME_PENALTY_PER_SECOND = 0.5
MAX_TIME_PENALTY_FRACTION = 0.3

def compute_score(difficulty, time_completed_seconds, correct_inputs, total_inputs):
    base = BASE_SCORE.get(difficulty, BASE_SCORE["medium"])
    accuracy = (correct_inputs / total_inputs) if total_inputs > 0 else 1.0

    accuracy_score = base * accuracy

    raw_time_penalty = time_completed_seconds * TIME_PENALTY_PER_SECOND
    time_penalty = min(raw_time_penalty, accuracy_score * MAX_TIME_PENALTY_FRACTION)

    score = accuracy_score - time_penalty
    return max(0, round(score))


