ff_faceAndHair.py
Required:
Python 2.7

Usage: ff_faceAndHair.py -u partner_username -p partner_apikey -i image [options]


Example:
user@ubuntu:~$ python ff_faceAndHair.py --partner-username=your_username --partner-apikey=your_apikey --image=faceAndHair_example.JPG --output-masked=faceAndHair_example_masked.png --output-mask=faceAndHair_example_mask.jpg
 
Uploading image:
{"ImageVersion": {"image_id": "87873", "format": "jpeg", "modified": "2012-11-20 15:29:40", "height": "1655", "width": "1236", "version": "", "sources": "[]", "created": "2012-11-20 15:29:40", "id": "329981"}, "Image": {"group": "Image", "created": "2012-11-20 15:29:40", "privacy": "private", "modified": "2012-11-20 15:29:40", "partner_id": "1", "id": "87873", "metadata": null}}

Removing Background:
{"segmentation_status": "pending"}
{"segmentation_status": "pending"}
{"segmentation_status": "pending"}
{"segmentation_status": "pending"}
{"chin_point_x": 158, "head_position_y": 240, "segmentation_status_message": null, "head_width": 169, "mask_status": null, "crop_width": 306, "image_scale": 0, "segmentation_status": "finished", "image_width": 0, "crop_rotation": 4.1025643348694, "mugshot_status": null, "head_position_x": 74, "chin_point_y": 264, "crop_position_x": 463, "crop_position_y": 405, "merge_status_message": null, "soft_chin_data": [50.54084777832, 85.273727416992, 49.062255859375, 99.72021484375, 49.120742797852, 113.16957092285, 50.692535400391, 127.28741455078, 55.329467773438, 141.94253540039, 63.695693969727, 152.47132873535, 74.63752746582, 158.26303100586, 91.081420898438, 160.48999023438, 107.61199951172, 157.7629699707, 118.88067626953, 151.38409423828, 126.63902282715, 140.78215026855, 130.56924438477, 126.8099822998, 132.22985839844, 111.68295288086, 132.40649414062, 98.008041381836, 131.27764892578, 83.458267211914, 0.4350583255291, -0.015780288726091, 0.00078597228275612, -0.47201189398766, -66.130126953125, 83.512016296387, 102], "mugshot_status_message": null, "mask_status_message": null, "merged_image_id": null, "crop_height": 320, "head_rotation": 0, "head_height": 169, "merge_status": null, "image_height": 0}

Downloading and Saving Mask (jpeg)

Downloading and Saving Masked (png)
