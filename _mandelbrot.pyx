
def divergence(complex c,nb_iteration):
	cdef complex z = 0
	for i in range(nb_iteration):
		z = z**2 + c
		if abs(z) > 2:
			return i+1
	return 0
