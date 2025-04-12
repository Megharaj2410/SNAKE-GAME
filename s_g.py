import streamlit as st
import random
import time

# Game Config
GRID_SIZE = 20
CELL_SIZE = 20
INITIAL_SNAKE_LENGTH = 3
MOVE_DELAY = 0.2  # seconds

# Initialize game state
if "snake" not in st.session_state:
    st.session_state.snake = [(5, 5), (4, 5), (3, 5)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    st.session_state.score = 0
    st.session_state.game_over = False

# Move logic
def move_snake():
    head_x, head_y = st.session_state.snake[0]
    dir_map = {
        "UP": (head_x, head_y - 1),
        "DOWN": (head_x, head_y + 1),
        "LEFT": (head_x - 1, head_y),
        "RIGHT": (head_x + 1, head_y),
    }
    new_head = dir_map[st.session_state.direction]

    # Collision detection
    if (
        new_head in st.session_state.snake
        or new_head[0] < 0
        or new_head[0] >= GRID_SIZE
        or new_head[1] < 0
        or new_head[1] >= GRID_SIZE
    ):
        st.session_state.game_over = True
        return

    st.session_state.snake.insert(0, new_head)

    # Eating food
    if new_head == st.session_state.food:
        st.session_state.score += 1
        while True:
            new_food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if new_food not in st.session_state.snake:
                st.session_state.food = new_food
                break
    else:
        st.session_state.snake.pop()

# UI Layout
st.title("🐍 Snake Game with Streamlit")
st.write(f"Score: {st.session_state.score}")

# Controls
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Left") and st.session_state.direction != "RIGHT":
        st.session_state.direction = "LEFT"
with col2:
    if st.button("⬆️ Up") and st.session_state.direction != "DOWN":
        st.session_state.direction = "UP"
    if st.button("⬇️ Down") and st.session_state.direction != "UP":
        st.session_state.direction = "DOWN"
with col3:
    if st.button("➡️ Right") and st.session_state.direction != "LEFT":
        st.session_state.direction = "RIGHT"

# Game rendering
canvas = [["⬛" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

for x, y in st.session_state.snake:
    canvas[y][x] = "🟩"
food_x, food_y = st.session_state.food
canvas[food_y][food_x] = "🍎"

game_area = "\n".join(["".join(row) for row in canvas])
st.text(game_area)

# Game loop
if not st.session_state.game_over:
    move_snake()
    time.sleep(MOVE_DELAY)
    st.experimental_rerun()
else:
    st.error("💀 Game Over!")
    if st.button("🔁 Restart"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
