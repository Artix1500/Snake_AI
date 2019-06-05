from Agent import Agent
from game.Game import Game

import csv

def RunAgent(game_count = 50, visible= True, waitForEyes= False, gamma=0.4, layer3=False, dropout=False, dropoutrate=0.5, path="model.h5", nepochs=2,eps=1):
    agent = Agent(gamma=gamma,ifDropout=dropout, dropoutrate=dropoutrate,path_saved_weights=path, layer3=layer3, nepochs=nepochs, epsilon=eps)

    with open('SnakeLogs.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Attempt', 'Length','iterations_count'])

    main_game = Game(visible, waitForEyes)
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
ngame=30000

ngame2=10
'''
RunAgent(game_count=ngame, visible=False, waitForEyes=False,gamma=0.4, layer3=False, dropout=False, dropoutrate=0.5,nepochs=2, path="model1.h5")

RunAgent(game_count=ngame, visible=False, waitForEyes=False,gamma=0.2, layer3=False, dropout=False, dropoutrate=0.5,nepochs=2, path="model2.h5")

RunAgent(game_count=ngame, visible=False, waitForEyes=False,gamma=0.6, layer3=False, dropout=False, dropoutrate=0.5,nepochs=2, path="model3.h5")

RunAgent(game_count=ngame, visible=False, waitForEyes=False,gamma=0.8, layer3=False, dropout=False, dropoutrate=0.5,nepochs=2, path="model4.h5")

RunAgent(game_count=ngame, visible=False, waitForEyes=False,gamma=0.4, layer3=True, dropout=True, dropoutrate=0.3,nepochs=6, path="model5.h5")

RunAgent(game_count=ngame, visible=False, waitForEyes=False,gamma=0.4, layer3=True, dropout=True, dropoutrate=0.5,nepochs=6, path="model6.h5")

RunAgent(game_count=ngame, visible=False, waitForEyes=False,gamma=0.4, layer3=True, dropout=False, dropoutrate=0.5,nepochs=4, path="model7.h5")

RunAgent(game_count=ngame, visible=False, waitForEyes=False,gamma=0.2, layer3=True, dropout=False, dropoutrate=0.5,nepochs=4, path="model8.h5")

RunAgent(game_count=ngame, visible=False, waitForEyes=False,gamma=0.6, layer3=True, dropout=False, dropoutrate=0.5,nepochs=4, path="model9.h5")

RunAgent(game_count=ngame, visible=False, waitForEyes=False,gamma=0.8, layer3=True, dropout=False, dropoutrate=0.5,nepochs=4, path="model10.h5")
'''
#zygzak najlepszy prawy dolny
#RunAgent(game_count=ngame2, visible=True, waitForEyes=True,gamma=0.4, layer3=False, dropout=False, dropoutrate=0.5,nepochs=2, path="model1.h5",eps=0)
#zygzak glupi
#RunAgent(game_count=ngame2, visible=True, waitForEyes=True,gamma=0.2, layer3=False, dropout=False, dropoutrate=0.5,nepochs=2, path="model2.h5",eps=0)
#niezygzak prawy gorny
#RunAgent(game_count=ngame2, visible=True, waitForEyes=True,gamma=0.6, layer3=False, dropout=False, dropoutrate=0.5,nepochs=2, path="model3.h5",eps=0)
#zygzak nie zygzak glupi lewy gorny
#RunAgent(game_count=ngame2, visible=True, waitForEyes=True,gamma=0.8, layer3=False, dropout=False, dropoutrate=0.5,nepochs=2, path="model4.h5",eps=0)
#nie zygzak glupi lewy dolny
#RunAgent(game_count=ngame2, visible=True, waitForEyes=True,gamma=0.4, layer3=True, dropout=True, dropoutrate=0.3,nepochs=6, path="model5.h5",eps=0)
#bardzo glupi
#RunAgent(game_count=ngame2, visible=True, waitForEyes=True,gamma=0.4, layer3=True, dropout=True, dropoutrate=0.5,nepochs=6, path="model6.h5",eps=0)
#srednio glupi
#RunAgent(game_count=ngame2, visible=True, waitForEyes=True,gamma=0.4, layer3=True, dropout=False, dropoutrate=0.5,nepochs=4, path="model7.h5",eps=0)
# calkiem spoko rogi
#RunAgent(game_count=ngame2, visible=True, waitForEyes=True,gamma=0.2, layer3=True, dropout=False, dropoutrate=0.5,nepochs=4, path="model8.h5",eps=0)
# calkiem glupi prawy dolny
#RunAgent(game_count=ngame2, visible=True, waitForEyes=True,gamma=0.6, layer3=True, dropout=False, dropoutrate=0.5,nepochs=4, path="model9.h5",eps=0)
#zygzak do gory prawy gorny
#RunAgent(game_count=ngame2, visible=True, waitForEyes=True,gamma=0.8, layer3=True, dropout=False, dropoutrate=0.5,nepochs=4, path="model10.h5",eps=0)

#RunAgent(game_count=10, visible=True, waitForEyes=True, eps=0)