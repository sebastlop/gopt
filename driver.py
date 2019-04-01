import numpy as np
import gopt

def f_to_min(x):
	try:
	    return np.apply_along_axis(np.sum,1 , x)
	except: 
		print ("ups",x)

def eggholder(x):
	# https://en.wikipedia.org/wiki/Test_functions_for_optimization
	# min is f(512, 404.2319) = -959.6407
	# search space: -512 <x,y< 512
	y = x[1]
	x = x[0]
	return - ( y + 47 ) * np.sin(np.sqrt(np.abs( 0.5 * x + y + 47 ) )) - x * np.sin(np.sqrt(np.abs( x - y - 47)))


args = {
			'function': eggholder,
			'lb': [-100,-100],
			'ub': [100,100],
			'tribus': 10,
			'population': 10,
			'mutation_prob': .5,
			'mut_model': 'uniform',
			'gens_merge': 50
             
}

opt=gopt.gopt(**args)
opt.init_gopt()
tabla=opt.get_ft()
#print(tabla)
opt.run_tribus()
tabla_h=opt.get_sons()
#print('hijos:', tabla_h)
tabla=opt.get_ft()
#print(tabla)

opt.run_merge()
tabla_m = opt.get_sons_merge()
#print('tablammmmmmmmmmm',tabla_m)

tabla_me=opt.get_ft_merge()
print(tabla_me)



