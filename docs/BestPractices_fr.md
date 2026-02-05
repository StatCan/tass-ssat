# Méthodes standards

Voici nos méthodes standards décidé par notre équipe pour harmoniser notre
travail et réduire des erreurs. Nos méthodes peuvent toujours être modifiée 
suite à une discussion.

Si vous travaillez différement, assurez-vous que vos contributions 
possèdent les mêmes qualités que les contributions résultants des méthodes 
ci-bas. S'il est nécessaire de diverger de ces méthodes pour des raisons 
d'affaires, veuillez les documenter dans l'endroit approprié et 
communiquer avec l'équipe.

## Style de programmation

Pour le code Python, nous suivons PEP-8 et utilisons Flake 8 pour la 
validation.

## Tabs vs espaces

Les espaces gagnent.

## Éditeurs de texte / IDE

Utilisez l'outil de votre choix tant qu'il produit des fichiers textes 
encodé correctement.

## Noms des branhces

Les branches doivent être nommé "nombre-type-résumé". Par exemple: 
2-feature-click_action.

Les types présentement acceptés sont : 
- feature
- doc
- bugfix

Des types supplémentaires peuvent être ajouté avec le temps.

Le résumé devrait être une brève explication de quelques mots. Ceux-ci 
devraient être séparé par "_".

## Fusion des branches Git (Git merge)

Des changements de code ne devraient jamais être fait directement 
sur la branche "main". Les changements doivent être fait sur une 
autre branche, et ensuite fusionner à la branche "main" après 
avoir été révisé et validé.

Lorsqu'un "pull request" est évalué, la personne qui révise doit 
s'assurer de regarder le code source, exécuter les tests, et valider 
le format du code avec Flake8. Les problèmes ou suggestions peuvent 
être envoyé à l'auteur original.

Un "pull request" doit être révisé par au moins une personne. Si la 
composition de l'équipe change, le nombre peut être révisé.
