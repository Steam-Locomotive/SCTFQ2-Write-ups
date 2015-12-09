## Pizazz - 190 (Reversing) ##
#### Writeup by r3ndom_ #####
Created: 2015-12-8

### Problem ###
Can you tell me the flag? the output of running this program was:

`221.164.100.10.237.97.167.177.205.54.30.53.124.232.78.134.215.10.37.45.30.244.131.235.116.131.237.237.85.27.210.205.35.76.5.5.210.102.157.157.3.96.114.25.91.238.192.`

### Hint ###
None

## Answer ##

### Overview ###
Brute force the flag.

### Details ###

Here is all my reversing work on the pizazz function.

tl;dr : They have a dictionary of 0xff bytes (grid) that they then grab variables from and move stuff around after that is then printed as a number. This creates the string.

```asm
loc_80484AE:                            ; CODE XREF: main+17j
                mov     eax, [eax+4]    ; get the argv list
                mov     eax, [eax+4]    ; get the first param ptr
                mov     [ebp+var_C], eax ; param is stored in var_c
                mov     [ebp+var_18], 0

loc_80484BE:                            ; DATA XREF: .data:tbl_1641o
                mov     eax, [ebp+var_18]
                lea     edx, [eax+1]
                mov     [ebp+var_18], edx ; var_18++
                mov     edx, [ebp+var_C]
                add     eax, edx        ; eax = input[iter]
                movzx   eax, byte ptr [eax]
                test    al, al          ; eax = eax[0]
                setz    al
                movzx   eax, al         ; eax = eax == 0 ? 1 : 0;
                mov     eax, tbl_1641[eax*4]
                nop                     ; jmp table whoooo

loc_80484DF:                            ; CODE XREF: main+1A5j main+1D7j
                jmp     eax
; ---------------------------------------------------------------------------

loc_80484E1:                            ; DATA XREF: .data:0804A184o
                sub     [ebp+var_18], 1 ; var_18 holds the number of characters
                mov     [ebp+var_14], 0 ; var_14 is the iter

loc_80484EC:                            ; DATA XREF: .data:tbl2_1644o
                mov     edx, [ebp+var_C] ; edx = string
                mov     eax, [ebp+var_14] ; eax = iter
                add     eax, edx        ; eax = input[iter]
                movzx   eax, byte ptr [eax]
                movsx   eax, al
                and     eax, 2          ; eax &= 2
                sar     eax, 1          ; eax >>= 1
                mov     ecx, eax        ; ecx = eax
                mov     edx, [ebp+var_C] ; edx = str
                mov     eax, [ebp+var_14] ; eax = iter
                add     eax, edx        ; eax = input[iter]
                movzx   eax, byte ptr [eax]
                movsx   eax, al
                and     eax, 8          ; eax &= 8
                sar     eax, 2          ; eax >>= 2
                or      ecx, eax        ; ecx |= eax
                mov     edx, [ebp+var_C]
                mov     eax, [ebp+var_14]
                add     eax, edx        ; eax = str[iter]
                movzx   eax, byte ptr [eax]
                movsx   eax, al
                and     eax, 20h        ; eax &= 0x20
                sar     eax, 3          ; eax >>= 3
                or      ecx, eax        ; ecx |= eax
                mov     edx, [ebp+var_C]
                mov     eax, [ebp+var_14]
                add     eax, edx
                movzx   eax, byte ptr [eax] ; eax = input[iter]
                movsx   eax, al
                and     eax, 80h        ; eax &= 0x80
                sar     eax, 4          ; eax >>= 4
                or      eax, ecx        ; eax |= ecx
                mov     [ebp+var_1B], al ; var_1b = eax
                mov     edx, [ebp+var_C]
                mov     eax, [ebp+var_14]
                add     eax, edx
                movzx   eax, byte ptr [eax]
                and     eax, 1          ; eax = 1 & (input[iter])
                mov     ecx, eax        ; ecx = eax
                mov     edx, [ebp+var_C]
                mov     eax, [ebp+var_14]
                add     eax, edx
                movzx   eax, byte ptr [eax]
                movsx   eax, al
                and     eax, 4          ; eax = (4 & input[iter]) >> 1
                sar     eax, 1
                or      ecx, eax        ; ecx |= eax
                mov     edx, [ebp+var_C]
                mov     eax, [ebp+var_14]
                add     eax, edx
                movzx   eax, byte ptr [eax]
                movsx   eax, al
                and     eax, 10h
                sar     eax, 2          ; eax = (0x10 & input[iter]) >> 2
                or      ecx, eax        ; |
                mov     edx, [ebp+var_C]
                mov     eax, [ebp+var_14]
                add     eax, edx
                movzx   eax, byte ptr [eax]
                movsx   eax, al
                and     eax, 40h
                sar     eax, 3          ; eax = (0x40 & input[iter]) >> 3
                or      eax, ecx        ; |
                mov     [ebp+var_19], al
                movzx   edx, [ebp+var_1B]
                movzx   eax, [ebp+var_19]
                shl     edx, 4
                add     eax, edx        ; grid[var_19 + (var_1b << 4)]
                add     eax, offset grid
                movzx   eax, byte ptr [eax]
                movzx   eax, al
                sub     esp, 8
                push    eax
                push    offset format   ; "%d."
                call    _printf
                add     esp, 10h
                movzx   eax, [ebp+var_1B] ; eax = var_1b
                shl     eax, 4          ; eax <<= 4
                add     eax, offset grid ; eax = grid+eax
                movzx   eax, byte ptr [eax] ; eax = *eax
                mov     [ebp+var_1A], al ; 1a = grid[var_1b << 4]
                mov     [ebp+var_10], 1 ; 10 = 1

loc_80485DE:                            ; DATA XREF: .data:tbl3_1649o
                movzx   edx, [ebp+var_1B] ; edx = 1b
                mov     eax, [ebp+var_10] ; eax = 10
                lea     ecx, [eax-1]    ; ecx = eax - 1
                movzx   eax, [ebp+var_1B] ; eax = 1b
                shl     eax, 4
                mov     ebx, eax
                mov     eax, [ebp+var_10] ; eax = 10
                add     eax, ebx        ; grid[ _10 + (1b << 4) ]
                add     eax, offset grid
                movzx   eax, byte ptr [eax]
                shl     edx, 4
                add     edx, ecx        ; grid[ (1b << 4) + (_10 - 1) ]
                add     edx, offset grid
                mov     [edx], al       ; set below to above
                add     [ebp+var_10], 1 ; ++_10
                cmp     [ebp+var_10], 0Fh
                setnle  al              ; eax = (_10 > 0xF) ? 1 : 0
                movzx   eax, al
                mov     eax, tbl3_1649[eax*4] ; loop if _10 < 0xF
                jmp     loc_80484DF
; ---------------------------------------------------------------------------

loc_8048625:                            ; DATA XREF: .data:0804A18Co
                movzx   eax, [ebp+var_1B]
                shl     eax, 4
                add     eax, 0Fh
                lea     edx, grid[eax]  ; edx = &grid[ (1b << 4) + 0xf]
                movzx   eax, [ebp+var_1A]
                mov     [edx], al       ; *edx = 1a
                add     [ebp+var_14], 1 ; _14 += 1
                mov     eax, [ebp+var_14]
                cmp     eax, [ebp+var_18]
                setnb   al              ; eax = _14 >= _18 ? 1 : 0
                movzx   eax, al
                mov     eax, tbl2_1644[eax*4]
                jmp     loc_80484DF
loc_8048657:                            ; DATA XREF: .data:0804A194o
                sub     esp, 0Ch
                push    0Ah             ; c
                call    _putchar
                add     esp, 10h
                mov     eax, 0

loc_8048669:
            ; Function end.
```

So based on that here's a quick brute forcer I wrote. This is possible because each character is only dependant on the characters before it and not after. As such we can just make something that progressively checks each character.

```python
import os
import random
import time
correct = "221.164.100.10.237.97.167.177.205.54.30.53.124.232.78.134.215.10.37.45.30.244.131.235.116.131.237.237.85.27.210.205.35.76.5.5.210.102.157.157.3.96.114.25.91.238.192."
answer = ""
check='flag{a'
invalid_chars = [' ', '&', '\'', '(', ')', '*', '`', '\\', '^', '~', '|', '>', '<', ':', ';', '"', '\t', '\n']
def gen_char(prev):
	num = ord(prev)
	num += 1
	if(num > 127):
		num = 0
	#print num
	while(chr(num) in invalid_chars or num > 255 or num < 1):
		num+=1
		if(num > 127):
			num = 0
	return chr(num)

previous_ch = 'a'
while answer != correct:
	answer = os.popen('./pizazz '+check).read()
	answer = answer[:len(answer)-1]
	if("no " in answer or answer != correct[:len(answer)]):
		previous_ch = check[len(check) - 1:]
		check = check[:len(check) - 1]
		check += gen_char(previous_ch)
	else:
		print check
		check += gen_char(chr(random.randint(0,255)))

print check
print answer
print correct
```

Run that in the same directory as pizazz on a linux machine and you'll get the flag.

### Flag ###

    flag{Z-0rder_curv3s_and_janky_p3rmutati10ns_FTW}
    
### Attempted Decompilation ###

```c
typedef unsigned char byte;

byte grid[0xff];

byte mod_char(char ch)
{
	byte b0 = (ch & 2) >> 1;
	byte b1 = (ch & 8) >> 2;
	byte b2 = (ch & 0x20) >> 3;
	byte b3 = (ch & 0x80) >> 4;
	byte bres = b0 | b1 | b2 | b3;

	byte c0 = (ch & 1);
	byte c1 = (ch & 4) >> 1;
	byte c2 = (ch & 0x10) >> 2;
	byte c3 = (ch & 0x40) >> 3;
	byte cres = c0 | c1 | c2 | c3;

	int index = cres + (bres << 4);
	byte ret = grid[index];

	byte _1a = grid[bres << 4];
	for (int i = 1; i <= 0xf; ++i)
	{
		grid[(bres << 4) + i - 1] = grid[(bres << 4) + i];
	}
	grid[(bres << 4) + 0xf] = _1a;

	return ret;
}

int get_index(char ch)
{
	byte b0 = (ch & 2) >> 1;
	byte b1 = (ch & 8) >> 2;
	byte b2 = (ch & 0x20) >> 3;
	byte b3 = (ch & 0x80) >> 4;
	byte bres = b0 | b1 | b2 | b3;

	byte c0 = (ch & 1);
	byte c1 = (ch & 4) >> 1;
	byte c2 = (ch & 0x10) >> 2;
	byte c3 = (ch & 0x40) >> 3;
	byte cres = c0 | c1 | c2 | c3;

	int index = cres + (bres << 4);
	return index;
}

int arr[] = { 0x5F4BB48, 0x70D06AB, 0x76E1343, 0x845B466, 0x8C4EAE, 0x2F39F, 0x0F919BD5, 0x0BAE5F7A, 0x40EF15D, 0x4A5A670, 0x0F11A9CF, 0x0C48527, 0x1BEB2D7, 0x0D882E67, 0x857D627, 0x6F965D6, 0x4E9D3B8, 0x0DDCB1D, 0x8E66640, 0x3E1E8D3, 0x4230865, 0x412325D, 0x33DD506, 0x35CDE80, 0x0C059781, 0x0C88B7BA, 0x0F6A4A2F, 0x554C327, 0x1FDFE09, 0x2268560, 0x0F474912, 0x36EED2, 0x2CE7470, 0x9E28B02, 0x8A807AE, 0x27AED1D, 0x0B90B8F3, 0x0C98890D, 0x0DB37A5C, 0x17FF4FA, 0x54ABAA3, 0x10D3B84, 0x0ACBB43D, 0x0BCA9772, 0x47FE39, 0x443CA39, 0x6CFEA0F, 0x1C9987E, 0x0B7CB73F, 0x0B6ADF03, 0x5175B58, 0x0CF58AF3, 0x13B2D49, 0x4DC32B6, 0x7DE45C, 0x63982AF, 0x0FBC129B, 0x0E911269, 0x0C692CAC, 0x0A8F557B, 0x1814029, 0x0C50F6B0, 0x5CC781E, 0x1D16699 };

int main(int argc, char** argv)
{
    if(argc < 2)
    {
        puts(">_>");
        return 1;
    }
    memcpy(grid, arr, sizeof(grid));
    size_t stLen = strlen(argv[1]);
    for(int i = 0; i < stLen; ++i)
    {
        printf_s("%d.", mod_char(argv[1][i]));
    }
    return 0;
}
```
