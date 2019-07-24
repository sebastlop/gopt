import sys
sys.path.append('./src')
import gopt
from functions import *
import numpy as np

funciones = {
        'rastrigin': {
            'f': rastrigin,
            'lb': [-5.12, -5.12],
            'ub': [5.12, 5.12],
            'min': [0,0],
            'fmin': 0
            },
        'sphere': {
            'f': sphere,
            'lb': [-1000, -1000],
            'ub': [1000, 1000],
            'min': [0,0],
            'fmin': 0
            },
        'ackley': {
            'f': ackley,
            'lb': [ -5, -5],
            'ub': [ 5, 5],
            'min': [ 0, 0],
            'fmin': 0
            },
        'eggholder': {
            'f': eggholder,
            'lb': [-512, -512],
            'ub': [512, 512],
            'min': [512, 404.2319],
            'fmin': -959.6407
            },
        'crossintray': {
            'f': crossintray,
            'lb': [-10, -10],
            'ub': [10,10],
            'min': [(1.34941,1.34941), (-1.34941,1.34941), (1.34941,-1.34941), (-1.34941,-1.34941)],
            'fmin': [ -2.06261, -2.06261, -2.06261, -2.06261]
            },
        'beale': {
            'f': beale,
            'lb': [-4.5, -4.5],
            'ub': [4.5, 4.5],
            'min': [ 3, 0.5 ],
            'fmin': 0
            },
        'three-hump-cf': {
            'f': thcf,
            'lb': [ -5, -5],
            'ub': [5, 5],
            'min': [0,0],
            'fmin': 0

            }
        }
        
print('[+] Uniform mutator')
print('\n')
for k,v in funciones.items():

    args = {
        'function': v['f'],
        'lb': v['lb'],   # lower bond for search space
        'ub': v['ub'],     # upper bond for search space
		'tribus': 100,
		'population': 100,
		'mutation_prob': .5,
		'mut_model': 'uniform',
		'gens_merge': 200
     }
    print("[+] Optimizing function %s" % k)
    opt=gopt.gopt(**args)
    opt.init_gopt()
    opt.run_tribus()
    opt.run_merge()
    mins_merg = opt.get_sons_merge()
    table_merg = opt.get_ft_merge()
    print ("[+] Algorithm returned %s with value %f" % ( mins_merg[0], table_merg[0]))
    print ("[+] Function minimum is at %s with value %s" % (v['min'], v['fmin']))
    print ("\n")
print("****************")
print('[+] Normal mutator')
print('\n')
for k,v in funciones.items():

    args = {
        'function': v['f'],
        'lb': v['lb'],   # lower bond for search space
        'ub': v['ub'],     # upper bond for search space
		'tribus': 100,
		'population': 100,
		'mutation_prob': .5,
		'mut_model': 'normal',
		'gens_merge': 200
     }
    print("[+] Optimizing function %s" % k)
    opt=gopt.gopt(**args)
    opt.init_gopt()
    opt.run_tribus()
    opt.run_merge()
    mins_merg = opt.get_sons_merge()
    table_merg = opt.get_ft_merge()
    print ("[+] Algorithm returned %s with value %f" % ( mins_merg[0], table_merg[0]))
    print ("[+] Function minimum is at %s with value %s" % (v['min'], v['fmin']))
    print ("\n")


