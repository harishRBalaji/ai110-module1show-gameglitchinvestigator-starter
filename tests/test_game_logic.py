from logic_utils import (
    check_guess,
    parse_guess,
    update_score,
    get_range_for_difficulty,
    get_attempt_limit_for_difficulty,
)


# --- check_guess ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_check_guess_hint_too_high():
    # Hint should tell player to go lower when guess is too high
    _, message = check_guess(80, 50)
    assert "LOWER" in message

def test_check_guess_hint_too_low():
    # Hint should tell player to go higher when guess is too low
    _, message = check_guess(20, 50)
    assert "HIGHER" in message


# --- parse_guess ---

def test_parse_guess_valid():
    ok, value, err = parse_guess("10", 1, 20)
    assert ok is True
    assert value == 10
    assert err is None

def test_parse_guess_empty():
    ok, value, err = parse_guess("", 1, 20)
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_none():
    ok, value, _ = parse_guess(None, 1, 20)
    assert ok is False
    assert value is None

def test_parse_guess_non_numeric():
    ok, value, _ = parse_guess("abc", 1, 20)
    assert ok is False
    assert value is None

def test_parse_guess_decimal_rejected():
    # Decimals should be rejected, not silently truncated
    ok, value, _ = parse_guess("3.9", 1, 20)
    assert ok is False
    assert value is None

def test_parse_guess_below_range():
    ok, value, _ = parse_guess("-1", 1, 20)
    assert ok is False
    assert value is None

def test_parse_guess_above_range():
    ok, value, _ = parse_guess("21", 1, 20)
    assert ok is False
    assert value is None

def test_parse_guess_boundary_low():
    # Boundary value: exactly low should be valid
    ok, value, err = parse_guess("1", 1, 20)
    assert ok is True
    assert value == 1

def test_parse_guess_boundary_high():
    # Boundary value: exactly high should be valid
    ok, value, err = parse_guess("20", 1, 20)
    assert ok is True
    assert value == 20


# --- update_score ---

def test_update_score_win_first_attempt():
    # Win on attempt 1: 100 - 10*1 = 90 points
    score = update_score(0, "Win", 1)
    assert score == 90

def test_update_score_win_minimum_points():
    # Win very late: score should not drop below 10 points added
    score = update_score(0, "Win", 100)
    assert score == 10

def test_update_score_too_high_no_change():
    # Wrong guesses do not deduct from score
    score = update_score(50, "Too High", 1)
    assert score == 50

def test_update_score_too_low_no_change():
    # Wrong guesses do not deduct from score
    score = update_score(50, "Too Low", 1)
    assert score == 50

def test_update_score_unknown_outcome():
    # Unknown outcome should leave score unchanged
    score = update_score(50, "Unknown", 1)
    assert score == 50


# --- get_range_for_difficulty ---

def test_range_easy():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_range_normal():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50

def test_range_hard():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100

def test_range_unknown_defaults():
    # Unknown difficulty should return a safe default
    low, high = get_range_for_difficulty("Extreme")
    assert low == 1
    assert high == 100


# --- get_attempt_limit_for_difficulty ---

def test_attempt_limit_easy():
    assert get_attempt_limit_for_difficulty("Easy") == 6

def test_attempt_limit_normal():
    assert get_attempt_limit_for_difficulty("Normal") == 8

def test_attempt_limit_hard():
    assert get_attempt_limit_for_difficulty("Hard") == 10

def test_attempt_limit_unknown_defaults():
    # Unknown difficulty should return a safe default
    assert get_attempt_limit_for_difficulty("Extreme") == 8
