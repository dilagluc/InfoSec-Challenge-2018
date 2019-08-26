# App CTF Challenge 1
<br>

After decompiling the APK and reviewing the source codes, it's noticeable that there is only one activity (MainActivity).<br>
In this (slim) activity there are 3 functions (with code): **onClick**, **onCreate**, **md5**.
It's pretty obvious what **onCreate** and **md5** (hashing the given string). So let's see what **onClick** does:
```java
        public void onClick(View v) {
            EditText password = (EditText) MainActivity.this.findViewById(C0194R.id.editText2);
            TextView lbl = (TextView) MainActivity.this.findViewById(C0194R.id.textView);
            if (MainActivity.md5(password.getText() + ":" + ((EditText) MainActivity.this.findViewById(C0194R.id.editText)).getText()).equals("263c7fa932b26a56ec0ad76b94aff98b")) {
                lbl.setText(":)");
            } else {
                lbl.setText(":(");
            }
        }
```

So, it's pretty basic stuff.<br>
The function gets a username and a password from the user, combine them into one string ([username]:[password]), hash it (using md5) and comparing the hash to **"263c7fa932b26a56ec0ad76b94aff98b"**. All of it happens in the if:
```java
if (MainActivity.md5(password.getText() + ":" + ((EditText) MainActivity.this.findViewById(C0194R.id.editText)).getText()).equals("263c7fa932b26a56ec0ad76b94aff98b"))
```
<br><br>
I don't know any other way besides brute-forcing to reverse a hash. So by using _hashcat_ (thank god for the GPUs), after some time I got a match - **p@5s:admin**.
