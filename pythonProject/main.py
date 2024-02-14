# CRUD (Create Read Update Delete) operations

# Database representation
team: list[dict] = [
    {'name': 'John', 'age': 20, 'number': 1},
    {'name': 'Mark', 'age': 33, 'number': 3},
    {'name': 'Cevin', 'age': 31, 'number': 12},
    {'name': 'Sofia', 'age': 22, 'number': 5},
    {'name': 'Kristopher', 'age': 25, 'number': 6},
    {'name': 'Denny', 'age': 24, 'number': 10},
]


def player_validate(name: str, age: int, number: int) -> bool:
    index = [pl['number'] for pl in team].index(number)
    return index < 0 and {'name': name, 'age': age} not in [{'name': plr['name'], 'age': plr['age']} for plr in team]
# Application source code


def repr_players(players: list[dict]):
    for player in players:
        print(
            f"\t[Player {player['number']}: {player['name']}, {player['age']}]"
        )


def player_add(name: str, age: int, number: int) -> dict:
    player: dict = {'name': name, 'age': age, 'number': number}

    if player not in team and number not in [pl['number']for pl in team]:

        team.append(player)
        return player
    print("Player is already exist!")
    return player


def player_delete(number: int) -> None:
    index = [pl['number'] for pl in team].index(number)
    if index >= 0:
        print(f'Player{number} deleted!')
        team.pop(index)
    else:
        print(f'Player {number} not exist!')





def player_update(name: str, age: int, number: int):

    index = [pl['number'] for pl in team].index(number)
    if index >= 0:
        team[index] = {'name': name, 'age': int(age), 'number': int(number)}
        print(f'player: {team[index]["name"]} updated!')
    else:
        print("Player not exist!")


if __name__ == "__main__":

    operations = ('add', 'del', 'repr', 'exit', 'update')

    while True:
        operation = input("Please input operation: ")
        if operation not in operations:
            print("Please input a valid operation")

        elif operation == 'repr':
            repr_players(team)

        elif operation == 'add':
            name, age, number = input("Enter name, age, number: ").split(',')
            player_add(name, int(age), int(number))

        elif operation == 'update':
            name, age, number = input("Enter name, age, number: ").split(',')
            player_update(name, int(age), int(number))

        elif operation == 'exit':
            break

        elif operation == 'del':
            number = int(input("Enter number: "))
            player_delete(int(number))

        else:
            print('Operation not implemented!\n')
