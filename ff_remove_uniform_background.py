import urlparse
import sys
import optparse
import json
import urllib
import urllib2
import mimetypes

#Argument Setup
usage = "Usage: %prog -u partner_username -p partner_api_key -i image [options]"
parser = optparse.OptionParser(usage=usage)

required = optparse.OptionGroup(parser, 'Required Fields')
required.add_option("-u", "--partner-username", dest="partner_username", help="Partner username")
required.add_option("-p", "--partner-apikey", dest="partner_apikey", help="Partner API Key (32 bit)")
required.add_option("-i", "--image", dest="image", help="The image file", metavar="FILE")

input_group = optparse.OptionGroup(parser, 'Input Options')
input_group.add_option("-b", "--base-url", dest="base_url", help="The base url for the project (Default: %default)", default='http://flashfotoapi.com/')
input_group.add_option("-f", "--find-holes", dest="findholes", help="Set to find holes in the image", default=False, action="store_true")
input_group.add_option("-t", "--hole-thresh", dest="hole_similarity_thresh", help="This value is analyzed only if findholes is set. Threshold color similarity for finding a hole. (Default: %default)", default="110")
input_group.add_option("-c", "--clip-limit", dest="adapt_hist_eq_clip_limit", help="Clipping limit for adaptive histogram equalization; increasing this limit increases the contrast enhancement. (Default: %default)", default="0.0065")

output_group = optparse.OptionGroup(parser, 'Output Options')
output_group.add_option("-m", "--output-mask", dest="output_mask", help="Write output mask to a file (jpeg)", default='')
output_group.add_option("-d", "--output-masked", dest="output_masked", help="Write output masked to a file (png)", default='')

parser.add_option_group(required)
parser.add_option_group(input_group)
parser.add_option_group(output_group)
(options, args) = parser.parse_args()

#Determine if required params are included
if not options.base_url or not options.partner_username or not options.partner_apikey or not options.image:
    print "Usage: %s -u partner_username -p partner_apikey -i image [options]" % __file__
    sys.exit(1)


#build necessary url components
auth_params = '?%s' % urllib.urlencode({'partner_apikey':options.partner_apikey, 'partner_username':options.partner_username})
add_image_url = '%sapi/add/%s' % (options.base_url, auth_params)

#get file data and info
file_handle = file(options.image)
file_data = file_handle.read()
mimetypes.init()
mimetype = mimetypes.guess_type(options.image)
mimetype = mimetype[0]

#open connection
print "\nUploading image:"
connection = urllib2.build_opener(urllib2.HTTPHandler)
request = urllib2.Request(add_image_url, data=file_data)
request.add_header('Content-Type', mimetype)
request.get_method = lambda: 'PUT'
try:
	url = connection.open(request)
	response = url.read()
except urllib2.HTTPError, e:
	print e
	print add_image_url
	sys.exit(1)

connection.close()	
	
#switch to json
try:
	response = json.loads(response)
	print json.dumps(response)
except ValueError, e:
	print e
	print 'Response: %s' % response
	sys.exit(1)
	
image_id = int(response['ImageVersion']['image_id'])
	
#build url strings to perform crop
crop_image_params = ''
if options.findholes:
	if options.hole_similarity_thresh:
		crop_image_params = '&%s' % urllib.urlencode({'findholes':options.findholes, 'hole_similarity_thresh':options.hole_similarity_thresh})
	else:
		crop_image_params = '&%s' % urllib.urlencode({'findholes':options.findholes})
if options.adapt_hist_eq_clip_limit:
	crop_image_params = '%s&%s' % (crop_image_params, urllib.urlencode({'adapt_hist_eq_clip_limit':options.adapt_hist_eq_clip_limit}))

crop_image_url = '%sapi/remove_uniform_background/%s%s%s' % (options.base_url, image_id, auth_params, crop_image_params)

#send the command
print "\nRemoving Background:"
try:
	perform_crop = urllib2.urlopen(crop_image_url)
	response = perform_crop.read()
except urllib2.HTTPError, e:
	print e
	print crop_image_url
	sys.exit(1)
#self closes so no need to call perform_crop.close()

#switch to json
try:
	response = json.loads(response)
	print json.dumps(response)
except ValueError, e:
	print e
	print 'Response: %s' % response
	sys.exit(1)

#determine if we need to get mask data
if options.output_mask:
	#we do, let's build the url
	mask_url = "%sapi/get/%s%s%s" % (options.base_url, image_id, auth_params, '&version=UniformBackgroundMask')
	print "\nDownloading and Saving Mask (jpeg)"
	
	#download the file
	try:
		download_mask = urllib2.urlopen(mask_url)
		response = download_mask.read()
	except urllib2.HTTPError, e:
		print e
		print mask_url
		sys.exit(1)	
	#self closes so no need to call download_mask.close()
	
	#save the file
	try:
		fh = open(options.output_mask, 'w')
		fh.write(response)
	except IOError, e:
		print e
		sys.exit(1)
		
	fh.close()

#determine if we need to get masked data
if options.output_masked:
	#we do, let's build the url
	masked_url = "%sapi/get/%s%s%s" % (options.base_url, image_id, auth_params, '&version=UniformBackgroundMasked')
	print "\nDownloading and Saving Masked (png)"
	
	#download the file
	try:
		download_masked = urllib2.urlopen(masked_url)
		response = download_masked.read()
	except urllib2.HTTPError, e:
		print e
		print masked_url
		sys.exit(1)	
	#self closes so no need to call download_mask.close()
	
	#save the file
	try:
		fh = open(options.output_masked, 'w')
		fh.write(response)
	except IOError, e:
		print e
		sys.exit(1)
		
	fh.close()