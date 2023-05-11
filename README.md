# QR Code Generator

<img src="https://img.shields.io/badge/QR%20Code%20Generator-v1.0-blue">
<img src="https://img.shields.io/badge/python-3.10-blue">

This project is a QR Code Generator tool providing the capabilities to create QR Codes with more complex data structures (such as VCard).
The tool also allow to add a logo to the generated QR Code which allows so to custominze its appearence.

## Project configuration
To configure this project you need to install some additional python library (described in requirements.txt). It is recommend using a dedicated virtual environment such as venv. An example of the installation flow is:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Sample usage
There are two available modes to generate a QR Code: url and vcard.
- url: allows to encode the given url inside the QR Code. Here is an example:
```bash
python generator.py --type url --url <your url here>
```
- vcard: allows to generate a QR Code containing a vCard with the data provided (see the program help to get all the available options).
```bash
python generator.py --type vcard --name <name> --surname <surname> --email <type1> <email1> <type2> <email2>
```
In both modes, the generated qrcode will be saved in the file qrcode.png. It is possible to customize the QR Code adding a custom logo in the center with the `--logo <logofile.png>` option. Here is a simple example of how to do this:
```bash
python generator.py --type url --url <your url here> --logo <logofile>
```

## Author
This project is created and maintained by [Niccolò Borgioli](mailto:borgioli.niccolo@gmail.com)