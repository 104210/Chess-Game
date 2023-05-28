import pygame

# This program is a good example of how you should always actually come up with
# the design of a program first before making it. Also, it's a good example of
# how you can know how to program, but not know to make the program actually good.

# The code is so bad that it makes me feel unwell, so don't get sick looking at this.

pygame.init()

WIDTH, HEIGHT = 720, 720
CELL_WIDTH, CELL_HEIGHT = WIDTH / 8, HEIGHT / 8

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
CLOCK = pygame.time.Clock()

# Load in the board and make it 10 times bigger for better visibility.
BOARD = pygame.image.load("sprites/boards/board 1.png")
BOARD = pygame.transform.scale_by(BOARD, 10)

# This sprite's rect is used to detect collisions between the mouse and a piece.
MOUSE_SPRITE = pygame.sprite.Sprite()
MOUSE_SPRITE.image = pygame.Surface((1, 1))
MOUSE_SPRITE.rect = MOUSE_SPRITE.image.get_rect()


class Piece(pygame.sprite.Sprite):
    """Used to represent the pieces of each player."""

    # These will hold all of the surfaces that will be used for the pieces.
    white_piece_surfs = {}
    black_piece_surfs = {}

    def __init__(self, surf: pygame.Surface, pos: tuple, type: str):
        super().__init__()

        self.image = surf
        self.rect = surf.get_rect(center=pos)
        
        # Used to make a piece return to the square it was on if it cannot move to a certain square.
        self.pos_before_click = surf.get_rect(center=pos)
        # Holds what exactly a piece is. For example, whatever or not it's a pawn or something else.
        self.type = type
    
    def calculate_legal_squares(self) -> list:
        """Creates and returns a list of x and y positions that the piece can move to."""

        legal_squares = []

        # God forgive me.

        match self.type:
            case "pawn":
                if turn == "white":
                    print("Idk.")
                    
                    pass

    @staticmethod
    def capture(captured_piece: "Piece") -> None:
        """Allows for the capturing of pieces."""

        # Yes, that's all.
        captured_piece.kill()

    @staticmethod
    def change_turn() -> None:
        """Changes whos turn it is."""

        global turn

        if turn == "white":
            turn = "black"
        else:
            turn = "white"

    @staticmethod
    def click() -> None:
        """Used to pick pieces up or put them down."""

        # If the mouse was left-clicked.
        if pygame.mouse.get_pressed()[0]:
            global clicked_piece, MOUSE_SPRITE, moving, turn

            # See if we are already moving a piece. If not, then start moving one if possible.
            if not moving:
                # Only check for collisions with the pieces of the player whos turn it is.
                if turn == "white":
                    clicked_piece = pygame.sprite.spritecollideany(MOUSE_SPRITE, white_pieces)
                else:
                    clicked_piece = pygame.sprite.spritecollideany(MOUSE_SPRITE, black_pieces)

                # See if a piece was actually clicked on.
                if clicked_piece:
                    clicked_piece.pos_before_click.center = clicked_piece.rect.center
                    # Let the piece follow the mouse.
                    moving = True
            # If already moving a piece,
            else:
                Piece.put_down_piece()
    
    @staticmethod
    def load_surfs() -> None:
        """Loads in all of the surfaces that will be used for pieces."""

        for piece_name in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
            # These lines load in a sprite and save it under the name of the sprite in the dictionary.
            # They also make the sprites 5 times bigger for better visibility.
            Piece.white_piece_surfs[piece_name] = pygame.transform.scale_by(pygame.image.load(f"sprites/pieces/white/{piece_name}.png"), 5)
            Piece.black_piece_surfs[piece_name] = pygame.transform.scale_by(pygame.image.load(f"sprites/pieces/black/{piece_name}.png"), 5)

    @staticmethod
    def put_down_piece() -> None:
        """Puts down a piece if possible. Yep."""

        global clicked_piece, MOUSE_SPRITE, moving, turn

        # If already moving a piece, then stop moving it.
        moving = False

        # Holds where the piece would like to go to.
        piece_new_pos = [
            MOUSE_SPRITE.rect.center[0]//CELL_WIDTH * CELL_WIDTH + CELL_WIDTH / 2,
            MOUSE_SPRITE.rect.center[1]//CELL_HEIGHT * CELL_HEIGHT + CELL_HEIGHT / 2
        ]

        # Puts the piece down.
        if turn == "white":
            if len(pygame.sprite.spritecollide(clicked_piece, white_pieces, False)) == 2:
                # Move piece back to where it was, because you can't jump onto your own pieces or
                # move to where your pieces already are.
                clicked_piece.rect.center = clicked_piece.pos_before_click.center

                # We don't change whos turn it is here, because White hasn't move a piece yet.
            elif (captured_piece := pygame.sprite.spritecollideany(clicked_piece, black_pieces)):
                # Calculate what squares we can move to and then loop over them.
                for square_pos in clicked_piece.calc_legal_squares():
                    # If the place we want to go to (new_piece_pos) is in below list,
                    if square_pos == piece_new_pos:
                        # then we let the piece go there.
                        clicked_piece.rect.center = (piece_new_pos[0], piece_new_pos[1])

                        Piece.capture(captured_piece)

                        Piece.change_turn()

                        break
            else:
                # If the piece hasn't touched a white or black piece, then we would like to simply
                # put it down into the center of a chess board square.

                # Calculate what squares we can move to and then loop over them.
                for square_pos in clicked_piece.calc_legal_squares():
                    # If the place we want to go to (new_piece_pos) is in below list,
                    if square_pos == piece_new_pos:
                        # then we let the piece go there.
                        clicked_piece.rect.center = (piece_new_pos[0], piece_new_pos[1])

                        Piece.capture(captured_piece)

                        Piece.change_turn()

                        break

                Piece.change_turn()
        else:
            if len(pygame.sprite.spritecollide(clicked_piece, black_pieces, False)) == 2:
                # Move piece back where it was, because you can't jump onto your own pieces or
                # move to where your pieces already are.
                clicked_piece.rect.center = clicked_piece.pos_before_click.center

                # We don't change whos turn it is here, because Black hasn't move a piece yet.
            elif (captured_piece := pygame.sprite.spritecollideany(clicked_piece, white_pieces)):
                clicked_piece.rect.center = (piece_new_pos[0], piece_new_pos[1])

                Piece.capture(captured_piece)

                Piece.change_turn()
            else:
                # If the piece hasn't touched a white or black piece, then simply
                # put it down into the center of a chess board square.
                clicked_piece.rect.center = (piece_new_pos[0], piece_new_pos[1])

                Piece.change_turn()

        clicked_piece = None

    @staticmethod
    def create_white_pieces() -> pygame.sprite.Group:
        """Creates pieces for the white player."""

        # Holds the white player's pieces.
        white_pieces = pygame.sprite.Group()

        # These coords are used for determining where white's first piece will be placed.
        white_x = CELL_WIDTH / 2
        white_y = (CELL_HEIGHT / 2) + CELL_HEIGHT*6

        # Places all of white's pawns (first piece row).
        for i in range(8):
            white_pieces.add(Piece(Piece.white_piece_surfs["pawn"], (white_x, white_y), "pawn"))

            white_x += CELL_WIDTH

        white_x = CELL_WIDTH / 2
        white_y += CELL_HEIGHT

        # Places the rest of white's pieces (second piece row).
        for piece_name in ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook"]:
            white_pieces.add(Piece(Piece.white_piece_surfs[piece_name], (white_x, white_y), piece_name))

            white_x += CELL_WIDTH
        
        return white_pieces
    
    @staticmethod
    def create_black_pieces() -> pygame.sprite.Group:
        """Creates pieces for the black player."""

        # Holds the black player's pieces.
        black_pieces = pygame.sprite.Group()

        # These coords are used for determining where black's first piece will be placed.
        black_x = WIDTH - CELL_WIDTH/2
        black_y = (CELL_HEIGHT / 2) + CELL_HEIGHT

        # Places all of black's pawns (first piece row).
        for i in range(8):
            black_pieces.add(Piece(Piece.black_piece_surfs["pawn"], (black_x, black_y), "pawn"))

            black_x -= CELL_WIDTH

        black_x = WIDTH - CELL_WIDTH/2
        black_y -= CELL_HEIGHT

        # Places the rest of black's pieces (second piece row).
        for piece_name in ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]:
            black_pieces.add(Piece(Piece.black_piece_surfs[piece_name], (black_x, black_y), piece_name))

            black_x -= CELL_WIDTH
        
        return black_pieces


# Load in surfaces for pieces.
Piece.load_surfs()

white_pieces = Piece.create_white_pieces()
black_pieces = Piece.create_black_pieces()

# Removes these dictionaries containing surfaces, because they are only used once
# and then never again, so no need to have them any more. May change this later.
# Also, these are the surfaces that were loaded in above.
del Piece.white_piece_surfs, Piece.black_piece_surfs

# Used to keep track of what piece is currently being moved.
clicked_piece = None
# Used to keep track of whatever or not the player
# is currently moving a piece.
moving = False
# Keeps track of whos turn it currently is.
turn = "white"

# The main game loop.
while True:
    # Updates the rect of the MOUSE_SPRITE, which is used to check for collisions with pieces.
    MOUSE_SPRITE.rect.center = pygame.mouse.get_pos()

    # Handles things that the player does (events).
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Lets the player click stuff (like picking up a piece or putting it down).
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Piece.click()
        
    # If we're moving a piece,
    if moving:
        # then let it continue to follow the mouse.
        clicked_piece.rect.center = MOUSE_SPRITE.rect.center

    # Draws everything.
    # SCREEN.fill("black")
    SCREEN.blit(BOARD, (0, 0))
    white_pieces.draw(SCREEN)
    black_pieces.draw(SCREEN)

    pygame.display.update()
    CLOCK.tick(60)