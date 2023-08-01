'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    This program is developed and maintained by Niccolò Borgioli <borgioli.niccolo@gmai.com>
'''

import qrcode
from PIL import Image
import argparse

'''
This function generates a VCard string using the provided data
@param name - string: name 
@param surname - string: surname
@param middlename - string (optional): middlename
@param title - string (optional) Specifies the job title, functional position or function of the individual associated with the vCard object within an organization.
@param suffix - string (optional) Honorific Suffixes
@param company - string (optional) The name and optionally the unit(s) of the organization associated with the vCard object. This property is based on the X.520 Organization Name attribute and the X.520 Organization Unit attribute.
@param email - list (optional) List containing the email addresses of the person. Each list element is a dictionary with 'type' and 'email' attribute
@param phone - string (optional) Phone number
@param address - string (optional) A structured representation of the physical delivery address for the vCard object.
@return string - vCard object string representation
'''
def generateVCard(name, surname, middlename='', title='', suffix='', company=None, email=[], phone=None, address=None):
    data = ['BEGIN:VCARD', 'VERSION:3.0']
    data.append('FN:{} {}'.format(name, surname))
    data.append('N:{};{};{};{};{}'.format(surname, name, middlename,title, suffix))
    
    for mail in email:
        data.append('EMAIL;TYPE={}:{}'.format(mail['type'], mail['email']))
    
    if phone is not None:
        data.append('TEL;TYPE={}:{}'.format(phone['type'], phone['number']))

    if address is not None:
        data.append('ADR;TYPE={}:{}'.format(address['type'], address['addr']))

    if company is not None:
        data.append('ORG:{}'.format(company))

    data.append('END:VCARD')
    return "\n".join(data)

'''
This function generates a QR Code image encoding the data provided and with the (optional) logo
@param data - string: data to be encoded in the QR Code
@param filename - string: name of the generated QR Code image
@param logo_file - string (optional): name of the logo image to be included into the generated QR Code
'''
def generateQRCode(data, filename, logo_file=None):
    if logo_file is not None:
        qr_code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)   # In this case we need a high redundant qrcode
        qr_code.add_data(data)
        qr_code.make()
        qr_img = qr_code.make_image().convert('RGB') # generate the image of the qrcode
        logo = Image.open(logo_file)
        basewidth = 100

        # adjust logo image size
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

        # compute logo position to put it at the center
        logo_x_position = (qr_img.size[0] - logo.size[0]) // 2
        logo_y_position = (qr_img.size[1] - logo.size[1]) // 2
        logo_position = (logo_x_position, logo_y_position)

        # insert logo image into qr code image
        qr_img.paste(logo, logo_position)
    else:
        qr_img = qrcode.make(data)
    qr_img.save(filename)

'''
This program generates a QR Code image encoding either an url or a vCard 
Here is a sample of the two available modes:
python generator.py --type url --url <your url here>
python generator.py --type vcard --name <name> --surname <surname> --email <type1> <email1> <type2> <email2>
The generated qrcode is saved in the qrcode.png file 
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser("QR Code generator")
    parser.add_argument("--type", choices=['url', 'vcard'], required=True)
    parser.add_argument("--name", type=str, default='')
    parser.add_argument("--surname", type=str, default='')
    parser.add_argument("--middlename", type=str, default='')
    parser.add_argument("--title", type=str, default='')
    parser.add_argument("--suffix", type=str, default='')
    parser.add_argument("--company", type=str, default=None)
    parser.add_argument("--email", nargs='+', default=None)
    parser.add_argument("--phone", type=str, default=None)
    parser.add_argument("--address", type=str, default=None)
    parser.add_argument("--url", type=str, default=None)
    parser.add_argument("--logo", type=str, default=None)
    args = parser.parse_args()

    if args.type == 'vcard':
        if args.name != '' and args.surname != '':
            email = []
            type = None
            if args.email is not None:
                for item in args.email:
                    if type is None:
                        type = item
                    else:
                        email.append({'type': type, 'email': item})
                        type = None
            data = generateVCard(args.name, args.surname, middlename=args.middlename, title=args.title, suffix=args.suffix, company=args.company, email=email, phone=args.phone)
        else:
            print("Error: when generating a vCard at least a name and surname is required")
    else:
        data = args.url
    generateQRCode(data, 'qrcode.png', logo_file=args.logo)
    print("QR code generated successfully")