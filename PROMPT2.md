# Rule

Great! Let's move next phase.

- There are three pokemons for each players:

  - Snorlax (Default Active) / HP: 523
    - Return
    - Earthquake
  - Zapdos / HP: 383
    - Thunderbolt
    - Hidden Power Ice
  - Nidoking / HP: 365
    - Ice Beam
    - Earthquake

- Damages:

| Attacker | Defender | Move             | Damage |
| -------- | -------- | ---------------- | ------ |
| Snorlax  | Snorlax  | Return           | 166    |
| Snorlax  | Snorlax  | Earthquake       | 109    |
| Snorlax  | Zapdos   | Return           | 142    |
| Snorlax  | Zapdos   | Earthquake       | 0      |
| Snorlax  | Nidoking | Return           | 150    |
| Snorlax  | Nidoking | Earthquake       | 198    |
| Zapdos   | Snorlax  | Thunderbolt      | 123    |
| Zapdos   | Snorlax  | Hidden Power Ice | 61     |
| Zapdos   | Zapdos   | Thunderbolt      | 141    |
| Zapdos   | Zapdos   | Hidden Power Ice | 140    |
| Zapdos   | Nidoking | Thunderbolt      | 0      |
| Zapdos   | Nidoking | Hidden Power Ice | 155    |
| Nidoking | Snorlax  | Earthquake       | 145    |
| Nidoking | Snorlax  | Ice Beam         | 63     |
| Nidoking | Zapdos   | Earthquake       | 0      |
| Nidoking | Zapdos   | Ice Beam         | 146    |
| Nidoking | Nidoking | Earthquake       | 262    |
| Nidoking | Nidoking | Ice Beam         | 162    |

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

- Consider Nidoking
- Now players have more than 2 pokemons, the action should contain "which pokemons to switch"

# Recommended tech stack

- uv
- pytest
- [pettingzoo](https://pettingzoo.farama.org/tutorials/custom_environment/2-environment-logic/)
