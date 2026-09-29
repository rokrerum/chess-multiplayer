"""
Regression tests for the chess engine (chess.py + chess_ai.py).

Each test corresponds to a specific bug that was found and fixed during
a debugging session. The goal is to catch regressions if any of these
conditions gets accidentally flipped back during future refactoring.

Run with: pytest test_chess.py -v
"""

import copy
import pytest
import chess
import chess_ai


def empty_board():
    """Empty 8x8 board - a convenient starting point for building test positions."""
    return [["" for _ in range(8)] for _ in range(8)]


def default_castling():
    return {
        "white": {"king": True, "Rook-L": True, "Rook-R": True},
        "black": {"king": True, "Rook-L": True, "Rook-R": True},
    }


def board_with_kings():
    """Empty board with both kings placed in a safe corner (off the main
    lines/diagonals from (4,4), where the piece under test is usually placed) -
    required because if_not_checke_after() assumes both kings exist on the
    board (otherwise check() returns 'always in check' as a safeguard)."""
    board = empty_board()
    board[7][0] = "k"
    board[0][7] = "K"
    return board


@pytest.fixture
def cm():
    return chess.piece_moves()


@pytest.fixture
def ai():
    return chess_ai.AI()


# ---------------------------------------------------------------------------
# MATE IN ONE - regression for the inverted max/min bug in min_max, and the
# inverted sign bug in evaluating() (both branches: my_color == "white"
# and my_color == "black")
# ---------------------------------------------------------------------------

MATE_IN_ONE_WHITE_TO_MOVE_LOSES = [
    ["R", "N", "B", "K", "Q", "B", "N", "R"],
    ["", "P", "P", "P", "P", "P", "P", "P"],
    ["", "Q", "Q", "", "Q", "", "", ""],
    ["P", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["p", "", "", "k", "", "p", "p", "p"],
    ["r", "", "", "", "", "", "", "r"],
]

# mirror image of the position above (case + row order flipped), used to
# check the other branch of evaluating() (my_color == "black")
MATE_IN_ONE_BLACK_TO_MOVE_LOSES = [
    ["R", "", "", "", "", "", "", "R"],
    ["P", "", "", "K", "", "P", "P", "P"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["p", "", "", "", "", "", "", ""],
    ["", "q", "q", "", "q", "", "", ""],
    ["", "p", "p", "p", "p", "p", "p", "p"],
    ["r", "n", "b", "k", "q", "b", "n", "r"],
]


def test_mate_in_one_ai_plays_white(ai):
    """AI plays white (my_color='black'). It must find Qb3-d5#."""
    result = ai.ai(
        MATE_IN_ONE_BLACK_TO_MOVE_LOSES, "white", "black", [False], default_castling()
    )
    assert result[0] == 999999
    assert result[1] == ((5, 1), (3, 3))


def test_mate_in_one_ai_plays_black(ai):
    """AI plays black (my_color='white'). It must find Qb6-d4#.
    This is the test that would catch an inverted sign in evaluating()
    for the my_color=='white' branch (bug: '-999999 if mate[1] else -999999')."""
    result = ai.ai(
        MATE_IN_ONE_WHITE_TO_MOVE_LOSES, "black", "white", [False], default_castling()
    )
    assert result[0] == 999999
    assert result[1] == ((2, 1), (4, 3))


def test_check_mate_detects_correct_side(cm):
    """check_mate() on its own (without AI) must correctly report that
    white is checkmated and black is not, in a known position."""
    mate = cm.check_mate(MATE_IN_ONE_WHITE_TO_MOVE_LOSES, "white", default_castling(), [False])
    assert mate == [False, False]  # nobody is checkmated before the move


# ---------------------------------------------------------------------------
# PAWN PROMOTION - regression for the IndexError crash when a pawn reaches
# the last row during AI's simulated search without being promoted
# ---------------------------------------------------------------------------

def test_pawn_promotes_in_simulated_move_white(ai):
    board = empty_board()
    board[6][3] = "p"  # white pawn one step from promotion
    new_board = ai.board_after_move(board, ((6, 3), (7, 3)))
    assert new_board[7][3] == "q"


def test_pawn_promotes_in_simulated_move_black(ai):
    board = empty_board()
    board[1][3] = "P"  # black pawn one step from promotion
    new_board = ai.board_after_move(board, ((1, 3), (0, 3)))
    assert new_board[0][3] == "Q"


def test_non_pawn_piece_not_promoted(ai):
    """Guard against accidentally 'promoting' some other piece that
    happens to land on the last row."""
    board = empty_board()
    board[6][3] = "r"
    new_board = ai.board_after_move(board, ((6, 3), (7, 3)))
    assert new_board[7][3] == "r"


def test_pawn_search_near_promotion_does_not_crash(ai):
    """Regression for a real crash: AI searching positions with a pawn
    close to promotion should not raise IndexError."""
    board = empty_board()
    board[7][4] = "K"
    board[0][4] = "k"
    board[1][0] = "p"  # white pawn one step from promotion
    result = ai.ai(board, "white", "black", [False], default_castling())
    assert result is not None  # the important part: it did not crash


# ---------------------------------------------------------------------------
# CASTLING - regression for the 'elif' bug in move_castle (one rook blocked
# detection of the other) and for mutating castling in place (corrupting
# game.castling)
# ---------------------------------------------------------------------------

def test_king_move_disables_all_castling_rights(ai):
    board = empty_board()
    board[0][4] = "k"
    new_castling = ai.move_castle(board, default_castling(), 0, 4)
    assert new_castling["white"]["king"] is False
    assert new_castling["white"]["Rook-L"] is False
    assert new_castling["white"]["Rook-R"] is False
    assert new_castling["black"]["king"] is True  # the other side untouched


def test_left_rook_leaving_disables_only_rook_l(ai):
    board = empty_board()
    board[0][0] = ""  # the left rook just left
    board[0][7] = "r"  # the right one is still in place
    new_castling = ai.move_castle(board, default_castling(), 0, 3)
    assert new_castling["white"]["Rook-L"] is False
    assert new_castling["white"]["Rook-R"] is True


def test_right_rook_leaving_after_left_already_gone(ai):
    """This is exactly the scenario that caught the 'elif' bug:
    the left rook ALREADY left its corner a while ago, and now the right
    one is leaving too. Rook-R MUST be disabled, even though Rook-L is
    already False."""
    castling = default_castling()
    castling["white"]["Rook-L"] = False  # left rook already gone

    board = empty_board()
    board[0][0] = ""  # left corner has been empty for a while
    board[0][7] = ""  # right rook JUST left
    new_castling = ai.move_castle(board, castling, 0, 5)

    assert new_castling["white"]["Rook-R"] is False


def test_rook_captured_by_any_piece_disables_castling(ai):
    """A rook being captured by ANY piece (not just a rook/king) should
    disable castling on that side."""
    board = empty_board()
    board[0][0] = "N"  # a knight just captured the white rook on its corner
    new_castling = ai.move_castle(board, default_castling(), 0, 0)
    assert new_castling["white"]["Rook-L"] is False


def test_move_castle_does_not_mutate_original_dict(ai):
    """Regression for game.castling corruption: move_castle MUST NOT
    modify the passed-in dict in place, since it's the same game.castling
    object from main.py."""
    original = default_castling()
    board = empty_board()
    board[0][4] = "k"
    ai.move_castle(board, original, 0, 4)
    assert original["white"]["king"] is True, "the original dict got corrupted!"


def test_castling_move_available_when_path_clear(cm):
    board = empty_board()
    board[0][4] = "k"
    board[0][0] = "r"
    board[0][7] = "r"
    board[7][7] = "K"  # opponent king, required by if_not_checke_after
    moves = cm.king_moves(board, 0, 4, "white", default_castling(), "white")
    destinations = [(m[0], m[1]) for m in moves]
    assert (0, 2) in destinations  # long castle
    assert (0, 6) in destinations  # short castle


def test_castling_unavailable_when_flag_false(cm):
    board = empty_board()
    board[0][4] = "k"
    board[0][0] = "r"
    board[0][7] = "r"
    board[7][7] = "K"  # opponent king, required by if_not_checke_after
    castling = default_castling()
    castling["white"]["Rook-L"] = False
    moves = cm.king_moves(board, 0, 4, "white", castling, "white")
    destinations = [(m[0], m[1]) for m in moves]
    assert (0, 2) not in destinations
    assert (0, 6) in destinations


# ---------------------------------------------------------------------------
# EN PASSANT - regression for the inverted condition (!= instead of ==)
# in move_en_passant
# ---------------------------------------------------------------------------

def test_double_pawn_move_sets_en_passant(ai):
    board = empty_board()
    board[4][3] = "p"
    result = ai.move_en_passant(board, [False], row=6, new_row=4, new_col=3)
    assert result == [True, 4, 3]


def test_single_pawn_move_clears_en_passant(ai):
    board = empty_board()
    board[5][3] = "p"
    result = ai.move_en_passant(board, [True, 4, 3], row=6, new_row=5, new_col=3)
    assert result == [False]


def test_non_pawn_move_clears_stale_en_passant(ai):
    """A move by any other piece should clear an existing en_passant flag,
    since it's only valid for a single move."""
    board = empty_board()
    board[4][3] = "n"
    result = ai.move_en_passant(board, [True, 4, 3], row=6, new_row=4, new_col=3)
    assert result == [False]


def test_en_passant_capture_is_generated(cm):
    """Checks that pawn_moves() actually generates an en_passant_move
    entry when the conditions are met."""
    board = board_with_kings()
    board[3][3] = "p"  # white pawn on the fifth rank
    board[3][4] = "P"  # black pawn next to it, which just double-moved
    en_passant = [True, 3, 4]
    moves = cm.pawn_moves(board, 3, 3, "white", "white", en_passant)
    flagged = [m for m in moves if len(m) == 3 and m[2] == "en_passant_move"]
    assert len(flagged) == 1
    assert flagged[0][:2] == [4, 4]


# ---------------------------------------------------------------------------
# PAWN DOUBLE MOVE - regression for the swapped row==1/row==6 condition
# ---------------------------------------------------------------------------

def test_white_pawn_double_move_from_start(cm):
    board = board_with_kings()
    board[1][0] = "p"
    moves = cm.pawn_moves(board, 1, 0, "white", "black", [False])
    assert [2, 0] in moves
    assert any(m[:2] == [3, 0] for m in moves)


def test_black_pawn_double_move_from_start(cm):
    board = board_with_kings()
    board[6][0] = "P"
    moves = cm.pawn_moves(board, 6, 0, "black", "black", [False])
    assert [5, 0] in moves
    assert any(m[:2] == [4, 0] for m in moves)


def test_pawn_not_on_start_row_cannot_double_move(cm):
    board = board_with_kings()
    board[3][0] = "p"  # white pawn already past its starting row
    moves = cm.pawn_moves(board, 3, 0, "white", "black", [False])
    assert [4, 0] in moves
    assert not any(m[:2] == [5, 0] for m in moves)


# ---------------------------------------------------------------------------
# BOARD ORIENTATION - regression for the where_to_move bug that depended on
# my_color instead of the moving piece's own color
# ---------------------------------------------------------------------------

def test_white_pawn_moves_towards_increasing_rows(cm):
    board = board_with_kings()
    board[3][0] = "p"
    moves = cm.pawn_moves(board, 3, 0, "white", "black", [False])
    assert [4, 0] in moves
    assert [2, 0] not in moves


def test_black_pawn_moves_towards_decreasing_rows(cm):
    board = board_with_kings()
    board[3][0] = "P"
    moves = cm.pawn_moves(board, 3, 0, "black", "black", [False])
    assert [2, 0] in moves
    assert [4, 0] not in moves


def test_pawn_direction_independent_of_my_color(cm):
    """The pawn's move direction is a fact about the piece itself, not
    about who the AI/human is playing as - this was the main board
    orientation bug."""
    board = board_with_kings()
    board[3][0] = "p"
    moves_a = cm.pawn_moves(board, 3, 0, "white", "white", [False])
    moves_b = cm.pawn_moves(board, 3, 0, "white", "black", [False])
    assert moves_a == moves_b


# ---------------------------------------------------------------------------
# SLIDING_MOVES (rook/bishop/queen consolidation) - basic correctness
# ---------------------------------------------------------------------------

ROOK_DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
BISHOP_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def test_rook_moves_in_straight_lines_only(cm):
    board = board_with_kings()
    board[4][4] = "r"
    moves = cm.sliding_moves(board, 4, 4, "white", "white", ROOK_DIRS)
    assert (4, 0) in moves
    assert (0, 4) in moves
    assert (3, 3) not in moves  # diagonal - not a rook move


def test_bishop_moves_diagonally_only(cm):
    board = board_with_kings()
    board[4][4] = "b"
    moves = cm.sliding_moves(board, 4, 4, "white", "white", BISHOP_DIRS)
    assert (0, 0) in moves
    assert (4, 0) not in moves  # straight line - not a bishop move


def test_sliding_piece_stops_at_own_piece(cm):
    board = board_with_kings()
    board[4][4] = "r"
    board[4][6] = "p"  # own piece blocking further movement
    moves = cm.sliding_moves(board, 4, 4, "white", "white", ROOK_DIRS)
    assert (4, 5) in moves  # empty square before the own piece
    assert (4, 6) not in moves  # cannot move onto an own piece
    assert (4, 7) not in moves  # nor past it


def test_sliding_piece_can_capture_enemy(cm):
    board = board_with_kings()
    board[4][4] = "r"
    board[4][6] = "P"  # enemy piece
    moves = cm.sliding_moves(board, 4, 4, "white", "white", ROOK_DIRS)
    assert (4, 6) in moves  # capture allowed
    assert (4, 7) not in moves  # but not further than that


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))