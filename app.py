import sqlite3
from flask import Flask, jsonify, request
from auth import utilisateur_connecte

app = Flask(__name__)
DB = "notes.db"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            etudiant TEXT NOT NULL,
            module TEXT NOT NULL,
            note REAL NOT NULL
        )
        """
    )
    cur.execute("SELECT COUNT(*) FROM notes")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO notes (etudiant, module, note) VALUES (?, ?, ?)",
            [
                ("Amina", "DevSecOps", 15),
                ("Youssef", "Java", 14),
            ],
        )
    con.commit()
    con.close()

@app.route("/", methods=["GET"])
def accueil():
    return jsonify({"message": "Service des notes des étudiants"}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/notes", methods=["GET"])
def lire_notes():
    etudiant = request.args.get("etudiant")
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if etudiant:
        # Requête paramétrée pour éviter l'injection SQL (S1)[cite: 5]
        cur.execute("SELECT * FROM notes WHERE etudiant = ?", (etudiant,))
    else:
        cur.execute("SELECT * FROM notes")
    lignes = [dict(ligne) for ligne in cur.fetchall()]
    con.close()
    return jsonify(lignes)

# Modification d'une note par l'enseignant (Version corrigée et sécurisée)
@app.route("/notes/<int:note_id>", methods=["PUT"])
def modifier_note(note_id):
    # 1. Authentification obligatoire (S2)[cite: 3, 5]
    utilisateur = utilisateur_connecte()
    if utilisateur is None:
        return jsonify({"erreur": "Authentification requise"}), 401

    # 2. Vérification du rôle enseignant (S3)[cite: 3, 5]
    if utilisateur.get("role") != "enseignant":
        return jsonify({"erreur": "Accès interdit"}), 403

    # 3. Validation stricte de la note : nombre entre 0 et 20 (S5)[cite: 3, 5]
    donnees = request.get_json(silent=True) or {}
    nouvelle_note = donnees.get("note")
    if (
        nouvelle_note is None
        or isinstance(nouvelle_note, bool)
        or not isinstance(nouvelle_note, (int, float))
        or not (0 <= nouvelle_note <= 20)
    ):
        return jsonify({"erreur": "Note invalide (doit être un nombre entre 0 et 20)"}), 400

    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()

        # 4. Vérification que l'enseignant est responsable du module de cette note (S4)[cite: 3, 5]
        cur.execute("SELECT module FROM notes WHERE id = ?", (note_id,))
        ligne = cur.fetchone()
        if ligne is None:
            con.close()
            return jsonify({"erreur": "Note introuvable"}), 404

        if utilisateur.get("module") != ligne[0]:
            con.close()
            return jsonify({"erreur": "Module non autorisé"}), 403

        # 5. Mise à jour sécurisée via une requête SQL paramétrée (S6)[cite: 5]
        cur.execute("UPDATE notes SET note = ? WHERE id = ?", (nouvelle_note, note_id))
        con.commit()
        con.close()
        return jsonify({"message": "Note modifiée avec succès"}), 200

    except sqlite3.Error:
        # 6. Gestion d'erreur sans fuite de détails techniques (S7)[cite: 5, 6]
        return jsonify({"erreur": "Erreur interne du serveur"}), 500

if __name__ == "__main__":
    init_db()
    app.run(port=5000)