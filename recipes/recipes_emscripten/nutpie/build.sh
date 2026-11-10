#!/bin/bash

export MATURIN_PYTHON_SYSCONFIGDATA_DIR=${PREFIX}/etc/conda/_sysconfigdata__emscripten_wasm32-emscripten.py

# Same setup as the wasm build in nutpie's CI: no threads, zarr or stan on
# wasm, and GKlib (vendored METIS) uses setjmp, which needs wasm longjmp.
# EMCC_CFLAGS from the emscripten activation already adds -fPIC and
# -fwasm-exceptions for the C code.
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-sSUPPORT_LONGJMP=wasm"

# Use wasm SIMD like the C code (EMCC_CFLAGS has -msimd128). faer and other
# crates pick their SIMD code paths at compile time on wasm.
export RUSTFLAGS="${RUSTFLAGS} -C target-feature=+simd128"

# TEMPORARY, for profiling: keep function names (wasm "name" section, no
# DWARF) so browser profilers show symbols. Remove before submitting.
# emcc appends EMCC_CFLAGS (which has -g0 from the emscripten activation)
# to every call, including the final link, so replace -g0 there.
export EMCC_CFLAGS="${EMCC_CFLAGS//-g0/--profiling-funcs}"
export MATURIN_PEP517_ARGS="--no-default-features"

${PYTHON} -m pip install . -vvv ${PIP_ARGS}
