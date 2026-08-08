"""Registry — one place that knows every solver.

The rest of the pipeline looks up a solver by its type name instead of
importing each solver file by hand. Add a new solver here once and it's
available everywhere.
"""

from vcd.solvers.numeral import NumeralSolver
from vcd.solvers.unit import UnitSolver
from vcd.solvers.gravitational import GravitationalSolver
from vcd.solvers.text_encryption import TextEncryptionSolver
from vcd.solvers.bit_manipulation import BitManipulationSolver
from vcd.solvers.equation import EquationSolver


# build one instance of each solver, keyed by its type_name
_SOLVERS = {}
for solver_class in (
    NumeralSolver,
    UnitSolver,
    GravitationalSolver,
    TextEncryptionSolver,
    BitManipulationSolver,
    EquationSolver,
):
    solver = solver_class()
    _SOLVERS[solver.type_name] = solver


def get_solver(type_name: str):
    """Return the solver for a puzzle type, or raise a clear error."""
    if type_name not in _SOLVERS:
        known = ", ".join(sorted(_SOLVERS))
        raise KeyError(
            f"No solver for type {type_name!r}. Known types: {known}")
    return _SOLVERS[type_name]


def all_types():
    """List every type that has a solver."""
    return sorted(_SOLVERS)
