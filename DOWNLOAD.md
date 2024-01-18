Dataset **Strawberry Disease Detection** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/b/T/f8/fDsV4qOjZQ3k09zyinszUTscRk9DMLKaHptANzoBSUF6WIGHIG4HZ57Ob5evlRAdsCyJEZNd2gwiGwojIvBzCZsClKyQlQnkqtADl4h8u8Pby08x49joWHuTWlnL.tar)

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

