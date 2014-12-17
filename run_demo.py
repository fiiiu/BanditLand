
import sys
import BanditExperiment

if len(sys.argv)>1:
    subject=sys.argv[1]
else:
    subject='tamara'

bedemo=BanditExperiment.BanditExperiment(subject=subject+'_demo', demo=True)
bedemo.run()
bedemo.save() 
 