# APP CTF Challenge 3
<br>
According to the description, disassembling is required. So, first thing first, let's check what function we should look for.<br>
After decompiling the APK and reviewing the source code, it seems like there is only one activity (MainActivity) with the following code: 

```java
...snip...
public void onClick(View v) {
  TextView tv = (TextView) MainActivity.this.findViewById(C0194R.id.result);
  if (MainActivity.this.check(((EditText) MainActivity.this.findViewById(C0194R.id.editText)).getText().toString())) {
    tv.setText(":)");
  } else {
    tv.setText(":(");
  }
}
...snip...
public native boolean check(String str);
...snip...
```
Ok. So we should look for the **check** function.<br><br>

In the root directory of the decompiled APK, there is a _lib_ directory. In this directory, there are various of sub-directories, containing architectures (arm64-v8a, armeabi, armeabi-v7a, mips, x86, x86_64). Probably most of the people would choose the x86 family architecture. But I really like ARM so I decided to analyze the armeabi library.<br><br>
Using the command ```arm-linux-gnueabihf-objdump -D libnative-lib.so```, I could disassemble the library and start to reverse the function's assembly code.<br><br>

The function was found at the address 0x5ac.
According to the Java code above, the **check** function gets only a string. So, Let's take a look at the first code block after the function's prolog:
```assembly
 5bc:	4604      	mov	r4, r0
 5be:	f7ff efb4 	blx	528 <strlen@plt>
 5c2:	2818      	cmp	r0, #24
 5c4:	d147      	bne.n	656 <Java_com_ctf_app3_MainActivity_check@@Base+0xaa>
```
That is easy. Just getting the length of the given string (using _strlen_ function) and comparing in to 24. If it's not equal to 24, then a jump will occur.<br>
So, the flag is <span>_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ </span>. Still empty but at least the length is known.<br><br>

Before continuing to the next block, let's check what happens in ```<Java_com_ctf_app3_MainActivity_check@@Base+0xaa>```.<br>
```assembly
656:	2000      	movs	r0, #0
658:	bdd0      	pop	{r4, r6, r7, pc}
```
It seems like the return value is 0 (```movs	r0, #0```) and it exits the function (```pop	{r4, r6, r7, pc}```). According to the Java code, 0 is not good. So we have to make sure that the program will skip the first instruction.<br><br>

Continuing to the next block.<br>
```assembly
5c6:	7ca0      	ldrb	r0, [r4, #18]
5c8:	2873      	cmp	r0, #115	; 0x73
5ca:	bf04      	itt	eq
5cc:	7b20      	ldrbeq	r0, [r4, #12]
5ce:	2866      	cmpeq	r0, #102	; 0x66
5d0:	d141      	bne.n	656 <Java_com_ctf_app3_MainActivity_check@@Base+0xaa>	;656
```
The 19th letter getting loaded to r0, and compared to the value 115 ("s").<br>
Using ARM "EQ" magic, if the letter equals to "s", then the 13th letter getting loaded and compared to the value 102 ("f").<br>. If the 19th letter is not equal to "s" or the 13th letter is not equal to "f", then the program will jump to ```<Java_com_ctf_app3_MainActivity_check@@Base+0xaa>``` (not good).<br><br>

So now, the flag is <span>_ _ _ _ _ _ _ _ _ _ _ _ f _ _ _ _ _ s _ _ _ _ _ </span>.
The next few blocks are pretty much the same.
```assembly
 5d2:	7ba0      	ldrb	r0, [r4, #14]
 5d4:	2864      	cmp	r0, #100	; 0x64
 5d6:	bf04      	itt	eq
 5d8:	7c20      	ldrbeq	r0, [r4, #16]
 5da:	2868      	cmpeq	r0, #104	; 0x68
 5dc:	d13b      	bne.n	656 <Java_com_ctf_app3_MainActivity_check@@Base+0xaa>	;656
 --------------------------------------------------------------------------------------
 5de:	7ae0      	ldrb	r0, [r4, #11]
 5e0:	285f      	cmp	r0, #95	; 0x5f
 5e2:	bf04      	itt	eq
 5e4:	7b60      	ldrbeq	r0, [r4, #13]
 5e6:	2865      	cmpeq	r0, #101	; 0x65
 5e8:	d135      	bne.n	656 <Java_com_ctf_app3_MainActivity_check@@Base+0xaa>	;656
 --------------------------------------------------------------------------------------
 5ea:	7aa0      	ldrb	r0, [r4, #10]
 5ec:	2864      	cmp	r0, #100	; 0x64
 5ee:	bf04      	itt	eq
 5f0:	78e0      	ldrbeq	r0, [r4, #3]
 5f2:	285f      	cmpeq	r0, #95	; 0x5f
 5f4:	d12f      	bne.n	656 <Java_com_ctf_app3_MainActivity_check@@Base+0xaa>	;656
 --------------------------------------------------------------------------------------
 5f6:	7d60      	ldrb	r0, [r4, #21]
 5f8:	2865      	cmp	r0, #101	; 0x65
 5fa:	bf04      	itt	eq
 5fc:	7be0      	ldrbeq	r0, [r4, #15]
 5fe:	285f      	cmpeq	r0, #95	; 0x5f
 600:	d129      	bne.n	656 <Java_com_ctf_app3_MainActivity_check@@Base+0xaa>	;656
 --------------------------------------------------------------------------------------
 602:	7da0      	ldrb	r0, [r4, #22]
 604:	2874      	cmp	r0, #116	; 0x74
 606:	bf04      	itt	eq
 608:	7a60      	ldrbeq	r0, [r4, #9]
 60a:	2869      	cmpeq	r0, #105	; 0x69
 60c:	d123      	bne.n	656 <Java_com_ctf_app3_MainActivity_check@@Base+0xaa>	;656
 --------------------------------------------------------------------------------------
 60e:	7960      	ldrb	r0, [r4, #5]
 610:	286e      	cmp	r0, #110	; 0x6e
 612:	bf04      	itt	eq
 614:	7860      	ldrbeq	r0, [r4, #1]
 616:	2868      	cmpeq	r0, #104	; 0x68
 618:	d11d      	bne.n	656 <Java_com_ctf_app3_MainActivity_check@@Base+0xaa>
 --------------------------------------------------------------------------------------
 61a:	7de0      	ldrb	r0, [r4, #23]
 61c:	2873      	cmp	r0, #115	; 0x73
 61e:	bf04      	itt	eq
 620:	78a0      	ldrbeq	r0, [r4, #2]
 622:	2865      	cmpeq	r0, #101	; 0x65
 624:	d117      	bne.n	656 <Java_com_ctf_app3_MainActivity_check@@Base+0xaa>
 --------------------------------------------------------------------------------------
 626:	79e0      	ldrb	r0, [r4, #7]
 628:	2872      	cmp	r0, #114	; 0x72
 62a:	bf04      	itt	eq
 62c:	7a20      	ldrbeq	r0, [r4, #8]
 62e:	286f      	cmpeq	r0, #111	; 0x6f
 630:	d111      	bne.n	656 <Java_com_ctf_app3_MainActivity_check@@Base+0xaa>
 --------------------------------------------------------------------------------------
 632:	7d20      	ldrb	r0, [r4, #20]
 634:	2870      	cmp	r0, #112	; 0x70
 636:	bf04      	itt	eq
 638:	7ce0      	ldrbeq	r0, [r4, #19]
 63a:	285f      	cmpeq	r0, #95	; 0x5f
 63c:	d10b      	bne.n	656 <Java_com_ctf_app3_MainActivity_check@@Base+0xaa>
 --------------------------------------------------------------------------------------
 63e:	7820      	ldrb	r0, [r4, #0]
 640:	2874      	cmp	r0, #116	; 0x74
 642:	bf04      	itt	eq
 644:	79a0      	ldrbeq	r0, [r4, #6]
 646:	2864      	cmpeq	r0, #100	; 0x64
 648:	d105      	bne.n	656 <Java_com_ctf_app3_MainActivity_check@@Base+0xaa>
```
If you'll follow the blocks, you'll get that the flag is <span>t h e _ _ n d r o i d _ f e d _ h _ s _ p e t s </span> (where only the 5th and the 18th letters are missing). It pretty easy to guess what they are, but let check the last block.<br><br>
``` assembly
64a:	7c60      	ldrb	r0, [r4, #17]
64c:	2869      	cmp	r0, #105	; 0x69
64e:	bf04      	itt	eq
650:	7920      	ldrbeq	r0, [r4, #4]
652:	2861      	cmpeq	r0, #97	; 0x61
654:	d001      	beq.n	65a <Java_com_ctf_app3_MainActivity_check@@Base+0xae>
```
Like the same logic before, the 5th letter is "a" and the 18th letter is "i" (shocker).<br>
But in the end of the block, there is a jump to ```<Java_com_ctf_app3_MainActivity_check@@Base+0xae>```. Let's check what's up there.<br>
```assembly
65a:	2001      	movs	r0, #1
65c:	bdd0      	pop	{r4, r6, r7, pc}
```
It seems like the return value is 1 (```movs	r0, #1```) and it exits the function (```pop	{r4, r6, r7, pc}```). This is awesome for us!

So to conclude, the flag is **the_android_fed_his_pets**.
