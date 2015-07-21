import alphasign
import sys
import time
import urllib2
import random

def labelgen():
  l=32
  while l < 0x7f:
    yield chr(l)
    l+=1
    if l==0x30:
      l=0x36  
    if l==0x3f:
      l=0x40 



def update_sign():

        sign = alphasign.Serial(device='/dev/ttyUSB0')
        sign.connect()
        time.sleep(1)
        last_payload = ''

        while True:
            success=False
            
            try:
                # fetch new-line separated plain text from Interweb
                payload = urllib2.urlopen("https://server.appletonmakerspace.org/wiki/doku.php?id=sign_text&do=export_raw").read()
                success=True
            except Exception as e:
                payload = 'net err: '+str(e)

            # alert bystanders with beep when we update
            if payload == last_payload:
                t=txts[:]
                random.shuffle(t)
                sign.set_run_sequence(t)
            else:
                sign.beep(frequency=20, duration=1)
                last_payload = payload

                # loop over each line of plain text, displaying for 10 seconds
                txts=[]
                strs=[]
                l=labelgen()
                for line in payload.splitlines():
                    line = line.strip()
                    if not line:
                       continue
#                str = alphasign.String(line)
#                strs.append(str)
                    txts.append(alphasign.Text(line,mode=alphasign.modes.AUTOMODE, label=next(l)))

                sign.clear_memory()
                sign.allocate(txts+strs)
                for obj in txts + strs:
                    sign.write(obj)

                sign.set_run_sequence(txts[:])
                
                                
            time.sleep(10)
            if success:
                time.sleep(110)

if __name__ == "__main__":
    update_sign()

