## &lambda;1 - (Reversing) ##
#### Writeup by Jonathan S

Created: 2015-12-12

### Problem ###

I've got this Haskell program here, but for some reason, it just won't
complete. Can you figure out the correct output for me?

### Hint ###

I think it has something to do with `BPF_IF_PW^^VSNXAPCZL^XKM`...?

## Answer ##

### Overview ###

Reverse engineer the given program to find what it is computing in a very
unoptimized way and calculate that value more efficiently.

### Details ###

#### Intro ####

The binary, which we know came Haskell source code, was compiled with the
industry standard Haskell compiler, the [Glasgow Haskell Compiler][GHC],
as evidenced by the numerous occurances of the string `GHC` in symbol names
and the fact that basically no one uses anything but GHC these days.

Now, before we begin, there are some important facts to realize about Haskell:

- Haskell is a [functional programming][FP] language. This means that functions
  are treated as first-class objects that can be passed around and manipulated
  just like any piece of data. Moreover, instead of programming by writing down
  a list of commands that the computer will execute, functions are defined in
  terms of what functions are applied to pieces of data (in fact, only having
  the ability to define and apply functions is enough to compute anything
  computable, as shown by [lambda calculus][LC], a mathematical system that
  underpins much of functional programming).

- Haskell is more specifically a [pure][Pure] functional programming language.
  This means that nearly every piece of code will not use mutable variables,
  will not have any side effects (like input or output), will produce the same
  result every time it is run, and won't care when in the program's execution
  it is run. This will be incredibly useful for analyzing our program, as we
  can just look at individual expressions and how they are computed, not caring
  when and where those expressions are called.

- Haskell has non-strict semantics, which are implemented in GHC using
  [lazy evaluation][Lazy]. This means that expressions are only evaluated once
  the program has an immediate need for them, delaying any calculation to the
  last moment possible. This, more than any of the other properties, messes up
  execution order enourmously and almost single-handedly renders conventional
  debuggers basically useless.

- Haskell is incredibly generic-heavy, and for maximum flexibility (including
  support for [polymorphic recursion][PolyRec]), GHC stores and passes around
  at runtime certain information about a generic type that might be filled in
  at compile time or ignored in other languages.

- Haskell programmers often like to use [point-free style][PointFree] in their
  programs, manipulating and compsing functions instead of directly talking
  about data.

All these properties lead to Haskell having a dramatically different execution
model from something like C and from how the CPU actually executes. As a result,
GHC does many things completely differently from C, including a distinct calling
convention, a manually managed stack, and a specialized memory system and
garbage collector. Code produced by GHC is very distinctive, and will not look
anything like something produced by GCC, and debuggers will not aid understanding
at all.

[FP]: https://en.wikipedia.org/wiki/Functional_programming
[GHC]: https://www.haskell.org/ghc/
[Lazy]: https://en.wikipedia.org/wiki/Lazy_evaluation
[LC]: https://en.wikipedia.org/wiki/Lambda_calculus
[PointFree]: https://en.wikipedia.org/wiki/Tacit_programming
[PolyRec]: https://en.wikipedia.org/wiki/Polymorphic_recursion
[Pure]: https://en.wikipedia.org/wiki/Purely_functional

#### Aside: The compilation process ####

GHC actually sends a Haskell program through 3 intermediate representations before
generating any assembly. Haskell source is transformed into Core, which is
essentially a desugared, explicitly typed, and name-resolved version of Haskell.
Then, Core is lowered into STG, or Spineless Tagless G-machine code (a name that
is somewhat incorrect now that GHC has incorporated [pointer tagging][PtrTag]).
STG is still functional, but with all temporaries and thunks (expressions to be
lazily evaluated) explicitly spelled out. Finally, STG is converted into C--, a
low level language designed as a generic language for compilers to target, that,
despite its goals, is only targeted by GHC. C--, as implied by its name, is quite
like C and readily translates to assembly.

When optimizations are disabled, all of these transformations (except possibly
from STG to C--) just involve logical desugarings and don't introduce any random
new complexity. As such, we will ignore any intermediate representations for the
sake of this write-up, acting as if GHC went directly from Haskell to assembly.

For more details, see the GHC Wiki [here][CompPipe].

[CompPipe]: https://ghc.haskell.org/trac/ghc/wiki/Commentary/Compiler/HscMain
[PtrTag]: https://ghc.haskell.org/trac/ghc/wiki/Commentary/Rts/HaskellExecution/PointerTagging

#### Entering the program ####

With all of that out of the way, let's start on analyzing the acutal binary. Load
it up in your favorite disassembler (note that IDA, at least, balks at the foreign
character in a file name), and you should find that the programs starts much as a
C program might: after a short few steps in `_start` and `__libc_start_main`, the
`main` function is called. We inspect it:

```asm
    public main
main:          ; DATA XREF: _start+17 o
    push    ebp
    mov     ebp, esp
    and     esp, -16
    sub     esp, 48
    mov     eax, ds:defaultRtsConfig
    mov     edx, ds:dword_80BEE64
    mov     [esp+40], eax
    mov     [esp+44], edx
    mov     dword ptr [esp+40], 1
    mov     eax, [esp+40]
    mov     edx, [esp+44]
    mov     [esp+12], eax
    mov     [esp+16], edx
    mov     dword ptr [esp+8], offset ZCMain_main_closure
    mov     eax, [ebp+12]
    mov     [esp+4], eax
    mov     eax, [ebp+8]
    mov     [esp], eax
    call    hs_main
```

We might be initially tempted to continue down the rabbit hole looking at `hs_main`.
However, this would be a mistake, as the only code we actually care about is behind
`ZCMain_main_closure`. Remember that Haskell is implemented lazily, so to execute
anything, the unevaluated expression needs to be stored, then demanded later by
something that needs the expression. In this case, `ZCMain_main_closure` is the
unevaluated expression corresponding to the whole program, and `hs_main` is just
responsibly for demanding that expression. In general, anything labeled `_closure`
is a reference to an unevaluated, top-level expression.

Therefore, we dive into `ZCMain_main_closure` and find that it is in fact only a wrapper
around the actual implementation, `ZCMain_main_info`:

```asm
ZCMain_main_closure dd offset ZCMain_main_info ; DATA XREF: .text:0804CA7B o
```

All objects in Haskell are represented as pointers to pointers to code that evaluates the
expression. This extra layer of indirection allows for a crucial optimization where, after
an expression is evaluated, it is replaced by a simplified expression that just returns
the evaluated answer directly. Since we don't have to care about when things are evaluated,
we will just skip over any details pretaining to this, and just go staight into
`ZCMain_main_info`.

#### Our first Haskell expression ####

Disassembling `ZCMain_main_info` gives the following, which we will take chunk by chunk:

```asm
    lea     eax, [ebp-12]
    cmp     eax, [ebx+84]
    jb      short loc_804CA42
    add     edi, 8
    cmp     edi, [ebx+92]
    ja      short loc_804CA3B
    mov     dword ptr [edi-4], offset stg_CAF_BLACKHOLE_info
    mov     eax, [ebx+100]
    mov     [edi], eax
    lea     eax, [edi-4]
    push    eax
    push    esi
    push    ebx
    call    newCAF
    add     esp, 12
    test    eax, eax
    jz      short loc_804CA45
    mov     dword ptr [ebp-8], offset stg_bh_upd_frame_info
    lea     eax, [edi-4]
    mov     [ebp-4], eax
    mov     esi, offset base_GHCziTopHandler_runMainIO_closure
    mov     dword ptr [ebp-12], offset Main_main_closure
    add     ebp, -12
    jmp     stg_ap_p_fast
```

We start at the top.

```asm
    lea     eax, [ebp-12]
    cmp     eax, [ebx+84]
    jb      short loc_804CA42
```

This is a stack overflow check. As we mentioned before, GHC manages its own stack, and the tip of this
stack is stored in the register `ebp`. This short section of assembly, which comes at the beginning of
nearly every section in the whole program, just checks that the stack pointer does not run past the
end of the stack, the value stored in `[ebx+84]`.

```asm
    add     edi, 8
    cmp     edi, [ebx+92]
    ja      short loc_804CA3B
```

Looking very similar to the stack overflow check, this is the allocation code and heap overflow check. It
doesn't look very similar to what you might see in many other languages, with a call to a fairly complex
`malloc` function, instead only adding 8 to `edi`. This is because [GHC's][GHCGC0] [garbage][GHCGC1]
[collector][GHCGC2] is a [copying][CopyGC], and therefore [compacting][CompactGC] collector, which makes finding
free memory trivial. Instead of having some complicated division tracked through allocator data structures of
free and allocated memory, everything less than `edi` is allocated, while everything greater than `edi` is free.
Therefore, the `add edi, 8` is in fact allocating 8 bytes. The other two instructions, similiarly to the
stack overflow check, are just checking for heap overflow and possibly initiating a collection.

```asm
    mov     dword ptr [edi-4], offset stg_CAF_BLACKHOLE_info
    mov     eax, [ebx+100]
    mov     [edi], eax
```

This code is putting some values into the heap spots that were just allocated. We don't really have to worry
about either value, but the `stg_CAF_BLACKFOLE_info` is interesting. When evaluating an expression, GHC
temporarily replaces that expression with what is known as a [black hole][BlackHole]. This has two helpful
side effects. First, if the expression is actually an infinite loop, referring to itself (as in `loop = loop`),
then this black hole will get evaluated and, instead of hanging in a hard to debug way, the program will
print out `<<loop>>` and crash. Second, if two threads attempt to evalutate the same expression at the same time,
one thread will see the black hole and not do the same work that the other thread is doing. The storing
of `stg_CAF_BLACKHOLE_info` is most of this mechanism.

```asm
    lea     eax, [edi-4]
    push    eax
    push    esi
    push    ebx
    call    newCAF
    add     esp, 12
    test    eax, eax
    jz      short loc_804CA45
```

Here, a new [Constant Applicative Form][CAF] is being allocated. A CAF, for most purposes, is just a top level
expression, and specifically one that isn't a function. These are special because they want to be evaluated once
throughout the whole lifetime of a program. The details that make CAFs different from other expressions aren't
really important to us. The one thing of note is that the address of the just allocated black hole is passed to
`newCAF` so that it can finish initialization.

```asm
    mov     dword ptr [ebp-8], offset stg_bh_upd_frame_info
    lea     eax, [edi-4]
    mov     [ebp-4], eax
```

Remember that GHC's stack is tracked using `ebp`, so this code is putting some stuff onto the stack. In particular,
since GHC manages its own stack, it also needs to put addresses that function calls will return to on the stack
manually. This is what this piece of code is doing. When the function call coming up returns, it will jump to
`stg_bh_upd_frame_info`. This function is called an [update (stack) frame][UpdateFrame], hence its name.

As mentioned before, while an expression is being evaluated, it gets replaced by a blackhole. However, for laziness
to work properly, it needs to remove the blackhole and put the final, evaluated expression in its place. This is
exactly what `stg_bh_upd_frame_info` does. Note that immediately above this update function is the address where
`stg_CAF_BLACKHOLE_info` was stored, giving the update frame the information it needs to replace that blackhole.
Once the evaluated expression is stored, `stg_bh_upd_frame_info` will return to the address immediately preceding it,
at `[ebp]` - in general, the place an expression needs to return to will be at `[ebp]`.

```asm
    mov     esi, offset base_GHCziTopHandler_runMainIO_closure
    mov     dword ptr [ebp-12], offset Main_main_closure
```

Here we set up the function we want to call and its argument. `base_GHCziTopHandler_runMainIO_closure` is stored in
`esi`, the location for the function to be called, while its argument, `Main_main_closure`, like most languages is put
at the bottom of the stack.

At this point is starts being useful to decode these cryptic names of expressions. Every closure
comes in 4 parts, separated by underscores. The first part, `base` in this case, refers to the package that the expression
came from. In this case, `base` is the core standard library for Haskell. The second part, `GHCziTopHandler`, is the module
that the expression came from. The `zi` in there is actually just [code][SymbolNames] for a period, used because periods in
symbol names cause issues (compiled C++ files will also have this slightly cryptic mess). Therefore, the module in this case
is `GHC.TopHandler`. For the full list of rules for decoding symbols, see [here][SymbolNames]. The third part of a name is the
actual name of the expression being referenced, in this case `runMainIO`. The final part is just `closure` or `info`, depending
on whether the symbol is referring to the actual code implementing the expression (`info`) or just a memory location pointing to
the `info`.

Sometimes, as in `Main_main_closure`, not every part of the name is present. Since `Main_main_closure` is user code, it doesn't
have a package associated to it, and is just `main` in the module `Main`. This allows us to very easily identify library code.


```asm
    add     ebp, -12
```

Here we actually update the stack, moving its tip past the 12 bytes we used.

```asm
    jmp     stg_ap_p_fast
```

Finally, we jump into the actually function that will perform function application. This function is part of GHC's
[generic apply][GenericApply] mechanism, used when GHC isn't certain at compile time that a function is fully evaluated
and called on exactly as many arguments as it needs. Because this file was compiled without optimization, almost every
single function call will use this mechanism.

`stg_ap_p_fast` takes the function to apply in `esi` (hence why `runMainIO` was stored there earlier) and the argument it
needs on the stack. As denoted by the single `p` in its name, we are passing a single pointer argument (`main`) to `runMainIO`.
In the future, we will often see, for example, `stg_ap_pp_fast`, which takes 2 pointer arguments.

In total, this whole section boils down the following statement:

```haskell
:Main.main = runMainIO Main.main
```

[BlackHole]: http://mainisusuallyafunction.blogspot.com/2011/10/thunks-and-lazy-blackholes-introduction.html
[CAF]: https://wiki.haskell.org/Constant_applicative_form
[CopyGC]: https://en.wikipedia.org/wiki/Cheney's_algorithm
[CompactGC]: https://en.wikipedia.org/wiki/Mark-compact_algorithm
[GenericApply]: https://ghc.haskell.org/trac/ghc/wiki/Commentary/Rts/HaskellExecution/FunctionCalls#Genericapply
[GHCGC0]: http://blog.ezyang.com/2011/04/how-the-grinch-stole-the-haskell-heap/
[GHCGC1]: http://community.haskell.org/~simonmar/bib/local-gc-2011_abstract.html
[GHCGC2]: http://community.haskell.org/~simonmar/bib/parallel-gc-08_abstract.html
[UpdateFrame]: https://ghc.haskell.org/trac/ghc/wiki/Commentary/Rts/Storage/Stack
[SymbolNames]: https://ghc.haskell.org/trac/ghc/wiki/Commentary/Compiler/SymbolNames

#### Entering user code: `Main.main` ####

We next enter `Main.main` (or `Main_main_closure`), the first expression we see that the programmer actually wrote. `runMainIO`
is basically useless to us because it is just a library function, and one that basically just [starts up the program][runMainIO].

```asm
    lea     eax, [ebp-16]
    cmp     eax, [ebx+84]
    jb      short loc_804C9D9
    add     edi, 8
    cmp     edi, [ebx+92]
    ja      short loc_804C9D2
    mov     dword ptr [edi-4], offset stg_CAF_BLACKHOLE_info
    mov     eax, [ebx+100]
    mov     [edi], eax
    lea     eax, [edi-4]
    push    eax
    push    esi
    push    ebx
    call    newCAF
    add     esp, 12
    test    eax, eax
    jz      short loc_804C9DC
    mov     dword ptr [ebp-8], offset stg_bh_upd_frame_info
    lea     eax, [edi-4]
    mov     [ebp-4], eax
    mov     esi, offset base_GHCziBase_zd_closure
    mov     dword ptr [ebp-12], offset sBr_closure
    mov     dword ptr [ebp-16], offset sBs_closure
    add     ebp, -16
    jmp     stg_ap_pp_fast
```

We see the same stack and heap checks, blackhole creation, CAF initialization, and update frame creation as we did in `:Main.main`.
The change is the meat of what we are looking for - what function is applied to what. In this case, we have `base`'s `GHC.Base.($)`
applied to `sBs` and `sBr`. Note that since `$` (a convienience function that applies a function to an argument, useful for avoiding
parentheses) takes two arguments, we are using `stg_ap_pp_fast`, not `stg_ap_p_fast`. In total, we add the line

```haskell
Main.main = sBs $ sBr
```

[runMainIO]: https://hackage.haskell.org/package/base-4.6.0.1/docs/src/GHC-TopHandler.html#runMainIO

#### `sBs` ####

Jumping into `sBs_info`, we see much of the same, but some interesting things happen when filling the stack and heap:

```asm
    mov     dword ptr [edi-12], offset sB8_info
    mov     dword ptr [edi-4], offset sBm_info
    lea     eax, [edi-12]
    mov     [edi], eax
    mov     esi, offset base_GHCziBase_zi_closure
    lea     eax, [edi-3]
    mov     [ebp-12], eax
    mov     dword ptr [ebp-16], offset base_SystemziIO_putStrLn_closure
    add     ebp, -16
    jmp     stg_ap_pp_fast
```

Following the patterns we saw before, `GHC.Base.(.)` is being called on two arguments, the first being `System.IO.putStrLn`, but the
second is a little stange. For the second argument, there is a pointer into the heap, specifically `[edi-3]`.

Now, we didn't store anything at `[edi-3]` - every store done was at an aligned address, at multiple of four. However, as an optimization,
GHC uses the lower 2 bits (3 on a 64 bit machine) to [tag pointers][TagPtr]. Having zeroed out low bits means that the pointed-to
expression might be unevalutated, but any other tag bits mean that the expression is evaluated, the specific tag value telling us about
what the evaluated expression. In this case, since `(.)` takes two functions as arguments, we know that the tag bits are tellings us
the arity (number of arguments) of the function passed, so `[edi-4]`, or `sBm`, must be a function of 1 argument.

The remaining interesting part of `sBs` is the 3 other heap words allocated - we store `sB8_info` and a pointer to that slot, and
`[edi-8]` is left empty, essentially giving `sBs` an extra word to store information about its evaluation status.

In total, we end up with something like

```haskell
:Main.main = runMainIO Main.main
Main.main = sBs $ sBr
sBs = let sB8 = ???
          sBm = ???
      in putStrLn . sBm
```

[TagPtr]: https://ghc.haskell.org/trac/ghc/wiki/Commentary/Rts/HaskellExecution/PointerTagging

#### `sB8` ####

`sB8_info` looks a little bit different from the previous expressions we have seen.

```asm
    lea     eax, [ebp-12]
    cmp     eax, [ebx+84]
    jb      short loc_804C6DE
    mov     dword ptr [ebp-8], offset stg_upd_frame_info
    mov     [ebp-4], esi
    mov     esi, offset ghczmprim_GHCziCString_unpackCStringzh_closure
    mov     dword ptr [ebp-12], offset cDX_str ; "BPF_IF_PW^^VSNXAPCZL^XKM"
    add     ebp, -12
    jmp     stg_ap_n_fast
```

Since it does no allocation, it only has a stack overflow check, and, since we have left the realm of top level expressions, we don't do any
of the CAF business that previous things had to deal with. We still set up the update frame, but the function we call and its argument are
slightly strange. We are now using `stg_ap_n_fast`, which signifies a function (here, `unpackCString#`) that takes a single non-pointer argument.
Calling this argument non-pointer is a little stange, as it is in fact a pointer, but looking at the [signature of `unpackCString#`][unpackCString],
we see that this function takes an `Addr#`, a special unboxed value that isn't like a normal Haskell object.

This `unpackCString#` business is automatically inserted by GHC every time there is a string literal in the Haskell source file, as an optimization.
Instead of storing it in Haskell format (a horribly inefficient linked list of pointers to characters), GHC just emits the more compact C-style string,
then inserts a call to `unpackCString#`. In particular, the C-style encoded string that is being unpacked into a Haskell-style string, stored at
`cDX_str`, is "BPF_IF_PW^^VSNXAPCZL^XKM", the string mentioned in the hint to the problem. We're on the right track! The result after inspecting
`sB8` is the following:

```haskell
:Main.main = runMainIO Main.main
Main.main = sBs $ sBr
sBs = let sB8 = "BPF_IF_PW^^VSNXAPCZL^XKM"
          sBm = ???
      in putStrLn . sBm
```

[unpackCString]: https://hackage.haskell.org/package/ghc-prim-0.4.0.0/docs/src/GHC-CString.html#unpackCString

#### `sBm` ####

`sBm_info` has the normal stack and heap check, but, as it is a function, does some interesting things after them:

```asm
    mov     dword ptr [edi-20], offset sDJ_info
    mov     eax, [ebp+0]
    mov     [edi-12], eax
    mov     dword ptr [edi-8], offset sDK_info
    mov     eax, [esi+3]
    mov     [edi], eax
    mov     esi, offset base_GHCziBase_zd_closure
    lea     eax, [edi-20]
    mov     [ebp+0], eax
    lea     eax, [edi-8]
    mov     [ebp-4], eax
    add     ebp, -4
    jmp     stg_ap_pp_fast
```

`sDJ` and `sDK` are stored on the heap, with empty words adjacent to them, as we saw before in `sBs`. The application code also works as we saw
before, applying `GHC.Base.($)` to `sDK` and `sDJ`. However, we are now using `[ebp+0]` as a valid stack slot to overwrite. This is because `sBm`
was passed its argument in `[ebp+0]` and needs to return to `[ebp+4]`. Previously, we were only dealing with simple expressions, not functions, so
`[ebp+0]` held to return address and could not be overridden, but now we have the extra space left for our argument. Now, just overwriting our argument
would be bad, so before doing so we copy it to the heap, putting it at `[edi-12]`.

After this, the one unexplained allocation is putting `[esi+3]` at `[edi]`. Crucial to this is that when a function is called, `esi` holds a pointer to
the function itself (this is related to why `stg_ap_??_fast` takes the function to apply in `esi`). This is useful, because, going back to `sBs`, `sBm`
was allocated on the heap just 4 bytes away from the pointer to `sB8`. The function location, plus 4 bytes, holds `sB8`, and `sBm` wants to reference
that string. Now, we don't use `[esi+4]`, instead using `[esi+3]`. This is because, as mentioned before, pointers are tagged, and pointers to functions
hold the arity of that function in the tag bits. Therefore, `esi` is actually pointing at `sBm` plus 1 byte (since `sBm` is running, it must be fully
evaluated), and `[esi+3]` is the correct location.

In conclusion, we now have:

```haskell
:Main.main = runMainIO Main.main
Main.main = sBs $ sBr
sBs = let sB8 = "BPF_IF_PW^^VSNXAPCZL^XKM"
          sBm x = let sDJ = ???
                      heap_x = x
                      sDK = ???
                      heap_sB8 = sB8
                  in sDK $ sDJ
      in putStrLn . sBm
```

#### `sDJ` ####

Once again in `sDJ` we see the stack check and the update frame, but the rest is a little different from what we've seen before:

```asm
    mov     eax, [esi+8]
    mov     [ebp-12], eax
    mov     dword ptr [ebp-16], offset stg_ap_p_info
    mov     dword ptr [ebp-20], offset base_GHCziShow_zdfShowInteger_closure
    add     ebp, -20
    jmp     base_GHCziShow_show_info
```

Instead of using the generic apply mechanism, this code jumps directly to [`GHC.Show.show`][Show], the function in Haskell that produces human readable
versions of values. Importantly, this function is generic, and can be applied to many different types. To implement these generic functions and tell `show`
which type of object it is being passed and how to display it, GHC uses a [typeclass dictionary][Dictionary]. For every type that implements the type
class (like an interface in other languages) `Show`, GHC generates a wrapper data structure that just contains every function that is part of `Show`.
the function `show` is then just an instance accessor function - it takes a single argument, the dictionary, and returns the function that actually
does the displaying of the type we care about.

Therefore, `show`, which we jump to, takes a single argument, `$fShowInteger` (this is the [mangled name][DictName] for the implementation of `Show` for
the type `Integer`). `show` stores its return value (the actual function for displaying `Integer`s) in `esi`, then jumps to the return address given to it,
`stg_ap_p_info`. This leads to another interesting thing about `sDJ`. By putting `stg_ap_p_info` on the stack, we make it so that whatever `show` returns
is then called on one more argument, stored just beyond it in `[ebp-12]`. Through this double-application process, we all in all display the integer stored
at `[ebp-12]` and return that result.

Now, just like in `sBm`, we have a reference to `esi`, this time pulling from `[esi+8]`. Note that since we are running an thunk (unevaluated expression), not
a function, we know we have no tag bits, and `esi` points directly at the heap location containing `sDJ`. Going back to `sBm` where `sDJ` was allocated,
we find that `[esi+8]` refers to the argument of `sBm`, copied into the heap. This reference to `sBm` is then copied into `[ebp-12]`, the place for the
integer that we will display.

All together, we end up with:

```haskell
:Main.main = runMainIO Main.main
Main.main = sBs $ sBr
sBs = let sB8 = "BPF_IF_PW^^VSNXAPCZL^XKM"
          sBm x = let sDJ = show heap_x
                      heap_x = x
                      sDK = ???
                      heap_sB8 = sB8
                  in sDK $ sDJ
      in putStrLn . sBm
```

[Dictionary]: http://okmij.org/ftp/Computation/typeclass.html
[DictName]: https://github.com/ghc/ghc/blob/c12fc2e68d0781c82241fb895f6022518321b5ad/compiler/basicTypes/OccName.hs#L533
[Show]: https://hackage.haskell.org/package/base-4.6.0.1/docs/src/GHC-Show.html#Show

#### `sDK` ####

For the first time, `sDK` introduces nothing new, and following through everything done in previous sections, we see that `zipWith` is called on two arguments,
the first being a newly allocated `sBh` and the second being the previously allocated reference to `sB8`

Therefore, we have:

```haskell
:Main.main = runMainIO Main.main
Main.main = sBs $ sBr
sBs = let sB8 = "BPF_IF_PW^^VSNXAPCZL^XKM"
          sBm x = let sDJ = show heap_x
                      heap_x = x
                      sDK = let sBh = ???
                            in zipWith sBh heap_sB8
                      heap_sB8 = sB8
                  in sDK $ sDJ
      in putStrLn . sBm
```

Going deeper into this rabbit hole is similarly straightforward (moreso, even, as there are no `esi` references), so we finish that up and result in:

```haskell
:Main.main = runMainIO Main.main
Main.main = sBs $ sBr
sBs = let sB8 = "BPF_IF_PW^^VSNXAPCZL^XKM"
          sBm x = let sDJ = show heap_x
                      heap_x = x
                      sDK = let sBh = let sBf = let sBc = xor
                                                    sBd = fmap chr
                                                in sBd . sBc
                                      in sBf `on` ord
                            in zipWith sBh heap_sB8
                      heap_sB8 = sB8
                  in sDK $ sDJ
      in putStrLn . sBm
```

Inlining a bunch of stuff to simplify, we get that

```haskell
:Main.main = runMainIO Main.main
Main.main = sBs $ sBr
sBs = putStrLn . (\x -> zipWith ((fmap chr . xor) `on` ord) "BPF_IF_PW^^VSNXAPCZL^XKM" $ show x)
```

Essentially, `sBs` takes a number, displays it (in base 10), and xors the ascii values of that decimal representation with the string `"BPF_IF_PW^^VSNXAPCZL^XKM"`,
one byte at a type, then finally it prints the result.

#### `sBr` ####

After all the stadard stuff (stack check, heap check, blackhole and CAF stuff, and update frame), we have something new and interesting.

```asm
    mov     dword ptr [edi-4], offset integerzmgmp_GHCziIntegerziType_Szh_con_info
    mov     dword ptr [edi], 120
    lea     eax, [edi-3]
    mov     [ebp-12], eax
    add     ebp, -12
    jmp     rlz_info
```

Here, following that patterns established previously, we are calling the function `rlz`, providing one argument, the pointer to `[edi-3]`. However, we don't know for
certain how many arguments `rlz` expects. It looks like 1, since we only provide one, but it would be good to check. The answer comes right before the code of
`rlz_info`. GHC stores [various pieces][Tables] of information about a function right next to the code, including the arity. The 16 bit integer 10 bytes before the code
[holds this number][InfoTables], and sure enough, 10 bytes before `rlz_info`, we see a 1.

Now we look at the argument passed to `rlz`. This, as previously done with functions, is misaligned, because it is pointing at an already evaluated expression. This
time, however, we are looking at a data structure. GHC represents [algebraic data types][ADT] very simply, storing one word that contains a constructor, to distinguish
between different variants, followed immediately afterwards by any arguments that constructor takes. In this case, we are dealing with an `Integer`. Since `Integer`s
are the default commonly used numeric type in Haskell, GHC (at least by default, when relying on [GMP][GMP] for big integer support), not wanting to go through the
overhead of full arbitrary precision, defines an `Integer` variant, created by `S#`, that just wraps a machine word. This is used any time an integer fits inside a
machine word, and results in a useful speedup. Here, we just see the construction of a literal `Integer` 120. Since `S#` is variant number 1, the tag on our pointer
is also one.

Therefore, we have:

```haskell
:Main.main = runMainIO Main.main
Main.main = sBs $ sBr
sBs = putStrLn . (\x -> zipWith ((fmap chr . xor) `on` ord) "BPF_IF_PW^^VSNXAPCZL^XKM" $ show x)
sBr = rlz 120
```

[ADT]: https://en.wikipedia.org/wiki/Algebraic_data_type
[GMP]: https://gmplib.org/
[InfoTables]: https://ghc.haskell.org/trac/ghc/browser/ghc/includes/rts/storage/InfoTables.h#L229
[Integer]: https://hackage.haskell.org/package/integer-gmp-1.0.0.0/docs/src/GHC.Integer.Type.html#Integer
[Tables]: https://ghc.haskell.org/trac/ghc/wiki/Commentary/Rts/Storage/HeapObjects

#### `rlz` ####

This function is the heart of the whole problem. It is mostly staightforward, but introduces one new thing:

```asm
    mov     dword ptr [edi-4], offset integerzmgmp_GHCziIntegerziType_Szh_con_info
    mov     dword ptr [edi], 1
    lea     eax, [edi-3]
    mov     [ebp-8], eax
    mov     eax, [ebp+0]
    mov     [ebp-12], eax
    mov     dword ptr [ebp-16], offset stg_ap_pp_info
    mov     dword ptr [ebp-20], offset integerzmgmp_GHCziIntegerziType_zdfEqInteger_closure
    mov     dword ptr [ebp-4], offset sBx_info
    add     ebp, -20
    jmp     ghczmprim_GHCziClasses_zeze_info
```

Following the patterns seen before, this calls `==` on its argument and the constant 1. However, there is no update frame following this. Instead, we see
`sBx_info`, and the remaining stack slot (`[ebp+0]`, where the argument was) is left empty. This means that when `==` returns, it will (like everything)
put its result in `esi`, then jump into `sBx_info`, which will be responsible for finishing up anything that needs to be done. This is the general pattern
we will see any time the return value of a function is scrutinized using a `case` expression.

#### `sBx` ####

This, as a case statement, has a start that we haven't seen at all yet:

```asm
    mov     eax, esi
    and     eax, 3
    cmp     eax, 2
    jnb     short loc_804C5A1
```

Remember that `==` put its result in `esi` before jumping to `sBx`. Therefore, `esi` holds an object of type `Bool` that we know to be evaluated. Since we
know that it is evaluated, we can just check the tag bits, masking out all but the bottom 2 bits and doing a comparison. `False` is the first variant, so
has tag value 1, while `True` has tag value 2. Therefore, this will jump to `loc_804C5A1` if `==` returned `True`.

The `False` case, coming immediately after this prelude, is fairly straight forward, following all the patterns we have seen before. Note, however, that the
argument to `rlz` is now stored at `[ebp+4]`, since `[ebp+0]` is where `sBx_info` was stored. Going into `sBu` and `sBv` (which are identical), we find that
the false case returns `rlz (arg - 1) + rlz (arg - 1)`.

The `True` case, at the target of the prelude's jump, is something new. After a quick allocation an heap check, we have:

```asm
    mov     dword ptr [edi-4], offset integerzmgmp_GHCziIntegerziType_Szh_con_info
    mov     dword ptr [edi], 2
    lea     esi, [edi-3]
    add     ebp, 8
    jmp     dword ptr [ebp+0]
```

This allocates a literal integer 2 on the heap, stores a pointer to it in `esi`, and then jumps to a pointer further down the stack. This is exactly how we said
that all functions will eventually return. This case is just returning 2.

All together, this results in the following:

```haskell
:Main.main = runMainIO Main.main
Main.main = sBs $ sBr
sBs = putStrLn . (\x -> zipWith ((fmap chr . xor) `on` ord) "BPF_IF_PW^^VSNXAPCZL^XKM" $ show x)
sBr = rlz 120
rlz x = case x == 1 of
    False -> rlz (x - 1) + rlz (x - 1),
    True -> 2
```

#### Optimization and conclusion ####

Once we have this source code, getting the flag isn't too hard. `rlz x` is just 2 to the power of `x`, calculated stupidly slowly. A quick calculation or search on
Wolfram Alpha gives that 2^120 is 1329227995784915872903807060280344576, which, when xored character by character in ascii values with `"BPF_IF_PW^^VSNXAPCZL^XKM"`,
gives the flag.

### Flag ###

```
sctf{thinkingwiththunks}
```
