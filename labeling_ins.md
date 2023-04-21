## 1. unzip the dataset

You will download one or mores zip files, the first step is going to unzip those files.

## 2. create `<dataset_name>.csv`

In the folder you just unzipped, there should a folder 
```
/<dataset_name>
    /image03
        /data
```
, which contains many png images. Change your working directory to it.

Next, please create a new file with a file name `<dataset_name>.csv`, i.e. `2011_09_26_drive_0048_extract.csv`. 

## 3. get all the file names

On windows with cmd:

`dir /b /a-d > <dataset_name>.csv`

On Mac/Linux with bash:

`ls > ./<dataset_name>.csv`

Where `<dataset_name>.csv` is the file you just created.

Once that's done, prepend the column names `frames,safety` to `<dataset_name>.csv`.

Now, the `<dataset_name>/image03/data` should look like below, and remember to remove the line `<dataset_name>.csv` from `<dataset_name>.csv`. It usually be the last line as:

```
frames,safety
00000001.png
00000002.png
00000003.png
...
00000012.png
00000013.png
<dataset_name>.csv // Remove this line.
```

## 4. label each frame

Open each image, and see if you think it's a good idea to make a lane change, if so, add `,1` to the corresponding filename in `<dataset_name>.csv`, if not, add `,0`. After all of the images are labeled, your `<dataset_name>.csv` should look like this:

```
frames,safety
00000001.png,0
00000002.png,0
00000003.png,1
...
00000012.png,1
00000013.png,0
```
