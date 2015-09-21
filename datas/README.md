# datas/

This folder is for base datas that are re-used between games. A good example is TurnBased. Many games are turn based so instead of re-defining all the turn gamed game structures we pre-define it here.

If you find a game pattern is being copied between games it's a good idea to abstract it, then inherit it, from here and probably in the server logic.
