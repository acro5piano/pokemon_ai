from pokemon_ai.simulator.pokedex import Jolteon, Rhydon, Starmie


def test_real_hp():
    assert Jolteon().actual_hp == 333
    assert Starmie().actual_hp == 323
    assert Rhydon().actual_hp == 413
