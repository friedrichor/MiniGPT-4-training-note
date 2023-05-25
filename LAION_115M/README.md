# Download LAION 115M


## **1** download <caption,url> file

download <caption, url> from [**url**](https://storage.googleapis.com/sfr-vision-language-research/BLIP/datasets/laion_synthetic_filtered_large.json) and save it locally as `laion_synthetic_filtered_large.json`

```shell
cd LAION_115M
python download_json.py
```

Data format:
```json
[
    {
        "caption": "the tiki ball logo is displayed on this apron", 
        "url": "https://image.spreadshirtmedia.com/image-server/v1/products/P1016953357T1186A359PC1026849373PA2537PT17X1Y0S28/views/1,width=300,height=300,appearanceId=359,version=1497265829/z-tiki-bar-adjustable-apron.png"
    }, 
    {
        "caption": "the view of an aerial pool with palm trees", 
        "url": "http://uberflip.cdntwrk.com/mediaproxy?url=http%3A%2F%2Fd22ir9aoo7cbf6.cloudfront.net%2Fwp-content%2Fuploads%2Fsites%2F4%2F2018%2F01%2FAyana1.jpg&size=1&version=1517393441&sig=e3e14f09e2b062e0fd144306d56abda7&default=hubs%2Ftilebg-blogs.jpg"
    }, 
    {
        "caption": "a sky with clouds women's v - neck", 
        "url": "https://render.fineartamerica.com/images/rendered/medium/t-shirt/30/9/images/artworkimages/medium/1/approaching-storm-paxton-mobley.jpg?targetx=0&targety=0&imagewidth=300&imageheight=149&modelwidth=300&modelheight=405"
    }, 
    ...
]
```

### (Optional) compress file
    
`laion_synthetic_filtered_large.json` occupies 20.24GB of cpu memory.

- [ ] If desired, you can compress it to a `tar.gz` file, which is only 7.32GB. But it doesn't help with training, it just makes it easier to upload or download.


## **2** prepare the data step-by-step

### setup the dataset folder and move the annotation file to the data storage folder

```shell
mv laion_synthetic_filtered_large.json laion
```

### convert the laion annotation file format to be img2dataset format

```shell
python convert_laion.py
```

You'll get `laion_synthetic_filtered_large.tsv`, which takes up 15.25GB of cpu memory.

### install img2dataset

github: [https://github.com/rom1504/img2dataset](https://github.com/rom1504/img2dataset)

```shell
pip install img2dataset
```

### download the datasets with img2dataset

```shell
sh download_laion.sh
```
