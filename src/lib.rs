use cpython::py_module_initializer;

py_module_initializer!(ece461_team11, |py, m| {
    m.add(py, "__doc__", "Module documentation string")?;
    Ok(())
});