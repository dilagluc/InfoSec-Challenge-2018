# APP CTF Challenge 2
<br>
After decompiling the APK and reviewing the source codes, there are 2 interesting files:<br>
<ul>
  <li>MainActivity.java (not so interesting but leading to the next one)</li>
  <li>C0195b.java (where are the magic happens).</li>
</ul>
<br>
In MainActivity.java there is a call for the **checkSerial** function in C0195b.java. So the investigation should probably be there.
<br><br>

```java
    public boolean checkSerial() {
        C0196c DbHelper = new C0196c(this.context);
        if (!DbHelper.openDataBase()) {
            return false;
        }
        Cursor c = DbHelper.getReadableDatabase().rawQuery("select * from e052bcf4c08a5c3478", null);
        c.moveToFirst();
        String iv = c.getString(0);
        return encrypt(this.serial, c.getString(1), iv).equals("6f4e8fff1523407fabf1e6ba7abcc585129e3802f785a75f28b0e63482449f5347501f6b38f014ae4f51e37ffb9b323b");
    }
```
This function containing a cursor to an application's database, and it seems like there is an encryption using the first and the seconds strings from the database - the encrypted stuff getting checked against a hexstring (the long one you can't miss it).<br>

Ok, so let's take a look at the **encrypt** function.
```java
private String encrypt(String message, String key, String iv) {
        String s4 = "";
        SecretKeySpec secretkeyspec = new SecretKeySpec(HexToBytes(key), "AES");
        Cipher cipher = null;
        try {
            cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (NoSuchPaddingException e2) {
            e2.printStackTrace();
        }
        try {
            cipher.init(1, secretkeyspec, new IvParameterSpec(HexToBytes(iv)));
        } catch (InvalidKeyException e3) {
            e3.printStackTrace();
        } catch (InvalidAlgorithmParameterException e4) {
            e4.printStackTrace();
        }
        try {
            s4 = bytesToHex(cipher.doFinal(message.getBytes()));
        } catch (IllegalBlockSizeException e5) {
            e5.printStackTrace();
        } catch (BadPaddingException e6) {
            e6.printStackTrace();
        }
        return s4;
    }
```
The function gets the message to encrypt, the key and the IV (in that order). It will create some instances of cipher, and it's pretty obvious that it will use AES-CBC with PKCS#5 padding. Ok neat :sunglasses:.<br>

Back to the **checkSerial** function. It seems like it calls the **encrypt** function with the user's input as the message, the first string from the database as the IV, and the second string from the database as the key.<br><br>
Like every (or most of them) Android application, this application has an *assets* directory. Surprise surprise, there is only one file in there - **db.db**.<br>
Using _binwalk_ command, we can find out the it's a SQLite 3 database.<br><br>

Let's run the query that **checkSerial** runs:
```sql
sqlite> select * from e052bcf4c08a5c3478;
1337133713371337BAADF0000DAAAAAA|FE5A10236842EF551087301E8B17EEFB|:3

```
Great. Now we got the key and the IV. So for getting the actual serial, we should decrypt the hexstring in *6f4e8fff1523407fabf1e6ba7abcc585129e3802f785a75f28b0e63482449f5347501f6b38f014ae4f51e37ffb9b323b*.<br><br>

The serial is **Serial-APPS-AND-DBS-ARE-BEST-FRIENDS**.<br>
