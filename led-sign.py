import alphasign
import sys
import time
import urllib2

def update_sign():

        sign = alphasign.Serial(device='/dev/ttyUSB0')
        sign.connect()
        sign.clear_memory()

        # create an empty alphasign.String
        alpha_str = alphasign.String()

        # create a single alphasign.Text object with a placeholder for our alphasign.String
        alpha_txt = alphasign.Text(alpha_str.call(),mode=alphasign.modes.COMPRESSED_ROTATE)

        # allocate memory for these objects on the sign
        sign.allocate((alpha_str,alpha_txt))

        # tell sign to only display the text part
        sign.set_run_sequence((alpha_txt,))

        # write objects
        for obj in (alpha_str,alpha_txt):
            sign.write(obj)

        # This gives time for the serial write to complete before we issue the next write.
        time.sleep(5)

        last_payload = ''

        while True:

            try:
                # fetch new-line separated plain text from Interweb
                payload = urllib2.urlopen("https://server.appletonmakerspace.org/beta-brite-message-file.txt").read()
            except Exception:
                payload = 'HALP! Internet down!?'

            # alert bystanders with beep when we update
            if payload != last_payload:
                sign.beep(frequency=20, duration=1)
                last_payload = payload

            # loop over each line of plain text, displaying for 10 seconds
            for line in payload.splitlines():
                alpha_str.data = line
                sign.write(alpha_str)
                time.sleep(10)

            # when the last line is read, the while loop repeats and fetches again

if __name__ == "__main__":
    update_sign()

