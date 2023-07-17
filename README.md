# xNBTD

xNBTD est une application de gestion pour entreprise de livraison.
Elle facilite la gestion des tournées et des plannings.

## Exigences

- Python 3.x
- Django 3.x
- Un serveur web pour héberger l'application

## Installation

Pour installer xNBTD, suivez ces étapes (pour les systèmes Linux) :

1. Créez le répertoire : `mkdir /opt/eldertek`
2. Accédez au répertoire : `cd /opt/eldertek`
3. Clonez le dépôt : `git clone https://github.com/eldertek/xnbtd && cd xnbtd`
4. Installez Poetry : `make install-poetry`
5. Installez xnbtd : `make install`
6. Voilà ! Vous devez maintenant déployer l'application.

**Vous devez ensuite la déployer, voir ci-dessous.**
## Déploiement

Pour déployer xNBTD dans un environnement de production, suivez ces étapes :

1. Installez un serveur web prêt pour la production, tel que Nginx ou Apache.
2. Configurez le serveur web pour servir l'application Django.
3. Utilisez un gestionnaire de processus, tel que Gunicorn ou uWSGI, pour exécuter l'application Django.

## Contribution

Nous accueillons les contributions à xNBTD ! Si vous souhaitez contribuer, veuillez suivre ces étapes :

1. Fork le dépôt
2. Créez une nouvelle branche pour vos modifications
3. Effectuez vos modifications et poussez-les vers votre fork
4. Soumettez une pull request pour examen

## Support

Si vous avez besoin d'aide avec xNBTD, veuillez ouvrir une issue sur le dépôt. Nous ferons de notre mieux pour vous aider.

Droits d'auteur (c) 2023 André Théo LAURET - Tous droits réservés
