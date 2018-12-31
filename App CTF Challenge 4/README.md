# APP CTF Challenge 4
<br>
According to the description, a QR code should be involved.<br>
After decompiling the APK and reviewing the source code, it seems like there are two main source code files: <strong>MainActivity.java</strong> and <strong>C0195c.java</strong>.<br><br>

After scanning a QR code, the **MainActivity.java** containing the following code:
```java
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    IntentResult result = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);
    if (result == null || result.getContents() == null) {
        super.onActivityResult(requestCode, resultCode, data);
        return;
    }
    String s = new C0195c(result.getContents()).cf();
    if (!s.equals("")) {
        Toast.makeText(this, "Good job :)", 1).show();
        ((TextView) findViewById(C0194R.id.tv_flag)).setText("flag{" + s + "}");
    }
}
```
This code first parses the given QR code's data (lines 1-5 of the function).<br>
Then it creates a **C0195c** object, using the parsed data, and calls the object's **cf** function (which returns a string).<br>
If the returned string is not empty, then the challenge completed.<br><br>

So, in order to solve this challenge the **cf** function should be called (using a QR code) and the returned value should be not an empty string.<br>
According to the **C0195c** constructor, the QR code's data is saved in *f9s* variable.<br>
Let's check what's up with the **cf** function.<br>
```java
public String cf() {
    String flag = "";
    if (this.f9s.length() != 11) {
        return flag;
    }
    if (this.f9s.charAt(3) != '-' || this.f9s.charAt(7) != '-') {
        return flag;
    }
    String p1 = this.f9s.substring(0, 3);
    String p2 = this.f9s.substring(4, 7);
    String p3 = this.f9s.substring(8, 11);
    String hash = m4h(p1, "MD5");
    if (!isAsciiPrintable(p1.charAt(0)) || !isAsciiPrintable(p1.charAt(2)) || !hash.toLowerCase().contains("1a") || p1.charAt(1) != 'f') {
        return flag;
    }
    try {
        Integer i_p2 = Integer.valueOf(Integer.parseInt(p2));
        if (i_p2.intValue() < 100 || i_p2.intValue() >= 200) {
            return flag;
        }
        hash = m4h(p3, "SHA-512");
        if (isAsciiPrintable(p1.charAt(1)) && isAsciiPrintable(p1.charAt(2)) && p1.charAt(0) != 'i' && hash.toLowerCase().contains("3") && hash.toLowerCase().contains("ed") && hash.toLowerCase().contains("fe")) {
            flag = mf(p1, p2, p3);
        }
        return flag;
    } catch (NumberFormatException e) {
        return flag;
    }
}
```

It seems like that the variable _flag_ is the return value of this function. Then in order to succeed this challenge, the program mush change its value from an empty string to something (```flag = mf(p1, p2, p3);```).<br>
But first, there are 2 functions that are used in this function: **isAsciiPrintable** (used 4 times) and **m4h** (used twice).<br><br>

The function **isAsciiPrintable**: <br>
```java
private boolean isAsciiPrintable(char ch) {
    return ch >= ' ' && ch < '';
}
```
It's pretty easy to understand what's up. The function gets a character and checks if it's between 0x20 (included) and 0x7f (excluded).<br><br>

The function **m4h**<br>
```java
private String m4h(String s, String hash) {
    try {
        MessageDigest digest = MessageDigest.getInstance(hash);
        digest.update(s.getBytes());
        byte[] messageDigest = digest.digest();
        StringBuilder hexString = new StringBuilder();
        for (byte aMessageDigest : messageDigest) {
            String h = Integer.toHexString(aMessageDigest & 255);
            while (h.length() < 2) {
                h = "0" + h;
            }
            hexString.append(h);
        }
        return hexString.toString();
    } catch (NoSuchAlgorithmException e) {
        e.printStackTrace();
        return "";
    }
}
```
This function gets two strings. The first one used for calculating a hash (and converting it to a hexstring), and the second string is for the type of hash to calculate (in this program MD5 or SHA-512).<br>
The function returns the hexstring of the calculated hash.<br><br>

Now, we can break the function **cf** down.<br>
The first checks are (reminder - the QR code is in the object's _f9s_ variable):
```java
if (this.f9s.length() != 11) {
    return flag;
}
if (this.f9s.charAt(3) != '-' || this.f9s.charAt(7) != '-') {
    return flag;
}
```
Pretty straight-forward. The QR code's should contain 11 characters, in the format of _ _ _ - _ _ _ - _ _ _.<br>
If it's not, then the function will return an empty string (reminder - not good).<br>

Next,
```java
String p1 = this.f9s.substring(0, 3);
String p2 = this.f9s.substring(4, 7);
String p3 = this.f9s.substring(8, 11);
String hash = m4h(p1, "MD5");
```
The QR code splitted into three parts (_p1_, _p2_, _p3_), each containing three characters.<br>
Then, the **m4h** is called for _p1_ and "MD5" - a MD5 hash of _p1_ is returned.<br><br>

```java
if (!isAsciiPrintable(p1.charAt(0)) || !isAsciiPrintable(p1.charAt(2)) || !hash.toLowerCase().contains("1a") || p1.charAt(1) != 'f') {
    return flag;
}
```
Now, four things are getting checked in _p1_:
<ol>
  <li><b>isAsciiPrintable</b> returns true for the first character (= the first character is between 0x20 and 0x7e). Narrows down from 16777216 possibilities to 6153150.</li>
  <li><b>isAsciiPrintable</b> returns true for the third character (= the third character is between 0x20 and 0x7e). Narrows down from 6153150 possibilities to 2268220.</li>
  <li>The hexstring of the MD5 hash of <i>p1</i> contains "1a". Narrows down from 2268220 possibilities to 259912.</li>
  <li>The second character of <i>p1</i> is "f". Narrows down from 259912 possibilities to 998.</li>
</ol><br>
So, now _p1_ is narrowed to 998 possibilies. Not good enough.<br><br>

```java
Integer i_p2 = Integer.valueOf(Integer.parseInt(p2));
if (i_p2.intValue() < 100 || i_p2.intValue() >= 200) {
    return flag;
}
```

Next, _p2_ is converted into an integer, and it should be between 100 to 199 (included). If not, _flag_ will be returned and it hasn't change yet (not good).<br>

```java
hash = m4h(p3, "SHA-512");
if (isAsciiPrintable(p1.charAt(1)) && isAsciiPrintable(p1.charAt(2)) && p1.charAt(0) != 'i' && hash.toLowerCase().contains("3") && hash.toLowerCase().contains("ed") && hash.toLowerCase().contains("fe")) {
    flag = mf(p1, p2, p3);
}
```
A SHA-512 is calculated from _p3_, and some stuff is getting checked in _p1_ and the hash:
<ol>
  <li><b>isAsciiPrintable</b> returns true for the second character of <i>p1</i> (= the second character is between 0x20 and 0x7e). It doesn't narrows the possibilities, because the second character should be "f".</li>
  <li><b>isAsciiPrintable</b> returns true for the third character of <i>p1</i> (= the third character is between 0x20 and 0x7e). It doesn't narrows the possibilities, because it already had been checked.</li>
  <li>The first character of <i>p1</i> shouldn't be "i".  Narrows down from 998 possibilities to 988.</li>
  <li>The hash of <i>p3</i> should contain "3". Narrows down from 16777216 possibilities to 16772988.</li>
  <li>The hash of <i>p3</i> should contain "ed". Narrows down from 16772988 possibilities to 6592815.</li>
  <li>The hash of <i>p3</i> should contain "fe". Narrows down from 6592815 possibilities to 2814977.</li>
</ol><br>

So for _p1_ there are 988 possibilities, _p2_ 100 possibilities and _p3_ 2814977 possibilities. Let's check if the function **mf** decreases the number of possibilities.<br><br>

```java
private String mf(String p1, String p2, String p3) {
    String f = "";
    boolean fe_found = false;
    boolean ed_found = false;
    int i = 0;
    String sha512 = m4h(p3, "SHA-512");
    while (true) {
        if (!fe_found && sha512.charAt(i) == 'f' && sha512.charAt(i + 1) == 'e') {
            f = f + Character.toString(sha512.charAt(i)) + Character.toString(sha512.charAt(i + 1));
            fe_found = true;
            i = 0;
        } else if (!fe_found || ed_found || sha512.charAt(i) != 'e' || sha512.charAt(i + 1) != 'd') {
            if (ed_found && sha512.charAt(i) == '3') {
                break;
            }
        } else {
            f = f + Character.toString(sha512.charAt(i)) + Character.toString(sha512.charAt(i + 1)) + "_";
            ed_found = true;
            i = 0;
        }
        i++;
    }
    f = (f + Character.toString('m') + Character.toString(sha512.charAt(i)) + "_") + Character.toString(p1.charAt(1)) + Character.toString(p2.charAt(0));
    i = 0;
    String md5 = m4h(p1, "md5");
    while (true) {
        if (md5.charAt(i) == '1' && md5.charAt(i + 1) == 'a') {
            return (f + Character.toString(md5.charAt(i + 1))) + "gs";
        }
        i++;
    }
}
```

First, the function initialize the _f_ variable (which may contain the flag), two booleans as false (<i>fe_found</i> and <i>ed_found</i>), an index variable (_i_) and the SHA-512 of _p3_.<br>
Let's look at the first while loop.
```java
while (true) {
    if (!fe_found && sha512.charAt(i) == 'f' && sha512.charAt(i + 1) == 'e') {
        f = f + Character.toString(sha512.charAt(i)) + Character.toString(sha512.charAt(i + 1));
        fe_found = true;
        i = 0;
    } else if (!fe_found || ed_found || sha512.charAt(i) != 'e' || sha512.charAt(i + 1) != 'd') {
        if (ed_found && sha512.charAt(i) == '3') {
            break;
        }
    } else {
        f = f + Character.toString(sha512.charAt(i)) + Character.toString(sha512.charAt(i + 1)) + "_";
        ed_found = true;
        i = 0;
    }
    i++;
}
```
There are 3 conditions in this loop:
<ol>
    <li>If the hash contains "fe" in the i-th index. If it does, then add "fe" to the flag, change the <i>fe_found</i> flag to true and reset the index.</li>
    <li>If "fe" not found or "ed" found or the i-th character is not "e" or the (i+1)-th charactr is not "d", then it will check if the i-th character is 3. If it does, then it will exit the loop.</li>
    <li>Otherwise, add the i-th character and the (i+1)-th character to the flag.</li>
</ol>
Let's explain few stuff.<br>
First, if the i-th character is not "e" or "f" and the (i+1)-th character is not "d" or "e", then the program will probably won't change anything in the current iteration but _i_.<br>
Second, apparently "fe" will appear before "ed" in all the 2814977 SHA-512 hashes of _p3_.<br>
Last but not least, after "fe" and "ed" were found, the program will basically search for "3".<br>
So to conclude the loop break down, at the end of the loop _f_ should contain "feed_" and i should be equal to the position of the first "3" character in the hash.<br><br>

Now let's break the second loop,
```java
f = (f + Character.toString('m') + Character.toString(sha512.charAt(i)) + "_") + Character.toString(p1.charAt(1)) + Character.toString(p2.charAt(0));
i = 0;
String md5 = m4h(p1, "md5");
while (true) {
    if (md5.charAt(i) == '1' && md5.charAt(i + 1) == 'a') {
        return (f + Character.toString(md5.charAt(i + 1))) + "gs";
    }
    i++;
}
```
The first line adds "m", the i-th character in the SHA-512 hash (should be "3"), "_", the second character of _p1_ (reminder - should be "f") and the first character to _p1_ (there are some possibilities but let's say the letter "l").<br>
Now, the flag is "feed_m3_fl".<br>
In the loop, the condition is actually looking for the first "1a" sequence in the MD5 hash of _p1_ (reminder - must be in the hash).<br>
When it finds it, it will return _f_ with "a" and "gs". So the return value would be "feed_m3_flags).<br><br>

So to conclude, there are a lot of possibilities (as I found out - I may be wrong) to the QR code and the flag.<br>
But I guess the idea was that the flag would be **feed_m3_flags**.
