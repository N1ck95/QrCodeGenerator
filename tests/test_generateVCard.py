import sys
sys.path.append('../')
from generator import generateVCard 

def test_generateVCard():
    vcard = generateVCard(
        name = 'Pippo',
        surname = 'Baudo',
        title = 'PhD.',
        email= [{'type': 'work', 'email': 'pippo.baudo@gmail.com'}]
    )

    assert vcard == "BEGIN:VCARD\nVERSION:3.0\nFN:Pippo Baudo\nN:Baudo;Pippo;;PhD.;\nEMAIL;TYPE=work:pippo.baudo@gmail.com\nEND:VCARD"