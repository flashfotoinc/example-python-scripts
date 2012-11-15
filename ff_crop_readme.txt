ff_crop.py
Required:
Python 2.7

Usage: ff_crop.py -u partner_username -p partner_api_key -i image -w ratioWidth -h ratioHeight -s filename [options]

Example:
user@ubuntu:~$ python ff_crop.py --partner-username=your_username --partner-apikey=your_apikey --image=002.jpg --width=1 --height=1 --save=002_cropped.jpg

Uploading image:
{"ImageVersion": {"image_id": "86463", "format": "jpeg", "modified": "2012-11-15 09:56:33", "height": "750", "width": "1000", "version": "", "sources": "[]", "created": "2012-11-15 09:56:33", "id": "325846"}, "Image": {"group": "Image", "created": "2012-11-15 09:56:33", "privacy": "private", "modified": "2012-11-15 09:56:33", "partner_id": "1", "id": "86463", "metadata": null}}

Croping and saving photo (jpeg):