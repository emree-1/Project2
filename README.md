# Cybersecurity Knowledge Base

Application autonome en français pour préparer une revue d’architecture, explorer des scénarios de risque et constituer une checklist traçable. Aucun compte, backend, téléchargement automatique ou installation n’est nécessaire pour l’utiliser.

## Ouvrir et utiliser

1. Téléchargez **`cybersecurity-knowledge-base.html`**, puis ouvrez ce fichier dans un navigateur moderne. Le fichier contient l’interface, le code et le corpus ; il fonctionne hors connexion. Seuls les liens documentaires ouverts volontairement nécessitent Internet.
2. Recherchez un composant ou un terme dans la recherche globale. Ouvrez une fiche puis suivez les liens **composant → risque → recommandation → source** et les associations inverses.
3. Dans **Architecture & cas d’usage**, sélectionnez les composants, renseignez le contexte et, si utile, les flux. Consultez les scénarios applicables, à confirmer et non retenus. Les scénarios ne constituent jamais une preuve de vulnérabilité.
4. Qualifiez les mesures, ajoutez vos notes et cliquez sur **Enregistrer l’évaluation**. Aucun contrôle n’est automatiquement marqué comme mis en œuvre. Exportez la checklist en JSON ou CSV, ou utilisez **Imprimer / PDF**.

Les navigateurs d’entreprise peuvent interdire les pages `file://`. Dans ce cas, servez le même fichier depuis un serveur statique autorisé, par exemple `python -m http.server 8000 --bind 127.0.0.1` depuis le répertoire du projet. Ce serveur est facultatif et ne fait pas partie de l’application.

## Modifier, sauvegarder et restaurer

- Les bibliothèques disposent de fiches et de formulaires de création/modification/suppression. Les sélecteurs relient les enregistrements sans recopier les identifiants. Les dates de revue et statuts documentaires restent visibles. Les correspondances, règles et architectures types sont accessibles dans **Gestion du référentiel**.
- Les catégories et sous-catégories représentent la hiérarchie. Les capacités et questions sont des attributs éditables. Les associations de famille sont des pistes de qualification ; certaines technologies disposent d’associations plus précises.
- Les liens inverses sont calculés : modifiez le composant pour ses risques, le risque pour ses recommandations, et une correspondance pour sa source et sa cible. Une suppression explique les relations affectées et demande une confirmation.
- IndexedDB est utilisé en priorité, puis localStorage si nécessaire. Si les deux sont indisponibles, une bannière indique le **mode session** : exportez impérativement avant de fermer. Le stockage dépend du navigateur, du profil et de l’origine du fichier ; déplacer le fichier peut changer l’accès aux données locales.
- **Exporter la sauvegarde** produit un JSON complet comprenant les bibliothèques, les évaluations enregistrées et l’évaluation en cours modifiée. Conservez plusieurs versions hors du navigateur. L’export de bibliothèque exclut les évaluations ; l’export d’évaluation permet de transporter un seul projet.
- **Importer JSON** valide entièrement le document et affiche une prévisualisation avant confirmation. **Fusionner** conserve les identifiants absents du fichier et remplace les collisions par les données entrantes ; **Remplacer** remplace le périmètre importé. Une bibliothèque importée conserve les évaluations existantes. Une référence manquante bloque l’import sans changement partiel.
- Les exports CSV fournissent les en-têtes et exemples à réutiliser. UTF-8 avec BOM, virgule ou point-virgule, guillemets et retours ligne sont pris en charge. Les listes/objets utilisent du JSON dans les cellules. Les caractères de formule sont neutralisés à l’export ; il n’y a pas de prise en charge `.xlsx`.
- Restaurer le corpus initial conserve les évaluations. Si celles-ci utilisent des identifiants personnalisés absents du corpus, la restauration est refusée pour préserver leur intégrité. Exportez d’abord.

## Architecture

Un unique fichier HTML contient CSS, données JSON et JavaScript vanilla, sans dépendance d’exécution. Les modules logiques sont `SchemaValidator`, `DataStore`, `AppState`, `SearchEngine`, `ApplicabilityEngine` et les fonctions de résolution des relations, rendu et import/export. Le corpus intégré reste séparé de la copie éditable. Les identifiants sont stables et les risques ne sont pas dupliqués dans les composants.

Le schéma est versionné (`schemaVersion: 1`). Les versions inconnues sont refusées explicitement ; une future version devra fournir sa migration. Les règles sont des arbres JSON avec `ALL`, `ANY`, `NOT`, `equals`, `not equals`, `includes`, `excludes`, `in` et `exists`. L’éditeur de règles est un formulaire avancé avec expression JSON : par exemple `{"field":"exposure","op":"equals","value":"Internet"}`. Les champs de contexte autorisés sont proposés dans l’évaluation. Une valeur inconnue conserve un résultat **à confirmer**, y compris sous négation. Plusieurs règles ciblant un même risque sont des alternatives. Les combinaisons d’architecture ajoutent des scénarios quand tous leurs composants sont sélectionnés.

Le contenu importé passe par une validation de types, identifiants, relations, URL HTTPS, structure et profondeur. Le rendu utilise les nœuds texte et les API DOM, sans `innerHTML`, `eval` ni code importé. Les liens sortants sont ouverts avec `noopener noreferrer`. La sauvegarde n’inclut aucune télémétrie.

## Corpus initial et traçabilité

| Objet | Quantité |
|---|---:|
| Composants | 108 |
| Scénarios distincts | 42 |
| Recommandations | 84 |
| Sources | 9 |
| Correspondances documentaires | 126 |
| Correspondances vérifiées | 3 |
| Correspondances à vérifier | 123 |
| Règles contextuelles | 8 |
| Architectures types | 6 |

Domaines : applications/API, données, échanges/SFTP/messagerie, identités, réseau, infrastructure, cloud/SaaS, résilience/opérations et IA. Les notices couvrent OWASP, NIST, ANSSI, CIS, MITRE et CNIL. Cinq notices sont actuellement sans correspondance ; la vue de validation le signale.

**Vérification réalisée le 31 octobre 2026 :** lecture du [document API1:2023 du dépôt officiel OWASP](https://github.com/OWASP/API-Security/blob/master/editions/2023/en/0xa1-broken-object-level-authorization.md), sections « Is the API Vulnerable? » et « How To Prevent ». Les correspondances `MAP-001`, `MAP-002` et `MAP-003` documentent respectivement le scénario d’autorisation objet et les mesures de contrôle serveur et de test. Le test entre tenants est une mise en pratique interne de cette recommandation de test. Les textes intégrés sont des reformulations, pas des citations. L’attribution et les liens officiels sont conservés.

**Les 123 autres correspondances ne sont pas vérifiées.** Elles proposent un rapprochement thématique à contrôler, pas une prescription officielle. Les sections, dates et versions inconnues ne sont pas inventées. Les niveaux Socle / Contextuel / Renforcé sont des classifications internes, sans niveau d’assurance ANSSI/NIST ni obligation réglementaire implicite.

## Validation

Ouvrez **Gestion du référentiel → Diagnostics intégrés**, ou ajoutez `?diagnostic` à l’URL. Les **33 diagnostics** vérifient l’intégrité, les opérateurs ternaires, les relations, les identifiants, la recherche, JSON/CSV, les URL actives, le rendu texte et dix scénarios de revue.

Une suite navigateur reproductible est fournie dans `tests/browser_smoke.py`. Elle utilise Python, Playwright et Chromium **uniquement pour le développement**, jamais pour utiliser l’application :

```sh
python -m pip install playwright
CHROMIUM_PATH=/usr/bin/chromium python tests/browser_smoke.py
```

La suite démarre un serveur HTTP local temporaire sur `127.0.0.1:8765`, utilise un profil de navigateur neuf, et contrôle CRUD, persistance après rechargement, sauvegarde/import avec prévisualisation, rejet atomique d’une URL malveillante, contenu HTML inerte, avertissement sans stockage, rendu à 390 px, génération PDF et absence de requêtes externes. Les captures et le PDF vont dans un répertoire temporaire annoncé par le test.

Validation effectuée sous Chromium dans l’environnement cloud. Le lancement direct en `file://` y est bloqué par politique administrateur et **n’a donc pas été validé**. Les tests ont utilisé le serveur statique local. Une validation manuelle sur les autres navigateurs reste à effectuer.

## Limites et travaux restant à réaliser

- Le corpus atteint 42 risques / 84 mesures, sous les objectifs de 120 / 180. Il doit être enrichi et revu par des spécialistes plutôt que complété artificiellement.
- Vérifier les 123 correspondances restantes, notamment les versions/sections des guides ANSSI et des publications NIST ; approfondir SAML, PKI, cloud natif et les risques spécifiques des produits.
- Les huit règles et les associations initiales constituent un premier moteur explicable, pas un moteur exhaustif de modélisation des menaces. Les flux sont documentés ; ils ne sont pas analysés comme un graphe. La criticité des risques n’est pas calculée automatiquement.
- Les règles complexes utilisent un éditeur JSON validé, pas un constructeur graphique. Les capacités et questions n’ont pas de bibliothèque autonome. La gestion des doublons détecte les titres identiques sans mesure sémantique de similarité.
- Les filtres couvrent domaines, impacts, fonctions de contrôle, organismes et statut des correspondances. Un filtrage croisé simultané par tous les objets n’est pas disponible.
- Les formulaires sont volontairement génériques. La revue ergonomique et d’accessibilité avec des utilisateurs réels et des corpus très volumineux reste à poursuivre.
