import numpy as np


def test_import_arro3_compute():
    import arro3.compute


def test_null_mask_and_filter():
    import arro3.compute as cc
    from arro3.core import Array, DataType

    arr = Array([1.0, None, 3.0], type=DataType.float64())
    assert arr.null_count == 1

    mask = cc.is_null(arr).to_numpy()
    np.testing.assert_array_equal(mask, [False, True, False])

    valid = cc.filter(arr, cc.is_not_null(arr))
    assert valid.null_count == 0
    np.testing.assert_array_equal(valid.to_numpy(), [1.0, 3.0])
