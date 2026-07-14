"""Put scripts/ on sys.path so tests import the build modules like the CLIs do."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
