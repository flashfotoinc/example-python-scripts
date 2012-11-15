ff_remove_uniform_background.py
Required:
Python 2.7

Usage: ff_remove_uniform_background.py -u partner_username -p partner_apikey -i image [options]


Example: (default)
user@ubuntu:~$ python ff_remove_uniform_background.py --partner-username=your_username --partner-apikey=your_apikey --image=apple.jpg --output-masked=apple_masked.png --output-mask=apple_mask.jpg

Uploading image:
{"ImageVersion": {"image_id": "86470", "format": "jpeg", "modified": "2012-11-15 10:04:04", "height": "1650", "width": "1523", "version": "", "sources": "[]", "created": "2012-11-15 10:04:04", "id": "325858"}, "Image": {"group": "Image", "created": "2012-11-15 10:04:04", "privacy": "private", "modified": "2012-11-15 10:04:04", "partner_id": "1", "id": "86470", "metadata": null}}

Removing Background:
{"status": "success"}

Downloading and Saving Mask (jpeg)

Downloading and Saving Masked (png)



Example: (remove holes)
user@ubuntu:~$ python ff_remove_uniform_background.py --partner-username=your_username --partner-apikey=your_apikey --image=backpack.jpg --find-holes --output-masked=backpack_masked.png --output-mask=backpack_mask.jpg

Uploading image:
{"ImageVersion": {"image_id": "86471", "format": "jpeg", "modified": "2012-11-15 10:04:04", "height": "1650", "width": "1523", "version": "", "sources": "[]", "created": "2012-11-15 10:04:04", "id": "325858"}, "Image": {"group": "Image", "created": "2012-11-15 10:04:04", "privacy": "private", "modified": "2012-11-15 10:04:04", "partner_id": "1", "id": "86470", "metadata": null}}

Removing Background:
{"status": "success"}

Downloading and Saving Mask (jpeg)

Downloading and Saving Masked (png)