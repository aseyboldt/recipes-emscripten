def test_import_arro3_core():
    import arro3.core


def test_array_roundtrip():
    from arro3.core import Array, DataType, Table

    arr = Array([1, 2, 3], type=DataType.int64())
    assert len(arr) == 3
    assert arr.type == DataType.int64()
    assert arr.to_pylist() == [1, 2, 3]

    table = Table.from_pydict({"a": arr})
    assert table.num_rows == 3
    assert table.column_names == ["a"]
