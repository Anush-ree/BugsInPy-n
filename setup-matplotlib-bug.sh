#!/opt/homebrew/bin/bash
# setup-matplotlib-bug.sh
#
# Sets up a matplotlib bug from BugsInPy on macOS (Apple Silicon).
# Handles: Rosetta conda env, build deps, runtime deps, in-place compile, pytest install.
#
# Usage:
#   ./setup-matplotlib-bug.sh <bug_id>
#
# Example:
#   ./setup-matplotlib-bug.sh 17
#
# Assumes BugsInPy framework scripts are already patched for macOS:
#   - shebangs point at /opt/homebrew/bin/bash
#   - /opt/conda paths replaced with /opt/homebrew/Caskroom/miniconda/base
#   - sed -i syntax fixed for BSD
#   - &>>file replaced with >>file 2>&1

set -e

# --- Config (edit these paths if your layout differs) ---
BUGSINPY_ROOT="/Users/anush/Downloads/DePaul/Research/Projects/BugsInPy-n"
WORKSPACE="${BUGSINPY_ROOT}/workspace"
CONDA_SH="/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh"

# --- Args ---
if [ -z "$1" ]; then
    echo "Usage: $0 <bug_id>"
    echo "Example: $0 17"
    exit 1
fi
BUG_ID="$1"
BUG_DIR="${WORKSPACE}/matplotlib"

# --- Sanity checks ---
if [ ! -f "${BUGSINPY_ROOT}/projects/matplotlib/bugs/${BUG_ID}/bug.info" ]; then
    echo "ERROR: matplotlib bug ${BUG_ID} not found in BugsInPy."
    echo "Available bugs:"
    ls "${BUGSINPY_ROOT}/projects/matplotlib/bugs/" | sort -n
    exit 1
fi

source "$CONDA_SH"

# --- Step 1: Checkout ---
echo "==> [1/5] Checking out matplotlib bug ${BUG_ID}..."
# Remove existing checkout if present (avoid stale artifacts)
if [ -d "$BUG_DIR" ]; then
    echo "    Removing existing $BUG_DIR"
    rm -rf "$BUG_DIR"
fi
mkdir -p "$WORKSPACE"
"${BUGSINPY_ROOT}/framework/bin/bugsinpy-checkout" -p matplotlib -v 0 -i "$BUG_ID" -w "$WORKSPACE"

cd "$BUG_DIR"

# --- Step 2: Compute conda env name (matches bugsinpy-compile's hash logic) ---
PY_VER=$(grep -o '3\..\..' bugsinpy_bug.info | head -1)
# Empty/whitespace-only requirements still produce a hash; mirror the script
ENV_NAME=$(cat <(echo "$PY_VER") bugsinpy_requirements.txt | md5 -r | cut -d' ' -f1)
echo "==> [2/5] Conda env name: $ENV_NAME (Python $PY_VER)"

# --- Step 3: Create conda env (Rosetta x86_64 — Python 3.8.1 not on arm64) ---
if conda env list | grep -q "^${ENV_NAME}\s"; then
    echo "    Env already exists, reusing."
else
    echo "    Creating osx-64 env..."
    CONDA_SUBDIR=osx-64 conda create -n "$ENV_NAME" -y python="$PY_VER"
fi
conda activate "$ENV_NAME"

# --- Step 4: Install build deps + runtime deps + pytest ---
echo "==> [3/5] Installing build dependencies (freetype, libpng, pkg-config)..."
conda install -y -c conda-forge freetype libpng pkg-config

echo "==> [4/5] Installing matplotlib runtime deps + pytest..."
pip install \
    "numpy>=1.15,<1.22" \
    "pillow<10" \
    "cycler" \
    "kiwisolver<1.4" \
    "pyparsing<3" \
    "python-dateutil" \
    "pytest"

# --- Step 5: Build matplotlib in-place (compiles C extensions) ---
echo "==> [5/5] Building matplotlib in-place (this takes a few minutes)..."
pip install -e . --no-build-isolation

# --- Verify ---
echo ""
echo "==> Verifying build..."
python -c "import matplotlib; print('matplotlib', matplotlib.__version__)"
python -c "from matplotlib import ft2font; print('ft2font OK')"

# --- Mark compile flag for bugsinpy-test ---
echo "1" > bugsinpy_compile_flag

echo ""
echo "==> Setup complete for matplotlib bug ${BUG_ID}"
echo "    Workspace: $BUG_DIR"
echo "    Conda env: $ENV_NAME (active)"
echo ""
echo "Next steps:"
echo "    cd $BUG_DIR"
echo "    bugsinpy-test     # should reproduce the failing test"
