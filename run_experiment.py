

import BanditExperiment


be=BanditExperiment.BanditExperiment('alejo', payrates='load')

be.run()
be.save()

#be.run(1)
#be.save()

#be.report()