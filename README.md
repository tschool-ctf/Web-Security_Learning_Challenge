# Web Security Learning Challenge: Runaway from Jail CTF

This repository contains a simple Capture The Flag (CTF) challenge designed as a web security learning exercise. The goal is to navigate through a series of web-based puzzles, exploit common vulnerabilities, and ultimately "escape" the web security jail by finding the final flag.

## 🚀 Objective

You are a prisoner in a digital jail. To escape, you must use your web security skills to overcome a series of four challenges. Each solved puzzle brings you one step closer to freedom and the final flag.

## ⚙️ How to Run the Challenge

To get started, you need to run the Flask web application locally.

1.  **Prerequisites**:

      * Python 3.x
      * `pip`

2.  **Clone the Repository**:

    ```bash
    git clone https://github.com/your-username/Web-Security_Learning_Challenge.git
    cd Web-Security_Learning_Challenge/runaway_ctf
    ```

3.  **Set up a Virtual Environment (Recommended)**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4.  **Install Dependencies**:
    The required Python packages are listed in the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Application**:

    ```bash
    python app.py
    ```

    The application will start on `http://127.0.0.1:3000` (or `http://0.0.0.0:3000`). Open this address in your web browser to begin the challenge.

## 🚩 Walkthrough & Solution

This section provides a step-by-step solution to the CTF. It's recommended to try solving the challenges on your own first\!

### Stage 1: Finding the Hidden Entrance

The first page challenges you to catch a runaway robot. While you can try to click it, the real vulnerability lies elsewhere.

\<details\>
\<summary\>Click for the solution\</summary\>

A common first step in web reconnaissance is to check for a `robots.txt` file. This file often reveals paths that are not meant to be indexed by search engines but can be accessed by users.

1.  Navigate to `http://127.0.0.1:3000/robots.txt`.
2.  The file disallows access to `/cookie_store` and `/flag`.
3.  Navigate to the disclosed path: `http://127.0.0.1:3000/cookie_store` to enter the next stage.

\</details\>

### Stage 2: The Secret Cookie Recipe

You've found the secret prison cookie store. The goal is to get the password for the kitchen's back door.

\<details\>
\<summary\>Click for the solution\</summary\>

This stage involves cookie manipulation.

1.  Upon visiting the `/cookie_store`, the application sets a `secret_cookie` with the value `guest` in your browser.
2.  The page gives a hint that admins might see something different. Use your browser's developer tools (usually F12) to change the value of `secret_cookie` from `guest` to `admin`.
3.  With the cookie modified, click on any cookie to open the details modal, and then click the "獲取秘方" (Get Recipe) button.
4.  Because your `secret_cookie` is now `admin`, the server provides the special password: `チョコミントよりもあ・な・た`.
5.  Click the "廚房後門" (Kitchen Backdoor), enter this password, and submit it to proceed to the next level.

\</details\>

### Stage 3: Choosing the Right Path

You are presented with five doors, but none seem to be the correct exit. You must find the hidden, correct path.

\<details\>
\<summary\>Click for the solution\</summary\>

This is a classic path discovery or "Insecure Direct Object Reference" (IDOR) style puzzle. The visible doors correspond to `/path/1` through `/path/5`.

1.  The application code reveals a sixth, hidden path.
2.  By analyzing the URL structure, you can try to access `http://127.0.0.1:3000/path/6`.
3.  This path reveals the message: "This way to the exit, \<a href='/door'\>Go to the next level\</a\>". Click the link to advance.
4.  Interestingly, the code also allows path 4 to advance the user to the next level.

\</details\>

### Stage 4: The Final Door

You've reached the final door, which is protected by a login system. To pass, you need to find the credentials and bypass the final security check.

\<details\>
\<summary\>Click for the solution\</summary\>

The clues for the username and password are hidden in the HTML source code of the `/door` page.

1.  **Find the Credentials**:

      * View the source code of the `door.html` page.
      * You will find a comment: `Admin Emergency Access Account: R29vb29vb29vb29vZCBIQENLZXI=`. This is a Base64 encoded string. Decoding it gives you the username: `Goooooooooood H@CKer`.
      * Another comment reads: `DEPRECATED Administrator Password Encoding: 106 105 51 97 112 55 103 52 121 106 105 52 99 108 51 99 57 52 100 107 52`. These are ASCII decimal codes. Converting them to characters reveals the password: `ji3ap7g4yji4cl3c94dk4`.

2.  **Bypass the Admin Check**:

      * When you visit the `/door` page, the application sets a cookie `admin` to `False`.
      * If you log in with the correct credentials, you will be shown a "not admin" page because of this cookie. The hint on this page reads: "Hint: The administrator has a special cookie...".
      * Before logging in, use your browser's developer tools to change the value of the `admin` cookie from `False` to `True`.

3.  **Get the Flag**:

      * With the correct username, password, and the `admin` cookie set to `True`, submit the login form.
      * You will be redirected to the success page, which contains the final flag.

    **Flag:** `AIS3{Y0u_4r3_w5_m4573r}`

\</details\>