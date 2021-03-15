(defrule powerpricebigbuy
    (deltaprice big)
    =>
    (assert (powerprice big buy)))
(defrule powerpricemediumbuy
    (deltaprice medium)
    =>
    (assert (powerprice medium buy)))
(defrule powerpricebiggerthan0
    (deltaprice biggerlow)
    =>
    (assert (powerprice low buy)))
(defrule powerpricelowerthan0
    (deltaprice lowerlow)
    =>
    (assert (powerprice low sell)))
(defrule powerpriceminusmedium
    (deltaprice minusmedium)
    =>
    (assert (powerprice medium sell)))
(defrule powerpriceminusbig
    (deltaprice minusbig)
    =>
    (assert (powerprice big buy)))