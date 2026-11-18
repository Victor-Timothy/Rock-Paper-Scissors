import streamlit as st
import random

# -----------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title = "Rock Paper Scissors Game",
    page_icon = "✊",
    initial_sidebar_state="auto",
    layout="centered",
    menu_items = {
        "Get Help": "https://docs.streamlit.io",
        "Report a bug": "mailto:ikennatimothy275@gmail.com",
        "About": "### Rock Paper Scissors Game\nBuilt as a Python Streamlit Project for The Fhenix IT Class.",
    }
)

# -----------------------------------
# 2. GAME TITLE
# -----------------------------------

st.title("✊ Rock, Paper, Scissors ✋")
st.write("Welcome! Challenge the computer in a game of Rock, Paper, Scissors.")

st.divider()

# -----------------------------------
# 3. INITIALIZE SESSION STATE
# -----------------------------------

if "user_score" not in st.session_state:
    st.session_state.user_score = 0

if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0

if "draws" not in st.session_state:
    st.session_state.draws = 0

if "user_choice" not in st.session_state:
    st.session_state.user_choice = None

if "computer_choice" not in st.session_state:
    st.session_state.computer_choice = None

if "result" not in st.session_state:
    st.session_state.result = None

defaults = {
    "user_score": 0,
    "computer_score": 0,
    "draws": 0,
    "user_choice": None,
    "computer_choice": None,
    "result": None,
    "history": [],
    "game_over": False,
    "rounds_played": 0
}


for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -----------------------------------
# 4. DEFINE GAME OPTIONS
# -----------------------------------

choices = ["Rock", "Paper", "Scissors"]

emoji = {
    "Rock": "✊",
    "Paper": "✋",
    "Scissors": "✌️"
}

# -----------------------------------
# 5. CREATE THE GAME LOGIC
# -----------------------------------

def determine_winner(user, computer):
    if user == computer:
        return "Draw"
    elif user == "Rock" and computer == "Scissors":
        return "You Win!"
    elif user == "Paper" and computer == "Rock":
        return "You Win!"
    elif user == "Scissors" and computer == "Paper":
        return "You Win!"
    else:
        return "Computer Wins!"

def reset_game():

    for key in defaults:
        st.session_state[key] = defaults[key]


def play_game(user_choice):

    computer_choice = random.choice(choices)

    result = determine_winner(user_choice, computer_choice)

    st.session_state.user_choice = user_choice
    st.session_state.computer_choice = computer_choice
    st.session_state.result = result
    st.session_state.rounds_played += 1

    if result == "You Win!":
        st.session_state.user_score += 1

    elif result == "Computer Wins!":
        st.session_state.computer_score += 1

    else:
        st.session_state.draws += 1

    st.session_state.history.append({
        "Round": st.session_state.rounds_played,
        "Your Choice": user_choice,
        "Computer Choice": computer_choice,
        "Result": result
    })

    # Check whether the selected game mode has ended
    target = st.session_state.target_score

    if (
        st.session_state.user_score >= target
        or st.session_state.computer_score >= target
    ):
        st.session_state.game_over = True


# -----------------------------------
# 6. GAME MODE SELECTION
# -----------------------------------

st.subheader("🎮 Select Game Mode")

game_mode = st.selectbox(
    "Choose how many rounds you want to play:",
    ["Unlimited", "Best of 5", "Best of 10"]
)

if game_mode == "Best of 5":
    target_score = 3

elif game_mode == "Best of 10":
    target_score = 6

else:
    target_score = None

# Store the target score
if "target_score" not in st.session_state:
    st.session_state.target_score = target_score

if st.session_state.target_score != target_score:
    reset_game()
    st.session_state.target_score = target_score

st.divider()

#-----------------------------------
# 7. DISPLAY SCOREBOARD
# -----------------------------------

st.subheader("🏆 Scoreboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Your Score", st.session_state.user_score)

with col2:
    st.metric("Computer", st.session_state.computer_score)

with col3:
    st.metric("Draws", st.session_state.draws)

st.write(f"**Rounds Played:** {st.session_state.rounds_played}")

if target_score:
    st.progress(
        min(
            max(
                st.session_state.user_score,
                st.session_state.computer_score
            ) / target_score,
            1.0
        )
    )

st.divider()

# -----------------------------------
# 8. USER SELECTS AN OPTION
# -----------------------------------

st.subheader("🎯 Make Your Choice")

if not st.session_state.game_over:

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✊ Rock", use_container_width=True):
            play_game("Rock")

    with col2:
        if st.button("✋ Paper", use_container_width=True):
            play_game("Paper")

    with col3:
        if st.button("✌️ Scissors", use_container_width=True):
            play_game("Scissors")

else:
    st.info("This game has ended! Start a new game to play again.")

# -----------------------------------
# 9. DISPLAY GAME RESULTS
# -----------------------------------

if st.session_state.result:

    st.divider()
    st.subheader("📢 Round Result")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Your Choice**")
        st.title(emoji[st.session_state.user_choice])
        st.write(st.session_state.user_choice)

    with col2:
        st.write("**Computer's Choice**")
        st.title(emoji[st.session_state.computer_choice])
        st.write(st.session_state.computer_choice)

    if st.session_state.result == "You Win!":
        st.success("🎉 Congratulations! You won this round!")
        st.balloons()

    elif st.session_state.result == "Computer Wins!":
        st.error("😢 The computer won this round. Try again!")

    else:
        st.warning("🤝 It's a draw! Nobody wins this round.")

# -----------------------------------
# 10. FINAL GAME RESULT
# -----------------------------------

if st.session_state.game_over:

    st.divider()
    st.subheader("🏆 Final Game Result")

    if st.session_state.user_score > st.session_state.computer_score:
        st.success("🎉 Congratulations! YOU WON THE GAME!")
        st.balloons()

    else:
        st.error("💻 The computer won the game! Better luck next time.")

# -----------------------------------
# 11. GAME HISTORY
# ----------------------------------

st.divider()
st.subheader("📜 Game History")

if st.session_state.history:

    st.dataframe(
        st.session_state.history,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No games played yet. Make your first move!")

# -----------------------------------
# 12. GAME STATISTICS
# -----------------------------------

st.divider()
st.subheader("📜 Game History")

if st.session_state.history:

    st.dataframe(
        st.session_state.history,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No games played yet. Make your first move!")

# -----------------------------------
# 12. GAME STATISTICS
# -----------------------------------

st.divider()
st.subheader("📊 Game Statistics")

total_games = st.session_state.rounds_played

if total_games > 0:

    win_rate = (
        st.session_state.user_score / total_games
    ) * 100

    loss_rate = (
        st.session_state.computer_score / total_games
    ) * 100

    draw_rate = (
        st.session_state.draws / total_games
    ) * 100

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Win Rate", f"{win_rate:.1f}%")

    with col2:
        st.metric("Loss Rate", f"{loss_rate:.1f}%")

    with col3:
        st.metric("Draw Rate", f"{draw_rate:.1f}%")

else:
    st.write("Statistics will appear after your first round.")

# -----------------------------------
# 13. RESET GAME
# -----------------------------------

st.divider()

if st.button("🔄 Restart Game", use_container_width=True):
    reset_game()
    st.rerun()

# -----------------------------------
# 14. FOOTER
# -----------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center;">
        <p>✊ Rock, Paper, Scissors ✋</p>
        <p>Built with ❤️ using Python and Streamlit</p>
        <p><b>The Fhenix IT Class</b></p>
    </div>
    """,
    unsafe_allow_html=True
)