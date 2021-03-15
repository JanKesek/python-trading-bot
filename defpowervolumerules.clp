(defrule powervolumebig
    (deltaprice ?deltaprice)
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
