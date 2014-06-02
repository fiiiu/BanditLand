
import sys
import BanditExperiment

if len(sys.argv)>1:
    subject=sys.argv[1]
else:
    subject='jose'


be=BanditExperiment.BanditExperiment(subject=subject, payrates='Input/payrates.txt')

be.run()
be.save() 
 