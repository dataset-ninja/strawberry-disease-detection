Dataset **Strawberry Disease Detection** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMjI2OV9TdHJhd2JlcnJ5IERpc2Vhc2UgRGV0ZWN0aW9uL3N0cmF3YmVycnktZGlzZWFzZS1kZXRlY3Rpb24tRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiZXgrZlBQYW1jc2QxOTdQTU1UeGlWcWdOS0psSTViWFZNWkMzeFdldG1rZz0ifQ==?response-content-disposition=attachment%3B%20filename%3D%22strawberry-disease-detection-DatasetNinja.tar%22)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Strawberry Disease Detection', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

