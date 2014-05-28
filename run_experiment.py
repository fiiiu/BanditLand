

import BanditExperiment


subject='test'

be=BanditExperiment.BanditExperiment(subject=subject, payrates='Input/payrates.txt')

be.run()
be.save() 
 