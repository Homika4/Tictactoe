from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

grille = [["" for _ in range(3)] for _ in range(3)]
end = False
winner = None

@app.route('/')
def home():
    reset_message = request.args.get('reset_message')
    return render_template("index.html", grille=grille, reset_message=reset_message, end=end, winner=winner)

@app.route('/play', methods=['POST', 'GET'])
def play():
    global end, winner

    row = int(request.form["row"])
    col = int(request.form["col"])

    if grille[row][col] == "":
        # Le joueur joue
        grille[row][col] = "X"

        # Vérifie si le joueur gagne directement
        if check_gagnant("X"):
            winner = "X"
            end = True
        else:
            # Lister les cases vides
            cases_vides = []
            for r in range(3):
                for c in range(3):
                    if grille[r][c] == "":
                        cases_vides.append((r, c))

            # L’ordinateur joue SEULEMENT si des cases sont dispo
            if len(cases_vides) > 0:
                r, c = random.choice(cases_vides)
                grille[r][c] = "O"

                # Vérifie si l’ordinateur gagne
                if check_gagnant("O"):
                    winner = "O"
                    end = True

        # Vérifie match nul
        if not end:
            end = True
            for r in range(3):
                for c in range(3):
                    if grille[r][c] == "":
                        end = False
                        break
                if not end:
                    break
            if end:
                winner = "Egalité"

    return redirect(url_for('home'))

def check_gagnant(symbole):
    # Lignes
    for row in grille:
        if row[0] == row[1] == row[2] == symbole:
            return True
    # Colonnes
    for c in range(3):
        if grille[0][c] == grille[1][c] == grille[2][c] == symbole:
            return True
    # Diagonales
    if grille[0][0] == grille[1][1] == grille[2][2] == symbole:
        return True
    if grille[0][2] == grille[1][1] == grille[2][0] == symbole:
        return True

    return False

@app.route('/reset', methods=['POST', 'GET'])
def reset():
    global end, winner
    for r in range(3):
        for c in range(3):
            grille[r][c] = ""
    end = False
    winner = None
    return redirect(url_for('home', reset_message=1))

if __name__ == "__main__":
    app.run()
