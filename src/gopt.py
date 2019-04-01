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
	
		
	def run_merge(self):

		if self.model == 'uniform':

			for tr in range(self.tribus):
				self.tribal_merge=np.vstack([self.tribal_merge,self.sons[tr,0,:]])

			self.tribal_merge = np.delete(self.tribal_merge,(0), axis=0)
			for tr in range(self.tribus):
				self.fit_table_merge[tr] = self.function(self.tribal_merge[tr].copy())
		
			for steps in range(self.g_m):
				for j in range(np.int(self.tribus/2)):
					self.sons_merge[j,:] = self.tribal_merge[self.fit_table_merge.argsort()][j,:]
				for j in range(np.int(self.tribus/2)):
					idx_cross_dad = np.random.randint(0,np.int(self.tribus/2),self.n_arg)
					idx_cross_mom = np.random.randint(0,np.int(self.tribus/2),self.n_arg)
					for k in range(self.n_arg):
						self.sons_merge[j+np.int(self.tribus/2),k] = (self.sons_merge[idx_cross_dad[k],k]+self.sons_merge[idx_cross_mom[k],k])/2
					if(np.random.uniform(0,1)< self.mut_prob):
						mutidx=np.random.randint(0,int(self.tribus/2))
						self.sons_merge[j+np.int(self.tribus/2)]=np.random.uniform(self.lb, self.ub, self.n_arg)
						    						    
				self.fit_table_merge.sort()
		
				for i in range(np.int(self.tribus/2)):
					self.fit_table_merge[i+np.int(self.tribus/2)] = self.function(self.sons_merge[i+np.int(self.tribus/2),0:int(self.n_arg)].copy())

				self.tribal_merge = self.sons_merge
		elif self.model == 'normal':

			for tr in range(self.tribus):
				self.tribal_merge=np.vstack([self.tribal_merge,self.sons[tr,0,:]])

			self.tribal_merge = np.delete(self.tribal_merge,(0), axis=0)
			for tr in range(self.tribus):
				self.fit_table_merge[tr] = self.function(self.tribal_merge[tr].copy())
		
			for steps in range(self.g_m):
				for j in range(np.int(self.tribus/2)):
					self.sons_merge[j,:] = self.tribal_merge[self.fit_table_merge.argsort()][j,:]
				for j in range(np.int(self.tribus/2)):
					idx_cross_dad = np.random.randint(0,np.int(self.tribus/2),self.n_arg)
					idx_cross_mom = np.random.randint(0,np.int(self.tribus/2),self.n_arg)
					for k in range(self.n_arg):
						self.sons_merge[j+np.int(self.tribus/2),k] = (self.sons_merge[idx_cross_dad[k],k]+self.sons_merge[idx_cross_mom[k],k])/2
					if(np.random.uniform(0,1)< self.mut_prob):
						for i in range(self.n_arg):
							mutidx=np.random.randint(0,int(self.tribus/2))
							self.sons_merge[j+np.int(self.tribus/2),i]=np.random.normal(self.sons_merge[mutidx,i],self.width_mut,1)
						    
				self.fit_table_merge.sort()
		
				for i in range(np.int(self.tribus/2)):
					self.fit_table_merge[i+np.int(self.tribus/2)] = self.function(self.sons_merge[i+np.int(self.tribus/2),0:int(self.n_arg)].copy())

				self.tribal_merge = self.sons_merge

		else:
			print('Select a valid model: uniform / normal')


		self.sons_merge = self.sons_merge[self.fit_table_merge.argsort()]
		self.fit_table_merge.sort()
		

	def get_ft(self):
		return self.fit_table

	def get_sons(self):
		return self.sons

	def get_sons_merge(self):
		return self.sons_merge

	def get_ft_merge(self):
		return self.fit_table_merge
