
# **DockWeb**

DockWeb is a versatile Docker image designed to run multiple money-making web extensions in a single container. As more Grass-like web extensions are emerging, DockWeb provides an efficient way to manage and deploy them together.  

---

## **Supported Apps**
 - [Grass](https://app.getgrass.io/register/?referralCode=cDmWvtOKIDU-7T-)
 - [NodePay](https://app.nodepay.ai/register?ref=EHEzbYy5vbpP2cj) (Soon)
 - [GradientNode](https://app.gradient.network/signup?code=WL8GSK)

More will be added soon ;) 

## **Quick Start 🚀**

Run the Docker container with your credentials for supported web extensions as environment variables. Replace `<your_email>` and `<your_password>` with your Grass account details (or details of other extensions):  

```bash
docker run -d -e GRASS_USER=<your_email> -e GRASS_PASS=<your_password> mrcolorrain/dockweb
```

---

## **Features**

- **Multi-Extension Support:** Run multiple web extensions in one container.  
- **Easy Setup:** Minimal configuration required.  
- **Resource Efficiency:** Consolidates extensions to save on system resources.  
- **Scalable:** Add support for new extensions as they emerge.  
- **Cross-Platform Compatibility:** Works seamlessly on any system that supports Docker.  

---

## **Usage**

1. **Pull the Docker image:**  
   ```bash
   docker pull mrcolorrain/dockweb
   ```

2. **Run the container:**  
   Provide credentials for one or more supported extensions as environment variables. For example:  
   ```bash
   docker run -d -e GRASS_USER=<your_email> -e GRASS_PASS=<your_password> mrcolorrain/dockweb
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
- Add a configuration wizard for easier setup.  
- Implement logs for debugging and monitoring.  

---

## **License**

This program is free software, distributed under the terms of the [GNU General Public License (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html).  
You are free to redistribute and/or modify it under the license terms.  

**Note:** This software is provided without warranty; use it at your own risk.  

---

## **Disclaimer**

This software is provided "as is," without warranties of any kind. The author disclaims all liability for any damages arising from its use, including but not limited to direct, indirect, incidental, or consequential damages.  

---