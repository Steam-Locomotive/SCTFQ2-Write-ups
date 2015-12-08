## Ubuntor - 55 (Recon) ##

#### Write-up by GenericNickname

Created: 2015-12-08

### Problem ###

Find out **about** me.

### Hint ###

It's all ***about*** me!

## Answer ##

### Overview ###

Figure out the flag based on the information Ubuntor has given.

### Details ###

Both the description and the hint emphasize the word about, so I instantly decided it must be related to the about page of the competition. I also googled Ubuntor, which brought up the github of Samuel Kim. Sure enough, on the about page, Samuel Kim's profile picture on the about page looks like a QR code, but the entire thing can't be seen.

Viewing the image will give you the full QRCode: 
<br/>
![Samuel Kim](http://sctf.io/img/team/SamuelKim.jpg)

Decoding the QR code gives some base64 text, which can be decoded using python. Looking at the base64 reveals that the base64 encoded text is actually the bytes of a png file, so saving it as one gets this image:
<br/>
![Ovaltine](/recon/ubuntor/ovaltine.png)
<br/>
Unfortuantely, this doesn't work as the flag, so there is more work to do. Downloading the original QR code and looking at it in either a hex editor or notepad++ reveals flag.txt towards the bottom of the file. This suggests that the image also contains a zip file, so changing the extension to .zip and opening it in a program such as 7zip will show flag.txt as its contents.

Trying to open flag.txt promopts the user for a password, and the first thing I tried was the message from the PNG we found earlier: `BE SURE TO DRINK YOUR OVALTINE`. This opens flag.txt and gives the flag.
### Flag ###

    sctf{all_about_the_ctf}


