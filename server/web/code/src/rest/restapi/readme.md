Basic schema of the models of our Django /restapi/ subapp.

SuperPACs -
  variables:
    name
  methods:
    __str__

Representatives -
  variables:
    name
    district
    state
    party
  methods:
    __str__

Legislation -
  variables:
    name
    hr
  methods:
    __str__

Votes -
  variables:
    representative
    legislation
    decision
  methods:
    __str__

Donations -
  variables:
    superpac
    represenative
    amount
  methods:
    __str__
