
# **DockWeb**

DockWeb is a versatile Docker image designed to run multiple money-making web extensions in a single container. As more Grass-like web extensions are emerging, DockWeb provides an efficient way to manage and deploy them together.  

---

## **Supported Apps**
 - [Grass](https://app.getgrass.io/register/?referralCode=cDmWvtOKIDU-7T-)
 - [GradientNode](https://app.gradient.network/signup?code=WL8GSK)
 - [NodePay](https://app.nodepay.ai/register?ref=EHEzbYy5vbpP2cj) (Soon)

More will be added soon ;) 

## **Deployment Guide 🚀**

To instantiate the Docker container with appropriate credentials for web extensions, set the required environment variables. Substitute `<your_email>` and `<your_password>` with your Grass account credentials or those corresponding to other supported extensions:

```bash
docker run -d \
  -e GRASS_USER=<your_email> \
  -e GRASS_PASS=<your_password> \
  -e GRADIENT_EMAIL=<your_email> \
  -e GRADIENT_PASS=<your_password> \
  -v ./chrome_user_data:/chrome_user_data \
  carbon2029/dockweb
```

### **Persistent Data Management**
To maintain browser session continuity across container lifecycle events, a volume mount has been configured. This mechanism ensures the preservation of Chrome user data by mapping `./chrome_user_data` from the host system to `/chrome_user_data` within the containerized environment, thereby enabling persistent storage and seamless session restoration.





## **Advance Usage**

1. **Pull the Docker image:**  
   ```bash
   docker pull carbon2029/dockweb
   ```

2. **Run the container:**  
   Provide credentials for one or more supported extensions as environment variables. For example:  
   ```bash
   docker run -d -e GRASS_USER=<your_email> -e GRASS_PASS=<your_password> carbon2029/dockweb
   ```
 

3. **Monitor the container:**  
   To check if the container is running:  
   ```bash
   docker ps
   ```

4. **Stop the container:**  
   ```bash
   docker stop <container_id>
   ```


---

## **Features**

- **Multi-Extension Support:** Run multiple web extensions in one container.  
- **Easy Setup:** Minimal configuration required.  
- **Resource Efficiency:** Consolidates extensions to save on system resources.  
- **Scalable:** Add support for new extensions as they emerge.  
- **Cross-Platform Compatibility:** Works seamlessly on any system that supports Docker.  

---

## **FAQ**
 

### **Is it lightweight?**  
Not entirely at the moment. Current resource usage:  
- **CPU**: ~0.01 - 1%  
- **RAM**: ~275 MB  

Optimizations are planned in future updates.  

### **Do the apps pay?**  
As of 11/25/2024 only grass had made their airdrop other are claiming to pay soon Time will tell so only use the apps if you trust them.

  

---

## **Planned Improvements**

- Further reduce resource usage.  
- Expand support for new web extensions.   

---

## **License**

This program is free software, distributed under the terms of the [GNU General Public License (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html).  
You are free to redistribute and/or modify it under the license terms.  

**Note:** This software is provided without warranty; use it at your own risk.  

---

## **Disclaimer**
This is an unofficial build and not affiliated or officially endorsed by Grass (getgrass) or any other apps. This repository (project) and its assets are provided "as is" without warranty of any kind. The author makes no warranties, express or implied, that this project and its assets are free of errors, defects, or suitable for any particular purpose. The author shall not be liable for any damages suffered by any user of this project, whether direct, indirect, incidental, consequential, or special, arising from the use of or inability to use this project, its assets or its documentation, even if the author has been advised of the possibility of such damages. 

---

## **Note**
Special thanks to [MRColorR](https://github.com/MRColorR) for helping out with this project.
Also if you use any referral link it helps me create more free projects thank you it means a lot <3
