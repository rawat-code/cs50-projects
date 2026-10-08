import random


class Nim():

    def __init__(self, initial=[1, 3, 5, 7]):
        """
        Initialize Nim game with the given number of piles.
        Each pile contains initial[i] objects.
        """
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        """
        Returns a set of all possible actions
        (i, j) where pile i contains at least j objects.
        """
        actions = set()

        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))

        return actions

    @classmethod
    def other_player(cls, player):
        """
        Returns the player who is not the player given.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = Nim.other_player(self.player)

    def move(self, action):
        """
        Make the given move, which should be of the form
        (i, j). If pile i contains fewer than j objects,
        or if there are no objects in pile i, then raise
        an Exception.

        If the move is legal, update the current state
        to reflect the move and switch the current player.
        If the move leaves all piles empty, then the game
        is over, and self.winner is set to the player who
        made the move.
        """
        pile, count = action

        if self.winner is not None:
            raise Exception("Game already won.")

        if pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile.")

        if count < 1 or self.piles[pile] < count:
            raise Exception("Invalid number of objects.")

        self.piles[pile] -= count

        self.switch_player()

        if all(pile == 0 for pile in self.piles):
            self.winner = self.other_player(self.player)


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        and set alpha and epsilon values.
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state,
        an action taken in that state, a new resulting state,
        and the reward received from taking that action.
        """
        old_q = self.get_q_value(old_state, action)
        future_rewards = self.best_future_reward(new_state)

        self.update_q_value(
            old_state,
            action,
            old_q,
            reward,
            future_rewards
        )

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state/action pair.
        If no Q-value exists yet, return 0.
        """
        state = tuple(state)
        return self.q.get((state, action), 0)

    def update_q_value(
        self,
        state,
        action,
        old_q,
        reward,
        future_rewards
    ):
        """
        Update the Q-value for the state/action pair
        using the Q-learning formula.
        """
        new_q = old_q + self.alpha * (
            reward + future_rewards - old_q
        )

        state = tuple(state)
        self.q[(state, action)] = new_q

    def best_future_reward(self, state):
        """
        Return the best Q-value for any available action
        in the given state.
        """
        actions = Nim.available_actions(state)

        if not actions:
            return 0

        return max(
            self.get_q_value(state, action)
            for action in actions
        )

    def choose_action(self, state, epsilon=True):
        """
        Choose an action based on the current state.

        If epsilon is True, use epsilon-greedy selection:
        with probability epsilon, choose randomly;
        otherwise choose the best action.

        If epsilon is False, always choose the best action.
        """
        actions = Nim.available_actions(state)

        if not actions:
            return None

        if epsilon and random.random() < self.epsilon:
            return random.choice(list(actions))

        best_action = None
        best_q = float("-inf")

        for action in actions:
            q_value = self.get_q_value(state, action)

            if q_value > best_q:
                best_q = q_value
                best_action = action

        return best_action


def train(n):
    """
    Train an AI by playing n games against itself.
    """

    player = NimAI()

    for i in range(n):
        print(f"Playing training game {i + 1}")

        game = Nim()

        last_move = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Keep track of last state and action
            last_move[game.player]["state"] = state
            last_move[game.player]["action"] = action

            # Make move
            game.move(action)

            # Win condition
            if game.winner is not None:

                # Give winning move reward
                player.update(
                    state,
                    action,
                    game.piles,
                    1
                )

                # Give losing move reward
                loser = game.player

                if last_move[loser]["state"] is not None:
                    player.update(
                        last_move[loser]["state"],
                        last_move[loser]["action"],
                        game.piles,
                        -1
                    )

                break

            # Give previous move a reward of 0
            current_player = game.player

            if last_move[current_player]["state"] is not None:
                player.update(
                    last_move[current_player]["state"],
                    last_move[current_player]["action"],
                    game.piles,
                    0
                )

    print("Done training")
    return player


def play(ai, human_player=None):
    """
    Let a human play against an AI.
    """

    game = Nim()

    if human_player is None:
        human_player = 0

    while True:

        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")

        print()

        available_actions = Nim.available_actions(game.piles)

        if game.player == human_player:
            print("Your Turn")
            print("Possible actions:")
            for action in available_actions:
                print(action)

            pile = int(input("Choose Pile: "))
            count = int(input("Choose Count: "))

            action = (pile, count)

            if action not in available_actions:
                print("Invalid move. Try again.")
                continue

        else:
            print("AI's Turn")
            action = ai.choose_action(
                game.piles,
                epsilon=False
            )

            print(
                f"AI chose to take {action[1]} "
                f"from pile {action[0]}."
            )

        game.move(action)

        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = game.winner

            if winner == human_player:
                print("You win!")
            else:
                print("AI wins!")

            return
``