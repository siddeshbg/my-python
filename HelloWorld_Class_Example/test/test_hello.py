from HelloWorld_Class_Example.src.HelloWorld import HelloWorld

def test_hello():
    metadata = HelloWorld("Siddesh")
    assert "Hello Siddesh" == metadata.hello()

    test2 = HelloWorld("Seema")
    assert "Hello Seema" == test2.hello()
