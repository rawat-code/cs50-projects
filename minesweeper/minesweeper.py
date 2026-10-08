import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)

            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are in cells
        that are within one row and column of cell,
        not including cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(
            max(0, cell[0] - 1),
            min(self.height, cell[0] + 2)
        ):
            for j in range(
                max(0, cell[1] - 1),
                min(self.width, cell[1] + 2)
            ):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Add to count if cell is a mine
                if self.board[i][j]:
                    count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines == self.mines_found


class Sentence:
    """
    Logical statement about a Minesweeper game.
    A sentence consists of a set of cells
    and a count of the number of those cells
    which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return (
            self.cells == other.cells
            and self.count == other.count
        )

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells
        that are known to be mines.
        """

        if self.count == len(self.cells) and self.count > 0:
            return set(self.cells)

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells
        that are known to be safe.
        """

        if self.count == 0:
            return set(self.cells)

        return set()

    def mark_mine(self, cell):
        """
        Updates the sentence given that a cell is known
        to be a mine.
        """

        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates the sentence given that a cell is known
        to be safe.
        """

        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have already been clicked
        self.moves_made = set()

        # Keep track of cells known to be mines
        self.mines = set()

        # Keep track of cells known to be safe
        self.safes = set()

        # List of all logical sentences known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to account for this information.
        """

        self.mines.add(cell)

        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to account for this information.
        """

        self.safes.add(cell)

        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us,
        for a given safe cell, how many mines
        are around that cell.
        """

        # Mark cell as having been made
        self.moves_made.add(cell)

        # Mark cell as safe
        self.mark_safe(cell)

        # Find neighboring cells
        neighbors = set()

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore cells outside the board
                if i < 0 or i >= self.height:
                    continue

                if j < 0 or j >= self.width:
                    continue

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                neighbor = (i, j)

                # If already known to be a mine,
                # reduce the count.
                if neighbor in self.mines:
                    count -= 1

                # If not known to be safe or a mine,
                # add it to the sentence.
                elif neighbor not in self.safes:
                    neighbors.add(neighbor)

        # Create a new sentence
        new_sentence = Sentence(neighbors, count)

        # Add it if it contains useful information
        if new_sentence.cells and new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        # Continue making inferences until no new information
        # can be found.
        while True:

            new_mines = set()
            new_safes = set()

            # Look for known mines and safe cells
            for sentence in self.knowledge:
                new_mines.update(sentence.known_mines())
                new_safes.update(sentence.known_safes())

            # Only keep genuinely new information
            new_mines -= self.mines
            new_safes -= self.safes

            # Mark newly discovered mines
            for mine in new_mines:
                self.mark_mine(mine)

            # Mark newly discovered safe cells
            for safe in new_safes:
                self.mark_safe(safe)

            # Find new sentences using subset inference
            new_sentences = []

            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:

                    if sentence1 == sentence2:
                        continue

                    # If sentence1 is a subset of sentence2,
                    # infer sentence2 - sentence1.
                    if (
                        sentence1.cells
                        and sentence1.cells < sentence2.cells
                    ):

                        new_cells = (
                            sentence2.cells - sentence1.cells
                        )

                        new_count = (
                            sentence2.count - sentence1.count
                        )

                        new_sentence = Sentence(
                            new_cells,
                            new_count
                        )

                        if (
                            new_sentence.cells
                            and new_sentence not in self.knowledge
                            and new_sentence not in new_sentences
                        ):
                            new_sentences.append(new_sentence)

            # Add newly inferred sentences
            for sentence in new_sentences:
                self.knowledge.append(sentence)

            # Remove empty sentences
            self.knowledge = [
                sentence
                for sentence in self.knowledge
                if sentence.cells
            ]

            # If nothing new was discovered, we're done
            if not new_mines and not new_safes and not new_sentences:
                break

    def make_safe_move(self):
        """
        Returns a safe cell that has not already been chosen,
        if one exists.
        """

        for cell in self.safes:
            if cell not in self.moves_made:
                return cell

        return None

    def make_random_move(self):
        """
        Returns a move that has not already been chosen
        and is not known to be a mine.
        """

        choices = []

        for i in range(self.height):
            for j in range(self.width):

                cell = (i, j)

                if cell in self.moves_made:
                    continue

                if cell in self.mines:
                    continue

                choices.append(cell)

        if not choices:
            return None

        return random.choice(choices)
