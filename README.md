# Labels: xml to txt

ImageNet (pascalVOC) xml label format to [Darknet](https://github.com/pjreddie/darknet) text format.

### Installation

```bash
sudo pip install -r requirements.txt
```
### Usage

convert all xml files in `src` folder to txt format and save in `out` directory:

```bash
python xmltotxt.py --src xml --out out
```

### Example

Input xml file:

```xml
<annotation>
	<filename>image-0000016.jpg</filename>
	<size>
		<width>1920</width>
		<height>1080</height>
	</size>
	<object>
		<name>sedan</name>
		<bndbox>
			<xmin>75</xmin>
			<ymin>190</ymin>
			<xmax>125</xmax>
			<ymax>210</ymax>
		</bndbox>
	</object>
</annotation>
```

Output text file:

```text
4 0.052083 0.185185 0.026042 0.018519
```

### Image Annotation

Use [labelImg](https://github.com/tzutalin/labelImg) for image annotaions or checking bounding boxes.

> To check bounding boxes for YOLO  `.txt` label file, place `label.txt` and `image` and `classes.txt` together and open the image using `labelImg`.
> for VOC format just open the image.