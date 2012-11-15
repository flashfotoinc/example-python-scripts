ff_mugshot.py
Required:
Python 2.7

Usage: ff_mugshot.py -u partner_username -p partner_apikey -i image [options]


Example:
user@ubuntu:~$ python ff_mugshot.py --partner-username=your_username --partner-apikey=your_apikey --image=mugshot_example.JPG --output-masked=mugshot_example_masked.png --output-mask=mugshot_example_mask.jpg
 
Uploading image:
{"ImageVersion": {"image_id": "86578", "format": "jpeg", "modified": "2012-11-15 15:19:49", "height": "1655", "width": "1236", "version": "", "sources": "[]", "created": "2012-11-15 15:19:49", "id": "326169"}, "Image": {"group": "Image", "created": "2012-11-15 15:19:49", "privacy": "private", "modified": "2012-11-15 15:19:49", "partner_id": "1", "id": "86578", "metadata": null}}

Removing Background:
{"mugshot_status": "pending"}
{"mugshot_status": "pending"}
{"mugshot_status": "pending"}
{"mugshot_status": "pending"}
{"mugshot_status_message": null, "mugshot_status": "finished"}

Downloading and Saving Mask (jpeg)

Downloading and Saving Masked (png)



