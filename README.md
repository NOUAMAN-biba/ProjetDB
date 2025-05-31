# 🏨 Système de Réservation Hôtelière

## Description
Application web développée avec Streamlit et SQLite pour la gestion des réservations hôtelières dans le cadre du projet de Base de Données - Licence MIP S4 2025.

## Fonctionnalités

### 📋 Consultation
- **Liste des réservations** : Affichage de toutes les réservations avec détails client et hôtel
- **Liste des clients** : Consultation de tous les clients enregistrés
- **Chambres disponibles** : Recherche de chambres libres pour une période donnée

### ➕ Gestion
- **Ajouter un client** : Formulaire d'ajout de nouveaux clients
- **Nouvelle réservation** : Création de réservations avec vérification de disponibilité


## Structure du Projet

```
ProjetDB/
├── Projet_Hotel.py                 # Application Streamlit principale
├── README.md             # Ce fichier
├── Projet_Hotel_BD.db  # Base de données SQLite (créée automatiquement)
└── Requêtes en Algèbre Relationnelle.pdf
```

## Base de Données

### Tables principales
- **Hotel** : Informations sur les hôtels
- **Client** : Données des clients
- **Chambre** : Détails des chambres
- **Reservation** : Réservations effectuées
- **Type_Chambre** : Types de chambres disponibles
- **Prestation** : Services proposés
- **Evaluation** : Évaluations des séjours

### Données de test
L'application initialise automatiquement la base avec des données de test incluant :
- 2 hôtels (Paris, Lyon)
- 5 clients
- 8 chambres
- Plusieurs réservations d'exemple

## Utilisation

### Navigation
Utilisez le menu latéral pour naviguer entre les différentes sections :

1. **🏠 Accueil** : Vue d'ensemble avec statistiques
2. **📋 Réservations** : Liste complète des réservations
3. **👥 Clients** : Annuaire des clients
4. **🏠 Chambres Disponibles** : Recherche par période
5. **➕ Ajouter Client** : Formulaire d'ajout
6. **📅 Nouvelle Réservation** : Processus de réservation

### Processus de Réservation
1. Sélectionner un client existant
2. Choisir les dates d'arrivée et de départ
3. Vérifier la disponibilité des chambres
4. Sélectionner une chambre parmi celles disponibles
5. Confirmer la réservation

## Fonctionnalités Techniques

### Sécurité
- Validation des données d'entrée
- Gestion des erreurs SQL
- Contraintes d'intégrité respectées

### Performance
- Requêtes optimisées avec jointures appropriées
- Index sur les clés étrangères
- Interface responsive

### Ergonomie
- Interface intuitive avec icônes
- Messages de feedback utilisateur
- Validation des formulaires
- Affichage des statistiques en temps réel

## Requêtes SQL Implémentées

L'application implémente toutes les requêtes demandées dans le projet :

1. **Liste des réservations** avec nom client et ville hôtel
2. **Clients parisiens** avec filtrage automatique
3. **Nombre de réservations par client** avec statistiques
4. **Nombre de chambres par type** avec regroupement
5. **Chambres disponibles** pour période donnée avec exclusion des réservées

## Technologies Utilisées

- **Frontend** : Streamlit (interface web)
- **Backend** : Python 3.8+
- **Base de données** : SQLite (développement) / MySQL (production)
- **Visualisation** : Pandas DataFrames
- **Styling** : CSS intégré Streamlit

## Auteur

Projet réalisé dans le cadre du cours de Base de Données - Licence MIP S4 2025  
Professeur : Pr. J.ZAHIR

## Support

Pour toute question ou problème :
1. Vérifiez que toutes les dépendances sont installées
2. Assurez-vous que Python 3.8+ est utilisé
3. Consultez les logs dans le terminal Streamlit