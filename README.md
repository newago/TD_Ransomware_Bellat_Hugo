# TD_Ransomware_Bellat_Hugo

Question 1 :
Il s'agit d'un chiffrement XOR. Il n'est pas solide car présente des faiblesses aux attaques brute force et analyse de fréquence. En outre, la clé présente une longueur fix est et répétitive. L'algorithme n'en est donc que plus sensible aux attaques.

Question 2 :
On ne hache pas la clé et le sel directement car on cherche à obtenir une clé unique dérivée de ce sel et de ce hash. Le HMAC permet de sécuriser la génération de la clé dérivée en utilisant un hachage sécurisé.

