from pokemon_ai.simulator.pokedex import calculate_actual_hp


def test_calculate_actual_hp():
    assert calculate_actual_hp(65) == 333
    assert calculate_actual_hp(60) == 323
    assert calculate_actual_hp(105) == 413
