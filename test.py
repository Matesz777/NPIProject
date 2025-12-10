from ruletkaDocker import one_game_sim

def test_simulation_range():
    result = one_game_sim(2)
    assert result is None or 1 <= result <= 6
