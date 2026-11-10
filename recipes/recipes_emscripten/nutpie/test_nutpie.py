import numpy as np


def _normal_model(n=3, **kwargs):
    from nutpie.compiled_pyfunc import from_pyfunc

    def make_logp_fn():
        def logp(x, **shared):
            return -0.5 * float(x @ x), -np.ascontiguousarray(x, dtype="float64")

        return logp

    def make_expand_fn(seed1, seed2, chain):
        def expand(x, **shared):
            return {"x": np.asarray(x, dtype="float64", order="C")}

        return expand

    return from_pyfunc(
        n,
        make_logp_fn,
        make_expand_fn,
        [np.dtype("float64")],
        [(n,)],
        ["x"],
        **kwargs,
    )


def test_import():
    import nutpie

    assert isinstance(nutpie.__version__, str)


def test_sample_pyfunc():
    import nutpie

    compiled = _normal_model(
        coords={"idx": ["a", "b", "c"]},
        dims={"x": ("idx",)},
    )
    trace = nutpie.sample(
        compiled, chains=2, tune=300, draws=300, seed=1, progress_bar=False
    )

    x = trace.posterior["x"]
    assert x.dims == ("chain", "draw", "idx")
    assert x.shape == (2, 300, 3)
    assert np.all(np.isfinite(x.values))
    assert int(trace.sample_stats["diverging"].sum()) == 0
