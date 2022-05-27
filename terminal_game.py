from snake import Game, SnakeDirection


a = Game(10, 10)
print(a.board)
while(True):
    key_input = input()
    if key_input == 'w':
        a.next_tick(SnakeDirection.UP)
        print(a.board)
        continue
    if key_input == 'd':
        a.next_tick(SnakeDirection.RIGHT)
        print(a.board)
        continue
    if key_input == 's':
        a.next_tick(SnakeDirection.DOWN)
        print(a.board)
        continue
    if key_input == 'a':
        a.next_tick(SnakeDirection.LEFT)
        print(a.board)
        continue
    break
