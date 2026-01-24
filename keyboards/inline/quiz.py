from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def grades_keyboard():
    buttons = []
    # Grades 1-11
    row = []
    for i in range(1, 12):
        row.append(InlineKeyboardButton(text=f"{i}-sinf", callback_data=f"grade:{i}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def answers_keyboard(current_index, options):
    buttons = []
    for i, opt in enumerate(options):
        buttons.append([InlineKeyboardButton(text=opt, callback_data=f"ans:{current_index}:{i}")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
