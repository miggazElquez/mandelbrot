#rouge|bleu- Rouge+, vert-, bleu+, rouge-
#_0        _1     _2     _3     _4      _5
_0,_1,_2,_3,_4,_5 = 0, 100, 200, 475, 700, 900



def rouge(val):
	if _2<=val<=_4:
		return 255
	elif _1 <= val <= _2:
		return round((val - _1) * 255 /(_2 - _1))
	elif val < _1: 
		return round((_1 - val)* 255/_1)
	else:
		return round((_5 - val) * 255 /(_5 - _4))

def vert(val):
	if val<=_2:
		return 255
	elif val>=_3:
		return 0
	else:
		return round((_3 - val) * 255 / (_3 - _2))

def bleu(val):
	if val < _1:
		return round((_1 - val)* 255/_1)
	elif val <=_3:
		return 0
	elif val >=_4:
		return 255
	else:
		return round((val - _3) * 255 / (_4 - _3))

def color(val):
	return rouge(val), vert(val), bleu(val)

