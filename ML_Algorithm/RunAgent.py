from Agent import Agent
from game.Game import Game

def RunAgent():
    agent = Agent()
    game_count = 50
    main_game = Game()
    for i in range(game_count):
        main_game.rerun()
        next_state = main_game.send_state()
        reward = 0 
        while main_game.running:
            state = next_state
            (next_state, reward)  = main_game.run(agent.get_action(state, reward))
            if not main_game.running:
                agent.get_action(next_state, reward, game_over = True)

RunAgent()