# TD_Ransomware_Bellat_Hugo

Question 1 :
Il s'agit d'un chiffrement XOR. Il n'est pas solide car présente des faiblesses aux attaques brute force et analyse de fréquence. En outre, la clé présente une longueur fix est et répétitive. L'algorithme n'en est donc que plus sensible aux attaques.

Question 2 :
On ne hache pas la clé et le sel directement car on cherche à obtenir une clé unique dérivée de ce sel et de ce hash. Le HMAC permet de sécuriser la génération de la clé dérivée en utilisant un hachage sécurisé.

Question 3 :
Vérifier qu'un fichier token.bin n'existe pas déjà permet d'éviter d'écraser des données s'il y a eu une installation préalable par exemple (alors il y aurait déjà un fichier créé et l'écraser pourrait causer la perte de données importantes).

Question 4 :
Pour vérifier que la clé est la bonne, on déchiffre une partie d'un fichier avec et si le résultat est cohérent (si il ressemble à du texte lisible), c'est qu'on a la bonne clé. Sinon, il faut signaler que la clé est incorrecte.