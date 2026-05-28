# Processus de publication

L'équipe garde la documentation de noter outil à jour avec chaque 
publication de l'outil TASS-SSAT.

## Projet git

L'application peut être téléchargé à partir de la section 
"[releases](https://github.com/StatCan/tass-ssat/releases)" du 
projet git.

## Étapes

Pour publier l'outil, il faut suivre les étapes décrites plus bas.

1) Un billet git nommé "Release X.Y.Z" doit être créé, ainsi qu'une branche.
2) Le commit git approprié doit être nommé "vX.Y.Z-RC1".
3) Tous les tests doivent être exécutés et le résultat doit être documenté.
4) Si des erreurs sont identifiées, on créer des billets git pour les 
documentés et on doit décidé si les erreurs nécessite de retarder la
publication de la nouvelle version. Si c'est le cas, on corrige les erreurs et
on répète l'étape 2 en incrémentant le numéro du RC.
5) Renommez le commit "vX.Y.Z-RC#" à "vX.Y.Z".
6) Allez à la section "Releases" et créer une nouvelle entrée avec le nom "vX.Y.Z".
7) Fusionnez la branche de publication à main et fermer le billet de publication.
8) Annoncez la nouvelle version tel que nécessaire. 

Ce processus nécessite aux moins deux personnes de l'équipe de 
développement. Idéalement, l'équipe au complet participe à la 
publication d'une nouvelle version.

## Nettoyage post-publication

Suite à la publication d'une nouvelle version de TASS-SSAT, tout 
le monde devrait prendre le temps de faire du nettoyage des branches 
et billets git pour s'assurer que seulement ce qui est encore valide 
est présent.
