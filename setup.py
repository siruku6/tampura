"""Build helpers for the tampura package.

This file keeps the project metadata in ``pyproject.toml`` and only adds the
custom build steps needed for SymK. It supports both normal and editable
installs by running ``tampura/third_party/symk/build.py`` before packaging.
"""

from pathlib import Path
import subprocess
import sys

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py as _build_py

try:
    from setuptools.command.editable_wheel import editable_wheel as _editable_wheel
except ImportError:
    _editable_wheel = None

PKG_NAME = "tampura"
SYMK_SRC = Path(__file__).parent / PKG_NAME / "third_party" / "symk"


def run_symk_build() -> None:
    """Invoke SymK’s own build script (CMake ➜ Make)."""
    subprocess.check_call([sys.executable, "build.py"], cwd=SYMK_SRC)


class BuildPy(_build_py):
    """Build SymK before packaging Python sources."""

    def run(self) -> None:
        run_symk_build()
        super().run()


if _editable_wheel is not None:

    class EditableWheel(_editable_wheel):
        """Build SymK before creating editable wheel metadata."""

        def run(self) -> None:
            run_symk_build()
            super().run()


cmdclass = {"build_py": BuildPy}
if _editable_wheel is not None:
    cmdclass["editable_wheel"] = EditableWheel

setup(
    name=PKG_NAME,
    version="0.1.0",
    packages=find_packages(include=[f"{PKG_NAME}*"]),
    cmdclass=cmdclass,
    include_package_data=True,
    package_data={f"{PKG_NAME}.third_party.symk": ["builds/release/**/*"]},
    zip_safe=False,  # the wheel contains platform-specific binaries
)
