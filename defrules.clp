(defrule pricebuy
    (deltaprice big)
    (deltavolume big)
    (deltawbb big)
    =>
    (assert (pricedecision buy)))
(defrule pricebuyhold
    (deltaprice big)
    (deltavolume big)
    (deltawbb low)
    =>
    (assert (pricedecision buyhold)))
(defrule pricehold
    (deltaprice big)
    (deltavolume medium)
    (deltawbb low)
    =>
    (assert (pricedecision hold)))
(defrule pricesell
    (deltaprice minusbig)
    (deltavolume big)
    (deltawbb big)
    =>
    (assert (pricedecision sell)))
(defrule etabuy
    (deltaeta big)
    (deltavolume big)
    (deltawbb medium)
    =>
    (assert (etadecision buy)))
(defrule etabuyhold
    (deltaeta big)
    (deltavolume big)
    (deltawbb low)
    =>
    (assert (etadecision buyhold)))
(defrule etasell
    (deltaeta minusbig)
    (deltavolume big)
    (deltawbb medium)
    =>
    (assert (etadecision sell)))
(defrule etasellhold
    (deltaeta minusbig)
    (deltavolume big)
    (deltawbb low)
    =>
    (assert (etadecision sellhold)))
