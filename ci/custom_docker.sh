# Copy of upstream function with added FREETYPEPY_BUNDLE_FT environment var
# passing.

function build_multilinux {
    # Runs passed build commands in manylinux container
    #
    # Depends on
    #     MB_PYTHON_VERSION
    #     UNICODE_WIDTH (optional)
    #     BUILD_DEPENDS (optional)
    #     DOCKER_IMAGE (optional)  
    #     MANYLINUX_URL (optional)
    #     WHEEL_SDIR (optional)
    local plat=$1
    [ -z "$plat" ] && echo "plat not defined" && exit 1
    local build_cmds="$2"
    local docker_image=${DOCKER_IMAGE:-quay.io/pypa/manylinux1_\$plat}
    docker_image=$(eval echo "$docker_image")
    retry docker pull $docker_image

    if [ -n "$FREETYPEPY_BUNDLE_FT" ];
        then
            docker run --rm \
                -e FREETYPEPY_BUNDLE_FT="1" \
                -e BUILD_COMMANDS="$build_cmds" \
                -e PYTHON_VERSION="$MB_PYTHON_VERSION" \
                -e UNICODE_WIDTH="$UNICODE_WIDTH" \
                -e BUILD_COMMIT="$BUILD_COMMIT" \
                -e CONFIG_PATH="$CONFIG_PATH" \
                -e ENV_VARS_PATH="$ENV_VARS_PATH" \
                -e WHEEL_SDIR="$WHEEL_SDIR" \
                -e MANYLINUX_URL="$MANYLINUX_URL" \
                -e BUILD_DEPENDS="$BUILD_DEPENDS" \
                -e USE_CCACHE="$USE_CCACHE" \
                -e REPO_DIR="$repo_dir" \
                -e PLAT="$PLAT" \
                -v $PWD:/io \
                -v $HOME:/parent-home \
                $docker_image /io/$MULTIBUILD_DIR/docker_build_wrap.sh
        else
            docker run --rm \
                -e BUILD_COMMANDS="$build_cmds" \
                -e PYTHON_VERSION="$MB_PYTHON_VERSION" \
                -e UNICODE_WIDTH="$UNICODE_WIDTH" \
                -e BUILD_COMMIT="$BUILD_COMMIT" \
                -e CONFIG_PATH="$CONFIG_PATH" \
                -e ENV_VARS_PATH="$ENV_VARS_PATH" \
                -e WHEEL_SDIR="$WHEEL_SDIR" \
                -e MANYLINUX_URL="$MANYLINUX_URL" \
                -e BUILD_DEPENDS="$BUILD_DEPENDS" \
                -e USE_CCACHE="$USE_CCACHE" \
                -e REPO_DIR="$repo_dir" \
                -e PLAT="$PLAT" \
                -v $PWD:/io \
                -v $HOME:/parent-home \
                $docker_image /io/$MULTIBUILD_DIR/docker_build_wrap.sh
    fi
}
