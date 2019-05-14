from Agent import Agent
from game.Game import Game

def RunAgent():
    agent = Agent()
    game_count = 50
    main_game = Game()
    for i in range(game_count):
        main_game.rerun()
        state = main_game.send_state()
        state.append(0)
        while main_game.running:
            old_state = state
            state = main_game.run(agent.get_action(old_state))

RunAgent()