# STL to STEP conversion

This packages [stltostp](https://github.com/slugdev/stltostp) in a web interface, exposed on port 8000.

This will take a STL file and return a STEP file.

Example run:
```
docker run -p 8000:8000 torkildr/stltostep-web
```

This can be consumed in a browser, or programmatically, eg.:

```
curl -F file=@foo.stl -o foo.step http://localhost:8000
```

