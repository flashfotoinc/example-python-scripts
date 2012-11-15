import urlparse
import sys
import optparse
import json
import urllib
import urllib2
import mimetypes

#Argument Setup
usage = "Usage: %prog -u partner_username -p partner_api_key -i image -w ratioWidth -h ratioHeight -s filename [options]"
parser = optparse.OptionParser(usage=usage)

required = optparse.OptionGroup(parser, 'Required Fields')
required.add_option("-u", "--partner-username", dest="partner_username", help="Partner username")
required.add_option("-p", "--partner-apikey", dest="partner_apikey", help="Partner API Key (32 bit)")
required.add_option("-i", "--image", dest="image", help="The image file", metavar="FILE")
required.add_option("-w", "--width", dest="ratioWidth", help="Specifies the ratio of width units to crop with")
required.add_option("-y", "--height", dest="ratioHeight", help="Specifies the ratio of height units to crop with")
required.add_option("-s", "--save", dest="filename", help="Write crop result to a file (jpeg)")

input_group = optparse.OptionGroup(parser, 'Input Options')
input_group.add_option("-b", "--base-url", dest="base_url", help="The base url for the project (Default: %default)", default='http://flashfotoapi.com/')

parser.add_option_group(required)
parser.add_option_group(input_group)
(options, args) = parser.parse_args()


#Determine if required params are included
if not options.base_url or not options.partner_username or not options.partner_apikey or not options.image or not options.ratioWidth or not options.ratioHeight or not options.filename:
    print "Usage: %s -u partner_username -p partner_api_key -i image -w ratioWidth -h ratioHeight -s filename [options]" % __file__
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
crop_image_params = '&%s' % urllib.urlencode({'ratioWidth':options.ratioWidth, 'ratioHeight':options.ratioHeight})
crop_image_url = '%sapi/crop/%s%s%s' % (options.base_url, image_id, auth_params, crop_image_params)

#send the command
print "\nCroping and saving photo (jpeg):"
try:
	perform_crop = urllib2.urlopen(crop_image_url)
	response = perform_crop.read()
except urllib2.HTTPError, e:
	print e
	print crop_image_url
	sys.exit(1)
#self closes so no need to call perform_crop.close()

#save the file
try:
	fh = open(options.filename, 'w')
	fh.write(response)
except IOError, e:
	print e
	sys.exit(1)
fh.close()