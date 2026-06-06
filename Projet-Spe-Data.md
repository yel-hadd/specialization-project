# EduTrack Analytics : Plateforme d'Analyse de Performance des Étudiants

> **MAROC YNOV CAMPUS** — Projet Spé DATA

---

## 1. Contexte et Objectifs

Le projet **EduTrack Analytics** consiste en la création d'une plateforme Data et Business Intelligence destinée à l'analyse de la performance académique des étudiants au sein d'un établissement d'enseignement supérieur.

L'objectif principal est de permettre à l'administration, aux responsables pédagogiques et aux formateurs de mieux comprendre l'évolution des étudiants à travers l'exploitation de données académiques telles que les notes, les absences, les retards, les modules, les classes et les résultats finaux.

La solution doit permettre d'**importer, nettoyer, analyser et visualiser** les données afin de produire des indicateurs fiables d'aide à la décision. Elle devra également identifier les étudiants en difficulté et proposer des alertes basées sur des règles statistiques ou des modèles prédictifs simples.

> **Objectif principal :** transformer des données académiques brutes en tableaux de bord interactifs, analyses exploitables et indicateurs de suivi pédagogique.

L'accent est mis sur la qualité de l'analyse exploratoire, la précision des calculs statistiques, la conception propre des pipelines de traitement de données, ainsi que la construction d'une interface claire pour la visualisation des résultats.

---

## 2. Exigences Fonctionnelles

### 2.1 Importation et Gestion des Données

- **Import de fichiers :** La plateforme doit permettre l'importation de fichiers CSV ou Excel contenant les notes, absences, retards, informations étudiants, classes et modules.
- **Validation des données :** Le système doit vérifier la présence des colonnes obligatoires, détecter les valeurs manquantes et signaler les erreurs de format.
- **Nettoyage automatique :** Les données doivent être nettoyées avant analyse : suppression des doublons, correction des valeurs incohérentes, normalisation des noms de colonnes et traitement des valeurs nulles.
- **Historique des imports :** Chaque import doit être enregistré avec la date, le nom du fichier, le nombre de lignes traitées et le statut du traitement.

### 2.2 Tableau de Bord Pédagogique

- **Vue globale :** Affichage des indicateurs principaux : moyenne générale, taux de réussite, taux d'absence, nombre d'étudiants à risque et progression globale.
- **Analyse par classe :** Comparaison des performances entre les différentes classes ou groupes.
- **Analyse par module :** Identification des modules les plus réussis, les plus difficiles et ceux présentant un taux d'échec élevé.
- **Analyse individuelle :** Fiche détaillée par étudiant incluant ses notes, absences, évolution, classement et statut de risque.
- **Visualisations interactives :** Graphiques permettant d'analyser les tendances, distributions, moyennes, écarts-types et corrélations.

### 2.3 Analyse et Exploration des Données

- **Statistiques descriptives :** Calcul de la moyenne, médiane, minimum, maximum, variance, écart-type et quartiles pour chaque module.
- **Distribution des notes :** Visualisation de la répartition des notes par module, classe ou période.
- **Corrélations :** Analyse de la relation entre les absences, les retards et les résultats académiques.
- **Détection d'anomalies :** Identification des notes inhabituelles, absences excessives ou variations fortes dans la performance d'un étudiant.
- **Segmentation des étudiants :** Classification des étudiants selon leur niveau : excellent, stable, moyen, fragile ou à risque.

### 2.4 Système d'Alerte et Suivi des Étudiants

- **Détection des étudiants à risque :** Le système doit identifier automatiquement les étudiants ayant une moyenne faible, un taux d'absence élevé ou une baisse significative de performance.
- **Alertes pédagogiques :** Génération d'alertes lorsqu'un étudiant dépasse un seuil critique défini par l'utilisateur.
- **Suivi de progression :** Affichage de l'évolution des performances dans le temps afin de détecter les améliorations ou régressions.
- **Recommandations simples :** Proposition d'actions pédagogiques comme un suivi personnalisé, un rappel d'assiduité ou un renforcement sur certains modules.

---

## 3. Logique Data, Backend et Architecture

La plateforme doit être construite autour d'une architecture claire séparant l'importation des données, leur traitement, leur stockage et leur visualisation.

- **Pipeline de traitement :** Les données importées doivent passer par plusieurs étapes : lecture, validation, nettoyage, transformation, analyse et stockage.
- **Modèle relationnel :** La base de données doit contenir des tables cohérentes pour les étudiants, classes, modules, notes, absences, imports et alertes.
- **Cohérence des données :** Les relations entre les entités doivent être respectées afin d'éviter les incohérences entre étudiants, modules et résultats.
- **Calculs statistiques :** Les indicateurs doivent être calculés de manière fiable côté backend ou via des scripts Python dédiés.
- **Séparation des responsabilités :** Le code doit être organisé en modules distincts : import, nettoyage, analyse, API, authentification et visualisation.

---

## 4. Spécifications Techniques

Le cadre technologique impose l'utilisation d'outils modernes pour la manipulation de données, le développement backend, la visualisation et la persistance.

> ### 🛠️ STACK TECHNIQUE RECOMMANDÉE
>
> - **Langage principal :** Python.
> - **Analyse de données :** Pandas, NumPy.
> - **Visualisation :** Plotly, Matplotlib, Seaborn ou Recharts.
> - **Machine Learning :** Scikit-learn pour les modèles prédictifs simples.
> - **Backend :** FastAPI, Django REST Framework, Flask ou Node.js.
> - **Frontend :** React, Next.js ou Vue 3.
> - **Base de données :** PostgreSQL, MySQL ou SQLite pour une version simplifiée.
> - **Authentification :** JWT ou système de session sécurisé.
> - **Versioning :** GitHub avec README complet.

### 4.1 Contraintes Techniques Obligatoires

- Le projet doit inclure au minimum un pipeline complet d'importation, nettoyage et analyse.
- Les données doivent être stockées dans une base relationnelle.
- Le tableau de bord doit contenir au moins **cinq visualisations** pertinentes.
- Les indicateurs affichés doivent être calculés à partir des données importées et non saisis manuellement.
- Le code doit respecter une structure claire et maintenable.
- Le projet doit contenir un fichier **README** expliquant l'installation, l'exécution et la structure du projet.

---

## 5. Défis Experts

> ### 🎯 BONUS A : MODÈLE PRÉDICTIF DU RISQUE D'ÉCHEC
>
> L'objectif est de construire un modèle capable d'estimer la probabilité qu'un étudiant soit en situation de risque académique.
>
> - **Logique :** Utiliser les notes, absences, retards et progression pour prédire si un étudiant risque d'échouer ou de nécessiter un accompagnement.
> - **Défi Technique :** Préparer les données, choisir les variables pertinentes, entraîner un modèle simple comme une régression logistique, un arbre de décision ou un Random Forest.
> - **Critère d'Excellence :** Le modèle doit être évalué avec des métriques claires : accuracy, precision, recall, F1-score et matrice de confusion.

> ### 🎯 BONUS B : SEGMENTATION AUTOMATIQUE DES PROFILS ÉTUDIANTS
>
> Ce bonus évalue la capacité à utiliser des méthodes non supervisées pour regrouper les étudiants selon leurs comportements académiques.
>
> - **La distinction Data Science :** Implémenter un algorithme de clustering comme K-Means afin d'identifier des groupes d'étudiants : excellents, réguliers, irréguliers, en progression ou à risque.
> - **Défi Technique :** Normaliser les variables, choisir le nombre de clusters et interpréter les groupes obtenus.
> - **Critère d'Excellence :** Les clusters doivent être expliqués clairement dans le rapport et visualisés à travers des graphiques pertinents.

> ### 🎯 BONUS C : GÉNÉRATION AUTOMATIQUE DE RAPPORTS
>
> L'objectif est de générer automatiquement un rapport PDF ou HTML à partir des résultats d'analyse.
>
> - **Logique :** Après import et analyse des données, l'utilisateur peut générer un rapport contenant les KPIs, graphiques, alertes et recommandations.
> - **Défi Technique :** Produire un document structuré avec les résultats calculés dynamiquement.
> - **Critère d'Excellence :** Le rapport doit être lisible, professionnel et exploitable par un responsable pédagogique.

---

## 6. Concepts et Définitions Data

### La Base : Le Dataset Académique

Un dataset académique représente un ensemble de données liées aux étudiants et à leur parcours.

- **Étudiant :** Entité principale contenant les informations d'identification, la classe et les résultats.
- **Module :** Matière ou unité d'enseignement évaluée par une ou plusieurs notes.
- **Note :** Résultat obtenu par un étudiant dans un module donné.
- **Absence :** Indicateur d'assiduité permettant d'analyser son impact sur la performance.

### Indicateurs Pédagogiques

- **Moyenne générale :** Indicateur global de performance d'un étudiant ou d'une classe.
- **Taux de réussite :** Pourcentage d'étudiants ayant obtenu une moyenne supérieure ou égale au seuil de validation.
- **Taux d'absence :** Rapport entre le nombre d'absences et le nombre total de séances.
- **Score de risque :** Indicateur calculé à partir de plusieurs variables afin d'évaluer la situation académique d'un étudiant.

### Analyse Exploratoire

L'analyse exploratoire des données, ou **EDA**, consiste à examiner les données avant toute modélisation. Elle permet de comprendre leur structure, détecter les erreurs, observer les tendances et formuler des hypothèses.

- **Distribution :** Répartition des valeurs d'une variable comme les notes.
- **Corrélation :** Mesure de relation entre deux variables, par exemple les absences et la moyenne.
- **Outlier :** Valeur inhabituelle pouvant indiquer une erreur ou un cas particulier.

---

## 7. Livrables Attendus

1. **Rapport Technique :** Incluant la description du projet, le schéma de la base de données, les choix techniques, les étapes du pipeline Data, l'analyse exploratoire et les résultats obtenus.
2. **Notebook d'Analyse :** Fichier Jupyter Notebook présentant le nettoyage des données, les visualisations, les statistiques et éventuellement les modèles prédictifs.
3. **Dépôt Code Source :** Lien GitHub contenant le frontend, le backend, les scripts Data, le README et les instructions d'installation.
4. **Application Fonctionnelle :** URL d'accès ou vidéo de démonstration montrant l'importation des données, le tableau de bord et les analyses.
5. **Base de Données :** Script SQL ou fichier de migration permettant de recréer la structure de la base.
6. **Soutenance :** Présentation orale expliquant la problématique, l'architecture, les choix Data, les visualisations, les résultats et une démonstration live.

---

## 8. Critères d'Évaluation

- **Qualité de l'analyse des données :** pertinence du nettoyage, richesse de l'exploration et justesse des interprétations.
- **Pertinence des indicateurs :** choix des KPIs et capacité à répondre à une problématique pédagogique réelle.
- **Qualité technique :** architecture, organisation du code, sécurité, base de données et maintenabilité.
- **Qualité des visualisations :** clarté des graphiques, interactivité et lisibilité du dashboard.
- **Fonctionnalité de l'application :** capacité à importer des données, afficher les analyses et générer des résultats fiables.
- **Présentation et professionnalisme :** qualité du rapport, démonstration, explication des choix et maîtrise du sujet.
