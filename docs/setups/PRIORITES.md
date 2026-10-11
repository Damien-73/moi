# Ordre de test des setups

Classement fait sur les preuves publiées et sur la possibilité de définir le setup de façon
déterministe. Il ne promet rien : il dit seulement où le hasard a le moins de chances de gagner.
Chaque setup est testé seul, avec la même règle : signal uniquement sur bougie de validation clôturée.

| # | Setup | Validation (bougie clôturée) | Preuves publiées sur le forex |
|---|---|---|---|
| 1 | Zone à zone (support / résistance) | clôture de rejet hors de la zone | Osler (2000, 2003, Fed de New York) : les niveaux S/R ont un pouvoir prédictif intraday. Code prêt. |
| 2 | Suivi de tendance : cassure de canal (Donchian) D1/H4 | clôture au-delà du plus haut / plus bas de N bougies | Moskowitz, Ooi, Pedersen (2012) : momentum présent sur les devises. Neely, Weller, Ulrich (2009) : gains des règles techniques en baisse depuis les années 1990. |
| 3 | Épaule-tête-épaule (et inverse) | clôture au-delà de la ligne de cou | Osler & Chang (1995) : rentable sur certaines devises, 1973–1994. Ancien, à confirmer. |
| 4 | Range (rebond sur les bornes) | clôture de rejet sur une borne du range | Proche du setup 1, donc testé ensuite. |
| 5 | Divergence RSI | clôture confirmant le pivot de la divergence | À ma connaissance, aucune étude sérieuse ne montre un avantage sur le forex après coûts. |
| 6 | Figures de chandeliers (marteau, avalement…) | clôture de la bougie suivante dans le sens attendu | Plutôt négatif : Marshall, Young, Rose (2006), aucun gain mesuré (actions US). |
| 7 | Order blocks / liquidité | à définir | Aucune étude académique ; concepts difficiles à rendre déterministes. |

Les « taux de réussite » des figures qui circulent (ex. Bulkowski) portent surtout sur des actions,
sans coûts, avec des figures reconnues après coup. Ils ne sont pas transposables au forex.
