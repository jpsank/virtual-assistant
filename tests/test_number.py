import sys, os
sys.path.append('{}/../'.format(os.path.dirname(os.path.abspath(__file__))))

from main import VirtAssistant

virt = VirtAssistant()

def text2num(text):
	return virt.text2num(text)
	
def test_one():
	assert text2num('one') == '1'
	
def test_two():
	assert text2num('two') == '2'
	
def test_three():
	assert text2num('three') == '3'
	
def test_four():
	assert text2num('four') == '4'
	
def test_five():
	assert text2num('five') == '5'

def test_six():
	assert text2num('six') == '6'

def test_seven():
	assert text2num('seven') == '7'

def test_eight():
	assert text2num('eight') == '8'

def test_nine():
	assert text2num('nine') == '9'

def test_ten():
	assert text2num('ten') == '10'

def test_eleven():
	assert text2num('eleven') == '11'

def test_twelve():
	assert text2num('twelve') == '12'

def test_thirteen():
	assert text2num('thirteen') == '13'

def test_fourteen():
	assert text2num('fourteen') == '14'

def test_fifteen():
	assert text2num('fifteen') == '15'

def test_sixteen():
	assert text2num('sixteen') == '16'

def test_seventeen():
	assert text2num('seventeen') == '17'

def test_eighteen():
	assert text2num('eighteen') == '18'

def test_nineteen():
	assert text2num('nineteen') == '19'

def test_twenty():
	assert text2num('twenty') == '20'

def test_thirty():
	assert text2num('thirty') == '30'

def test_forty():
	assert text2num('forty') == '40'

def test_fifty():
	assert text2num('fifty') == '50'

def test_sixty():
	assert text2num('sixty') == '60'

def test_seventy():
	assert text2num('seventy') == '70'

def test_eighty():
	assert text2num('eighty') == '80'

def test_ninety():
	assert text2num('ninety') == '90'

def test_one_hundred():
	assert text2num('one hundred') == '100'

def test_one_thousand():
	assert text2num('one thousand') == '1000'

def test_two_million():
	assert text2num('two million') == '2000000'

def test_three_billion():
	assert text2num('three billion') == '3000000000'

def test_four_trillion():
	assert text2num('four trillion') == '4000000000000'

def test_five_quadrillion():
	assert text2num('five quadrillion') == '5000000000000000'

def test_six_quintillion():
	assert text2num('six quintillion') == '6000000000000000000'

def test_seven_sextillion():
	assert text2num('seven sextillion') == '7000000000000000000000'

def test_eight_septillion():
	assert text2num('eight septillion') == '8000000000000000000000000'

def test_nine_octillion():
	assert text2num('nine octillion') == '9000000000000000000000000000'

def test_ten_nonillion():
	assert text2num('ten nonillion') == '10000000000000000000000000000000'

def test_eleven_decillion():
	assert text2num('eleven decillion') == '11000000000000000000000000000000000'

def test_one_million_two_hundred_thirty_two():
	assert text2num('one million two hundred thirty two') == '1000232'

def test_three_trillion_four_hundred_billion_five_million_two():
	assert text2num('three trillion four hundred billion five million two') == '3400005000002'