Create reinforcement learing program for Pokemon battle.

# Rule

- GSC OU (gen 2) rule is applied.

For phase 1, let's solve over-simplified environment:

- There are two pokemons for each players:
  - Snorlax (Default Active) / HP: 523
    - Return
    - Earthquake
  - Zapdos / HP: 523
    - Thunderbolt
    - Hidden Power Ice
- Damages are fixed value:

| Attacker | Defender | Move             | Damage |
| -------- | -------- | ---------------- | ------ |
| Snorlax  | Snorlax  | Return           | 166    |
| Snorlax  | Snorlax  | Earthquake       | 109    |
| Snorlax  | Zapdos   | Return           | 142    |
| Snorlax  | Zapdos   | Earthquake       | 0      |
| Zapdos   | Snorlax  | Thunderbolt      | 123    |
| Zapdos   | Snorlax  | Hidden Power Ice | 61     |
| Zapdos   | Zapdos   | Thunderbolt      | 141    |
| Zapdos   | Zapdos   | Hidden Power Ice | 140    |

- Players can do either:
  - use move 1
  - use move 2
  - change pokemon

Do not consider:

- Critical hit
- STAB
- Team building
- PP
- Damage random value
- Any other complex things

# What to do

For phase 1, train with simple Deep Q Network.

# Recommended tech stack

- uv
- pytest
- [pettingzoo](https://pettingzoo.farama.org/tutorials/custom_environment/2-environment-logic/)
