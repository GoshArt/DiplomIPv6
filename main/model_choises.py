class GAME_RES:
    BLACK_VICTORY = "black_victory"
    WHITE_VICTORY = "white_victory"
    ACTIVE = "active"
    ABORTED = "aborted"
    GAME_RESULT_CHOISES = (
        (BLACK_VICTORY, "BlackVictory"),
        (WHITE_VICTORY, "WhiteVictory"),
        (ACTIVE, "Active"),
        (ABORTED, "Aborted"),
    )


class USER_ROLES:
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    OWNER = "OWNER"
    USER_ROLE_CHOISES = (
        (STUDENT, "STUDENT"),
        (TEACHER, "TEACHER"),
        (OWNER, "OWNER"),
    )
