import random

import pytest

from notebook_loader import last_notebook

oppgave = last_notebook("oppgave")

INGEN = "Ingen løsning"
UENDELIG = "Uendelig mange løsninger"

FASTE = [
    ((1, 1, 10, 1, -1, 2), (6.0, 4.0)),
    ((2, 3, 13, 1, -1, -1), (2.0, 3.0)),
    ((0, 1, 5, 1, 0, 2), (2.0, 5.0)),
    ((0.5, 0.25, 1, 1, -1, 0.5), (1.5, 1.0)),
    ((3, 7, 1, 2, 5, 4), (-23.0, 10.0)),
    ((1, 2, 3, 2, 4, 7), INGEN),
    ((1, 1, 1, 1, 1, 2), INGEN),
    ((0, 3, 1, 0, 6, 1), INGEN),
    ((3, -2, 4, 6, -4, 8), UENDELIG),
    ((2, 1, 0, 4, 2, 0), UENDELIG),
    ((1, -1, 2, -2, 2, -4), UENDELIG),
]


def _naer_avrundingsgrense(v):
    return abs((abs(v) * 100) % 1 - 0.5) < 1e-6


def _tilfeldige(antall, seed=2025):
    rng = random.Random(seed)
    tilfeller = []
    while len(tilfeller) < antall:
        a1, b1, c1, a2, b2, c2 = (rng.randint(-10, 10) for _ in range(6))
        d = a1 * b2 - a2 * b1
        if d == 0:
            continue
        x = (c1 * b2 - c2 * b1) / d
        y = (a1 * c2 - a2 * c1) / d
        if _naer_avrundingsgrense(x) or _naer_avrundingsgrense(y):
            continue
        tilfeller.append(((a1, b1, c1, a2, b2, c2), (round(x, 2), round(y, 2))))
    return tilfeller


@pytest.mark.parametrize("args,fasit", FASTE + _tilfeldige(20))
def test_los_likningssett(args, fasit):
    svar = oppgave.los_likningssett(*args)
    if isinstance(fasit, tuple):
        assert isinstance(svar, (tuple, list)) and len(svar) == 2
        assert tuple(svar) == fasit
    else:
        assert svar == fasit
