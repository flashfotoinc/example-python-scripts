import urlparse
import sys
import optparse
import json
import urllib
import urllib2
import mimetypes
import time

#Argument Setup
usage = "Usage: %prog -u partner_username -p partner_api_key -i image [options]"
parser = optparse.OptionParser(usage=usage)

required = optparse.OptionGroup(parser, 'Required Fields')
required.add_option("-u", "--partner-username", dest="partner_username", help="Partner username")
required.add_option("-p", "--partner-apikey", dest="partner_apikey", help="Partner API Key (32 bit)")
required.add_option("-i", "--image", dest="image", help="The image file", metavar="FILE")

input_group = optparse.OptionGroup(parser, 'Input Options')
input_group.add_option("-b", "--base-url", dest="base_url", help="The base url for the project (Default: %default)", default='http://flashfotoapi.com/')

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
	

mugshot_image_url = '%sapi/mugshot/%s%s' % (options.base_url, image_id, auth_params)

#send the command
print "\nRemoving Background:"
try:
	perform_mugshot = urllib2.urlopen(mugshot_image_url)
	response = perform_mugshot.read()
except urllib2.HTTPError, e:
	print e
	print mugshot_image_url
	sys.exit(1)
#self closes so no need to call perform_mugshot.close()

mugshot_status_url = '%sapi/mugshot_status/%s%s' % (options.base_url, image_id, auth_params)

#send the command
try:
	perform_mugshot_status = urllib2.urlopen(mugshot_status_url)
	response = perform_mugshot_status.read()
except urllib2.HTTPError, e:
	print e
	print mugshot_status_url
	sys.exit(1)
#self closes so no need to call perform_mugshot.close()


#switch to json
try:
        response = json.loads(response)
	while (response['mugshot_status'] != 'finished' and response['mugshot_status'] != 'failed'):
	    time.sleep(4)
	    print json.dumps(response)
	    perform_mugshot_status = urllib2.urlopen(mugshot_status_url)
	    response = perform_mugshot_status.read()
	    response = json.loads(response)
	if (response['mugshot_status'] == 'finished'):
	    print json.dumps(response)
except ValueError, e:
	print e
	print 'Response: %s' % response
	sys.exit(1)

#determine if we need to get mask data
if options.output_mask:
	#we do, let's build the url
	mask_url = "%sapi/get/%s%s%s" % (options.base_url, image_id, auth_params, '&version=MugshotMask')
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
	masked_url = "%sapi/get/%s%s%s" % (options.base_url, image_id, auth_params, '&version=MugshotMasked')
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