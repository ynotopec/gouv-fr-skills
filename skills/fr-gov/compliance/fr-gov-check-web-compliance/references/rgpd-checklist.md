# Checklist RGPD — application web de l'État

Sources : règlement (UE) 2016/679 (RGPD), loi n° 78-17 du 6 janvier 1978 modifiée
(articles 82 et suivants pour les traceurs), doctrine CNIL. Relevé le 2026-10-22.
Les numéros d'articles sont donnés pour que chaque case puisse être opposée dans
une décision d'homologation ou une mise en demeure.

## Traitements

- [ ] **Base légale identifiée pour chaque traitement** (art. 6) — et non « le service est public »
- [ ] **Finalités déterminées, explicites et légitimes** (art. 5.1.b), écrites, pas déduites du code
- [ ] **Minimisation** : chaque donnée collectée est nécessaire à la finalité (art. 5.1.c) — un champ
      « civilité » ou « date de naissance » non utilisé est un manquement
- [ ] **Durées de conservation définies et appliquées techniquement** (art. 5.1.e), pas seulement documentées
- [ ] **Exactitude** : mécanisme de mise à jour et de rectification (art. 5.1.d)
- [ ] **Registre des activités de traitement** tenu et à jour (art. 30)
- [ ] **AIPD** réalisée pour tout traitement à risque élevé (art. 35) — profilage, données de santé,
      surveillance systématique, croisement de fichiers

## Personnes concernées

- [ ] **Information délivrée** au moment de la collecte : finalité, base légale, destinataires,
      durée, droits, DPO (art. 13 et 14)
- [ ] **Droits exerçables en ligne** : accès (art. 15), rectification (art. 16), effacement (art. 17),
      limitation (art. 18), opposition (art. 21), portabilité (art. 20)
- [ ] **Délai de réponse ≤ 1 mois** (art. 12.3), avec trace de la demande et de la réponse
- [ ] **DPO** désigné si requis, coordonnées publiées (art. 37, art. 13.1.b)
- [ ] **Aucune décision entièrement automatisée** produisant un effet significatif sans garanties
      (art. 22), ou droit d'obtenir une intervention humaine explicite

## Sous-traitance et transferts

- [ ] **Contrat de sous-traitance** avec chaque prestataire traitant des données (art. 28) :
      instructions, confidentialité, sécurité, sort des données en fin de contrat, sous-traitants ultérieurs
- [ ] **Transferts hors UE encadrés** (chapitre V) : décision d'adéquation, clauses contractuelles
      types ou mesures supplémentaires — un hébergement « cloud » non localisé n'est pas un transfert documenté
- [ ] **Si le service appelle un LLM ou un service tiers** : données personnelles absentes des prompts,
      ou sous-traitance et base légale établies (art. 28)

## Sécurité et incidents

- [ ] **Chiffrement au repos et en transit** des données sensibles, pseudonymisation quand possible (art. 32)
- [ ] **Contrôle d'accès** nominatif, moindre privilège, revue périodique des habilitations (art. 32)
- [ ] **Journalisation** des accès aux données personnelles, conservation et intégrité des journaux (art. 32)
- [ ] **Procédure de violation de données** écrite, avec notification CNIL sous 72 h (art. 33)
- [ ] **Registre des violations** tenu, même pour celles non notifiées (art. 33.5)
- [ ] **Aucune donnée réelle en environnement de test** : jeux synthétiques (art. 5.1.f, 32) —
      voir la règle « dataset de test synthétique » de `fr-gov-secure-coding-rules`

## Traceurs et cookies

- [ ] **Aucun traceur non essentiel avant consentement** (art. 82 loi 78-17) — mesure, publicité,
      réseaux sociaux, A/B testing inclus
- [ ] **Refus aussi simple que l'acceptation**, pas de case pré-cochée, pas de consentement par
      simple poursuite de navigation (doctrine CNIL)
- [ ] **Preuve du consentement conservée** et **horodatée**, avec la version du bandeau affiché
- [ ] **Durée de conservation du choix ≤ 13 mois** (recommandation CNIL), re-sollicitation au-delà
- [ ] **Finalité de chaque traceur documentée**, y compris ceux déposés par les composants DSFR
      (gestion opérationnelle : skill `fr-gov-configure-cookie-consent`)

## Ce que cette checklist ne fait pas

Elle ne remplace ni le registre, ni l'AIPD, ni la déclaration d'accessibilité. Une case cochée sans
pièce jointe (capture, extrait de code, décision) est une affirmation, pas une preuve : c'est le
rôle de `fr-gov-audit-app-compliance` de produire les preuves et de qualifier les écarts.
