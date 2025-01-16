from frontend.bot.games.false_state import FalseStateGame
from frontend.bot.games.false_state.schemas import Statements
from frontend.bot.base.texts import escape_markdown_v2

def with_game_slug(st: str) -> str:
    return f"{FalseStateGame.slug}_{st}"

def get_explain_user_wrong(expected: Statements, user_marked: list[int]) -> str:
    forgot_to_mark_inds = sorted(list(expected.wrong_inds - set(user_marked)))
    marked_extra_inds = sorted(list(set(user_marked) - expected.wrong_inds))
    
    forgot_to_mark = ""
    marked_extra = ""
    
    for i in forgot_to_mark_inds:
        forgot_to_mark += expected.arr[i - 1] + "\n"
    
    for i in marked_extra_inds:
        marked_extra += expected.arr[i - 1] + "\n"
    
    
    
    return f"""
{"*Вы забыли отметить* \n" + escape_markdown_v2(forgot_to_mark) if forgot_to_mark else ""}
{"*Вы отметили правильные утверждения* \n" + escape_markdown_v2(marked_extra) if marked_extra else ""}
"""