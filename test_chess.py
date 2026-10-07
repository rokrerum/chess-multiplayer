import pytest
import chess
import chess_ai


def empty_board():
    return [["" for _ in range(8)] for _ in range(8)]


def default_castling():
    return {"white": {"king": True, "Rook-L": True, "Rook-R": True},
            "black": {"king": True, "Rook-L": True, "Rook-R": True}}


def board_with_kings():
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
    result = ai.ai(MATE_IN_ONE_BLACK_TO_MOVE_LOSES, "white", "black", [False], default_castling())
    assert result[0] == 999999
    assert result[1] == ((5, 1), (3, 3))


def test_mate_in_one_ai_plays_black(ai):
    result = ai.ai(MATE_IN_ONE_WHITE_TO_MOVE_LOSES, "black", "white", [False], default_castling())
    assert result[0] == 999999
    assert result[1] == ((2, 1), (4, 3))


def test_check_mate_detects_correct_side(cm):
    state = cm.game_end_chcek(MATE_IN_ONE_WHITE_TO_MOVE_LOSES, "white", default_castling(), "white" , [False])
    assert state == [False, False, None]


def test_pawn_promotes_in_simulated_move_white(ai):
    board = empty_board()
    board[6][3] = "p"
    new_board = ai.board_after_move(board, ((6, 3), (7, 3)))
    assert new_board[7][3] == "q"


def test_pawn_promotes_in_simulated_move_black(ai):
    board = empty_board()
    board[1][3] = "P"
    new_board = ai.board_after_move(board, ((1, 3), (0, 3)))
    assert new_board[0][3] == "Q"


def test_non_pawn_piece_not_promoted(ai):
    board = empty_board()
    board[6][3] = "r"
    new_board = ai.board_after_move(board, ((6, 3), (7, 3)))
    assert new_board[7][3] == "r"


def test_pawn_search_near_promotion_does_not_crash(ai):
    board = empty_board()
    board[7][4] = "K"
    board[0][4] = "k"
    board[1][0] = "p"
    result = ai.ai(board, "white", "black", [False], default_castling())
    assert result is not None


def test_king_move_disables_all_castling_rights(ai):
    board = empty_board()
    board[0][4] = "k"
    new_castling = ai.move_castle(board, default_castling(), 0, 4)
    assert new_castling["white"]["king"] is False
    assert new_castling["white"]["Rook-L"] is False
    assert new_castling["white"]["Rook-R"] is False
    assert new_castling["black"]["king"] is True


def test_left_rook_leaving_disables_only_rook_l(ai):
    board = empty_board()
    board[0][0] = ""
    board[0][7] = "r"
    new_castling = ai.move_castle(board, default_castling(), 0, 3)
    assert new_castling["white"]["Rook-L"] is False
    assert new_castling["white"]["Rook-R"] is True


def test_right_rook_leaving_after_left_already_gone(ai):
    castling = default_castling()
    castling["white"]["Rook-L"] = False
    board = empty_board()
    board[0][0] = ""
    board[0][7] = ""
    new_castling = ai.move_castle(board, castling, 0, 5)
    assert new_castling["white"]["Rook-R"] is False


def test_rook_captured_by_any_piece_disables_castling(ai):
    board = empty_board()
    board[0][0] = "N"
    new_castling = ai.move_castle(board, default_castling(), 0, 0)
    assert new_castling["white"]["Rook-L"] is False


def test_move_castle_does_not_mutate_original_dict(ai):
    original = default_castling()
    board = empty_board()
    board[0][4] = "k"
    ai.move_castle(board, original, 0, 4)
    assert original["white"]["king"] is True


def test_castling_move_available_when_path_clear(cm):
    board = empty_board()
    board[0][4] = "k"
    board[0][0] = "r"
    board[0][7] = "r"
    board[7][7] = "K"
    moves = cm.king_moves(board, 0, 4, "white", default_castling(), "white")
    destinations = [(m[0], m[1]) for m in moves]
    assert (0, 2) in destinations
    assert (0, 6) in destinations


def test_castling_unavailable_when_flag_false(cm):
    board = empty_board()
    board[0][4] = "k"
    board[0][0] = "r"
    board[0][7] = "r"
    board[7][7] = "K"
    castling = default_castling()
    castling["white"]["Rook-L"] = False
    moves = cm.king_moves(board, 0, 4, "white", castling, "white")
    destinations = [(m[0], m[1]) for m in moves]
    assert (0, 2) not in destinations
    assert (0, 6) in destinations


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
    board = empty_board()
    board[4][3] = "n"
    result = ai.move_en_passant(board, [True, 4, 3], row=6, new_row=4, new_col=3)
    assert result == [False]


def test_en_passant_capture_is_generated(cm):
    board = board_with_kings()
    board[3][3] = "p"
    board[3][4] = "P"
    en_passant = [True, 3, 4]
    moves = cm.pawn_moves(board, 3, 3, "white", "white", en_passant)
    flagged = [m for m in moves if len(m) == 3 and m[2] == "en_passant_move"]
    assert len(flagged) == 1
    assert flagged[0][:2] == [4, 4]


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
    board[3][0] = "p"
    moves = cm.pawn_moves(board, 3, 0, "white", "black", [False])
    assert [4, 0] in moves
    assert not any(m[:2] == [5, 0] for m in moves)


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
    board = board_with_kings()
    board[3][0] = "p"
    moves_a = cm.pawn_moves(board, 3, 0, "white", "white", [False])
    moves_b = cm.pawn_moves(board, 3, 0, "white", "black", [False])
    assert moves_a == moves_b


ROOK_DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
BISHOP_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def test_rook_moves_in_straight_lines_only(cm):
    board = board_with_kings()
    board[4][4] = "r"
    moves = cm.sliding_moves(board, 4, 4, "white", "white", ROOK_DIRS)
    assert (4, 0) in moves
    assert (0, 4) in moves
    assert (3, 3) not in moves


def test_bishop_moves_diagonally_only(cm):
    board = board_with_kings()
    board[4][4] = "b"
    moves = cm.sliding_moves(board, 4, 4, "white", "white", BISHOP_DIRS)
    assert (0, 0) in moves
    assert (4, 0) not in moves


def test_sliding_piece_stops_at_own_piece(cm):
    board = board_with_kings()
    board[4][4] = "r"
    board[4][6] = "p"
    moves = cm.sliding_moves(board, 4, 4, "white", "white", ROOK_DIRS)
    assert (4, 5) in moves
    assert (4, 6) not in moves
    assert (4, 7) not in moves


def test_sliding_piece_can_capture_enemy(cm):
    board = board_with_kings()
    board[4][4] = "r"
    board[4][6] = "P"
    moves = cm.sliding_moves(board, 4, 4, "white", "white", ROOK_DIRS)
    assert (4, 6) in moves
    assert (4, 7) not in moves


# ---------------------------------------------------------------------------
# GAME_END_CHCEK - the merged mate/stalemate function
# ---------------------------------------------------------------------------

def test_game_end_chcek_mate_sets_correct_color_index(cm):
    """Only the checkmated side's index should be True; the other stays False."""
    state = cm.game_end_chcek(MATE_IN_ONE_WHITE_TO_MOVE_LOSES, "white", default_castling(), "black", [False])
    # (position is pre-move; nobody's mated yet - verifies no false positive)
    assert state[2] is None
    assert state[0] is False
    assert state[1] is False


def test_game_end_chcek_detects_mate_after_move(cm, ai):
    board_after = ai.board_after_move(MATE_IN_ONE_WHITE_TO_MOVE_LOSES, ((2, 1), (4, 3)))
    state = cm.game_end_chcek(board_after, "white", default_castling(), "white", [False])
    assert state[2] == "mate"
    assert state[0] is True  # white (the checkmated side) specifically
    assert state[1] is False  # black must NOT be flagged


def test_game_end_chcek_stalemate_sets_only_that_color(cm):
    """Classic stalemate: black king in the corner, no legal moves, not in check.
    `turn` is who is to move right now (black, since black is stalemated)."""
    board = empty_board()
    board[0][0] = "K"  # black king cornered
    board[1][2] = "q"  # white queen controlling escape squares
    board[2][1] = "k"  # white king supporting, not adjacent-check
    state = cm.game_end_chcek(board, "black", default_castling(), "black", [False])
    assert state[2] == "stalemate"
    assert state[1] is True  # black specifically
    assert state[0] is False  # white must NOT be flagged (regression for the old "set both" bug)


def test_game_end_chcek_integrates_correctly_with_evaluating(ai):
    """Full regression through the new evaluating()/game_ended() wiring."""
    result = ai.ai(MATE_IN_ONE_WHITE_TO_MOVE_LOSES, "black", "white", [False], default_castling())
    assert result[0] == 999999
    assert result[1] == ((2, 1), (4, 3))


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))