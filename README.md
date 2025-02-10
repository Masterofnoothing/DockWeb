# **DockWeb: Unified Web Extension Deployment**

DockWeb is a versatile Docker image designed to efficiently run multiple web extensions within a single container. As the landscape of monetizable web extensions expands, DockWeb provides a seamless solution for managing and deploying them collectively.

---

## **Supported Applications**
- [Grass](https://app.getgrass.io/register/?referralCode=cDmWvtOKIDU-7T-)
- [GradientNode](https://app.gradient.network/signup?code=WL8GSK)
- [DawnInternet](https://www.dawninternet.com/) *sufx302h use this code pretty please*
- [NodePay](https://app.nodepay.ai/register?ref=EHEzbYy5vbpP2cj) *(Coming Soon)*
- [Teno](https://bit.ly/teneo-community-node) *S7erg use this code pretty please*

---

## **Deployment Guide** 🚀

To deploy DockWeb with the appropriate credentials, set the required environment variables. You can specify credentials for all extensions at once using `ALL_EMAIL` and `ALL_PASS`, or define them individually as needed.

### **Basic Command (Beginner Friendly)**
```bash
docker run -d \
  --env ALL_EMAIL=<your_email> \
  --env ALL_PASS=<your_password> \
  --env GRASS_USER=<your_email> \
  --env GRASS_PASS=<your_password> \
  --env GRADIENT_EMAIL=<your_email> \
  --env GRADIENT_PASS=<your_password> \
  --env DAWN_EMAIL=<your_email> \
  --env DAWN_PASS=<your_password> \
  --env TENO_EMAIL=<your_email> \
  --env TENO_PASS=<your_password> \
  --volume ./chrome_user_data:/chrome_user_data \
  --publish 5000:5000 \
  carbon2029/dockweb
```

> **Note:** You only need to include the variables for the extensions you plan to use.


> **Tip** This is too difficult for you check this awesome project called [money4band](https://github.com/MRColorR/money4band) for easy app setup

### **Supported Environment Variables**

| Variable Name     | Description                                         |
|------------------|-------------------------------------------------|
| ALL_EMAIL      | Universal email for all extensions (if same)   |
| ALL_PASS       | Universal password for all extensions (if same) |
| GRASS_USER     | Email for Grass extension                      |
| GRASS_PASS     | Password for Grass extension                   |
| GRADIENT_EMAIL | Email for GradientNode extension               |
| GRADIENT_PASS  | Password for GradientNode extension            |
| DAWN_EMAIL     | Email for Dawn extension                       |
| DAWN_PASS      | Password for Dawn extension                    |
| TENO_EMAIL     | Email for Teno                                  |
| TENO_PASS     | Password for Teno                                |
| -v ./chrome_user_data:/chrome_user_data | Maps Chrome user data for session persistence |
| -p 5000:5000   | Exposes port 5000 for web-based interactions    |

### **Persistent Data Management**
To ensure session continuity across container restarts, DockWeb includes a volume mount for Chrome user data by default. This maps `./chrome_user_data` from the host system to `/chrome_user_data` within the container, enabling persistent storage and seamless session restoration.

---

## **Advanced Usage**

### **1. Pull the Docker Image:**
```bash
docker pull carbon2029/dockweb
```

### **2. Run the Container:**
Run the container while supplying credentials for one or more supported extensions:
```bash
docker run -d --env ALL_EMAIL=<your_email> --env ALL_PASS=<your_password> \
  --volume ./chrome_user_data:/chrome_user_data \
  --publish 5000:5000 carbon2029/dockweb
```

### **3. Monitor the Container:**
To verify if the container is running:
```bash
docker ps
```

### **4. Stop the Container:**
```bash
docker stop <container_id>
```

---

## **Key Features**

- **Multi-Extension Support:** Run multiple web extensions in a single container.
- **Simple Setup:** Minimal configuration required for deployment.
- **Resource Optimization:** Reduces system overhead by consolidating extensions.
- **Scalability:** Designed to accommodate new extensions as they emerge.
- **Cross-Platform Compatibility:** Works on any Docker-supported system.

---

## **Frequently Asked Questions (FAQ)**

### **Is DockWeb lightweight?**
Currently, resource usage is as follows:
- **CPU:** ~0.01 - 1%
- **RAM:** ~400 MB (With 3 apps)

Future updates will focus on further optimizations to reduce resource consumption.

### **Do these extensions generate revenue?**
As of **Feb 9, 2025**, only Grass and Nodepay have successfully distributed an airdrop. Other platforms claim to offer payouts in the future. Users should exercise discretion and only participate if they trust the respective platforms.

---

## **License**

This software is distributed under the [GNU General Public License (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html). Users are free to redistribute and modify it in accordance with the license terms.

**Disclaimer:** This software is provided "as is," without warranty of any kind. Users assume full responsibility for any risks associated with its usage.

---

## **Acknowledgments**

Special thanks to [MRColorR](https://github.com/MRColorR) for contributions to this project.

If you find this project helpful, consider using the referral links provided. Your support helps fund the development of more free and open-source projects. ❤️