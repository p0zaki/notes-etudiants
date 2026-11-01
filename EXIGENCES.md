# Exigences de sécurité de l'application des notes

| # | Exigence : « Le système doit... » | Vérification | Étape du SDLC | Test |
|---|---|---|---|---|
| 1 | Le système doit résister à l'injection SQL lors de la recherche d'un étudiant. | Test automatisé + SAST | Développement / Test | S1 |
| 2 | Le système doit refuser toute modification de note à un utilisateur non identifié (réponse 401). | Test automatisé | Conception / Test | S2 |
| 3 | Le système doit interdire aux étudiants de modifier une note (réponse 403). | Test automatisé | Conception / Test | S3 |
| 4 | Le système doit interdire à un enseignant de modifier les notes d'un autre module que le sien (réponse 403). | Test automatisé | Conception / Test | S4 |
| 5 | Le système doit vérifier que la note reçue est un nombre compris entre 0 et 20 (réponse 400 sinon). | Test automatisé | Développement / Test | S5 |
| 6 | Le système doit autoriser l'enseignant responsable du module à modifier la note de son étudiant (réponse 200). | Test automatisé | Test | S6 |
| 7 | Le système ne doit afficher aucun détail technique en cas d'erreur interne (réponse 500 générique). | Test automatisé | Développement / Test | S7 |