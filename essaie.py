import streamlit as st
import random

st.set_page_config(page_title="Morpion IA", page_icon="🤖", layout="centered")

st.title("⭕❌ Morpion contre l'IA")
st.write("Tu joues ❌ et l'IA joue ⭕. Essaie de gagner !")

# 1️⃣ Initialisation
if "grid" not in st.session_state:
    st.session_state.grid = [""] * 9
if "winner" not in st.session_state:
    st.session_state.winner = None
if "player_turn" not in st.session_state:
    st.session_state.player_turn = True  # le joueur commence

# 2️⃣ Vérification gagnant
def check_winner():
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # lignes
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colonnes
        (0, 4, 8), (2, 4, 6)              # diagonales
    ]
    for a, b, c in wins:
        if st.session_state.grid[a] == st.session_state.grid[b] == st.session_state.grid[c] != "":
            return st.session_state.grid[a]
    if "" not in st.session_state.grid:
        return "Égalité"
    return None

# 3️⃣ Coup IA
def ia_move():
    empty = [i for i, v in enumerate(st.session_state.grid) if v == ""]
    if not empty:
        return
    # IA peut gagner ?
    for i in empty:
        st.session_state.grid[i] = "⭕"
        if check_winner() == "⭕":
            return
        st.session_state.grid[i] = ""
    # Bloquer joueur ?
    for i in empty:
        st.session_state.grid[i] = "❌"
        if check_winner() == "❌":
            st.session_state.grid[i] = "⭕"
            return
        st.session_state.grid[i] = ""
    # Sinon coup aléatoire
    choice = random.choice(empty)
    st.session_state.grid[choice] = "⭕"

# 4️⃣ Affichage grille
cols = st.columns(3)
for i in range(9):
    if st.session_state.grid[i] == "":
        if st.session_state.player_turn and not st.session_state.winner:
            if cols[i % 3].button(" ", key=f"case{i}"):
                st.session_state.grid[i] = "❌"
                st.session_state.winner = check_winner()
                st.session_state.player_turn = False
                if not st.session_state.winner:
                    ia_move()
                    st.session_state.winner = check_winner()
                    st.session_state.player_turn = True
        else:
            cols[i % 3].button(" ", key=f"case{i}")
    else:
        cols[i % 3].button(st.session_state.grid[i], key=f"case{i}")

# 5️⃣ Affichage statut
if st.session_state.winner:
    if st.session_state.winner == "Égalité":
        st.warning("🤝 Match nul !")
    elif st.session_state.winner == "❌":
        st.success("🏆 Bravo, tu as gagné !")
    else:
        st.error("💀 L'IA a gagné !")
else:
    if st.session_state.player_turn:
        st.info("C'est ton tour.")
    else:
        st.info("L'IA joue...")

# 6️⃣ Rejouer
if st.button("🔄 Rejouer"):
    st.session_state.grid = [""] * 9
    st.session_state.winner = None
    st.session_state.player_turn = True
    st.rerun()
