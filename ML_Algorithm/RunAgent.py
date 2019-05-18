from Agent import Agent
from game.Game import Game

import csv

def RunAgent(game_count = 50):
    agent = Agent()

    with open('SnakeLogs.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Attempt', 'Length','iterations_count'])

    main_game = Game()
    for i in range(game_count):
        main_game.rerun()
        next_state = main_game.send_state()
        reward = 0 
        while main_game.running:
            state = next_state
            (next_state, reward)  = main_game.run(agent.get_action(state, reward))
            if not main_game.running:
                with open('SnakeLogs.csv', 'a', newline='') as csvfile:
                    spamwriter = csv.writer(csvfile)
                    spamwriter.writerow([str(i), str(main_game.get_snake_size()),str(main_game.iterations_count)])
                agent.get_action(next_state, reward, game_over = True)

RunAgent(game_count=1)