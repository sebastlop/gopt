import numpy as np
class gopt:
	def __init__(self, function, lb, ub, tribus = 1, population = 20, gens_trib = 20,
                 gens_merge = 50, mutation_prob = 0.3, mut_model = 'uniform', width_mut = 0.1):
    
		self.function = function
		self.lb = np.array(lb)
		self.ub = np.array(ub)
		self.tribus = tribus
		self.npop = population
		self.g_tr = gens_trib
		self.g_m = gens_merge
		self.mut_prob = mutation_prob
		self.model = mut_model
		self.width_mut = width_mut
		self.n_arg = len(self.lb)
		self.adan_eva = np.zeros((self.tribus, self.npop, self.n_arg))
		self.fit_table = np.zeros((self.tribus, self.npop))
		self.sons = np.zeros((self.tribus, self.npop, self.n_arg))
		self.tribal_merge=np.empty(self.n_arg)
		self.fit_table_merge=np.zeros(self.tribus)
		self.sons_merge=np.zeros((self.tribus,self.n_arg))

	def init_gopt(self):
		for tr in range(self.tribus):
			self.adan_eva[ tr] =  np.random.uniform(self.lb, self.ub, size = (self.npop, self.n_arg))
			self.fit_table[tr]  = np.apply_along_axis(self.function, 1, self.adan_eva[tr].copy())
			#self.fit_table[tr] = self.function(self.adan_eva[ tr ].copy() )
		

	def evolve_one_step(self, fathers, fit_table, mutator):
		
		sons = fathers[ fit_table.argsort()[: self.npop // 2], : ]

		id_cross_dad = np.random.randint( 0, self.npop //2, size = (self.npop//2, self.n_arg))
		id_cross_mom = np.random.randint( 0, self.npop //2, size = (self.npop//2, self.n_arg))

		bad_sons = (sons[ id_cross_dad, range(0, self.n_arg) ].copy() + sons[ id_cross_mom, range(0, self.n_arg) ].copy()) / 2.

		mut_idx = np.where( np.random.uniform( size = (self.npop // 2, 1) ) < self.mut_prob)[0]

		if self.model == 'uniform':
			muted = mutator(self.lb, self.ub, size = (bad_sons.shape[0], self.n_arg)) 
		else: 
			muted = mutator( sons[0], self.width_mut, size = (bad_sons.shape[0], self.n_arg))
			muted = np.minimum(self.ub,muted)
			muted = np.maximum(self.lb,muted)
	
		nidx = [ i for i in range(bad_sons.shape[0]) if i not in mut_idx ]
		muted[ nidx, :] = 0
		bad_sons[mut_idx, :] = 0
		bad_sons = np.add(muted, bad_sons)
		new_table = np.apply_along_axis(self.function, 1, bad_sons)

		fit_table = np.hstack( ( fit_table[ :self.npop // 2 ], new_table) )
		sons = np.vstack(([sons, bad_sons])) 
		idx = np.argsort(fit_table)
		return sons[idx], fit_table[idx]


	def run_tribus(self):
		assert(self.model in [ 'uniform', 'normal' ]), "Select a valid mutation model: uniform, normal"
		mutator = np.random.normal
		if self.model == 'uniform':
			mutator = np.random.uniform
		for steps in range(self.g_tr): 
			for tr in range(self.tribus): 
				self.adan_eva[tr], self.fit_table[tr] = self.evolve_one_step( self.adan_eva[tr][:], self.fit_table[tr], mutator )
	
		self.sons = self.adan_eva

	def run_merge(self):
		self.npop=self.tribus
        #model
		assert(self.model in [ 'uniform', 'normal' ]), "Select a valid mutation model: uniform, normal"
		mutator = np.random.normal
		if self.model == 'uniform':
			mutator = np.random.uniform
        #merging
		for tr in range(self.tribus):
			self.tribal_merge=np.vstack([self.tribal_merge,self.sons[tr,0,:]])
		self.tribal_merge = np.delete(self.tribal_merge,(0), axis=0)
        #calculating fit table
		for tr in range(self.tribus):
			self.fit_table_merge = np.apply_along_axis(self.function, 1, self.tribal_merge.copy())
        #Evolution
		for steps in range(self.g_m):
			self.tribal_merge, self.fit_table_merge = self.evolve_one_step( self.tribal_merge[:], self.fit_table_merge, mutator)
		self.sons_merge = self.tribal_merge
            
	def get_ft(self):
		return self.fit_table

	def get_sons(self):
		return self.sons

	def get_adan_eva(self):
		return self.adan_eva

	def get_tribal_merge(self):
		return self.tribal_merge
    
	def get_sons_merge(self):
		return self.sons_merge

	def get_ft_merge(self):
		return self.fit_table_merge