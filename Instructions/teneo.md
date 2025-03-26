# Teneo Cookie Extractor  

## ⚠️ Disclaimer  
**This script extracts your Teneo authentication token.**  
- **Do not share it with anyone.**  
- **Do not execute random scripts in your browser.**  
- **Anyone with this token can log into your account without needing your password.**  

---

## 📌 Steps to Extract the NodePay Cookie  

### Step 1: Open Developer Console  
1. Open your web browser.  
2. Go to the Teneo website and log in to your account.  
3. Open the Developer Console:  
   - **Chrome/Edge:** Press `F12` or `Ctrl + Shift + I`, then go to the **Console** tab.  
   - **Firefox:** Press `F12` or `Ctrl + Shift + K`.  
   - **Safari:** Press `Cmd + Option + C` (Enable "Develop" menu in settings if needed).  

---

### Step 2: Execute the Script  
Copy and paste the following JavaScript code into the **Console** and press **Enter**:  

```javascript
/**
 * DISCLAIMER: THIS SCRIPT EXTRACTS YOUR COOKIE.  
 * DO NOT SHARE IT WITH ANYONE. DO NOT EXECUTE RANDOM SCRIPTS IN YOUR BROWSER.  
 * ANYONE WITH THIS COOKIE CAN LOG INTO YOUR ACCOUNT WITHOUT NEEDING YOUR PASSWORD.  
 */

function printNpToken() {
    const npToken = localStorage.getItem("accessToken");

    if (npToken) {
        console.log("accessToken:", npToken);
    } else {
        console.log("accessToken not found in Local Storage.  Log in again");
    }
}

printNpToken();


