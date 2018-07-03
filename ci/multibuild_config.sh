# Define custom utilities
# Test for OSX with [ -n "$IS_OSX" ]

function pre_build {
    # Any stuff that you need to do before you start building the wheels
    # Runs in the root directory of this repository.
    if [ -z "$IS_OSX" ]; then
        pip install cmake  # Version in manylinux1 container too old.
    fi
}

function run_tests {
    # The function is called from an empty temporary directory.
    cd ../tests
    python -c "import freetype; print('Using FreeType version ', freetype.version())"
    pytest
}
