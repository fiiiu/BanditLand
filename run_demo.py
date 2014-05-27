

import parameters
import BanditExperiment

sub='prueba'

bedemo=BanditExperiment.BanditExperiment(subject=sub+'_demo', demo=True)
bedemo.run()
bedemo.save() 
 
#be.run(1)
#be.save()

#be.report()     