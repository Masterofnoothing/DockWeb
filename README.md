# 🚢 DockWeb: Unified Web Extension Deployment

<div align="center">

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/carbon2029/dockweb)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/gpl-3.0)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=for-the-badge)](https://github.com/carbon2029/dockweb/issues)

*A versatile Docker solution for running multiple web extensions in a single container*

</div>

---

## 🌟 Overview

DockWeb is a powerful Docker image designed to efficiently run multiple web extensions within a single container. As the landscape of monetizable web extensions expands, DockWeb provides a seamless "set it and forget it" solution for managing and deploying them collectively.

### ✨ Key Features

- 🔄 **Multi-Extension Support** - Run multiple web extensions simultaneously
- ⚡ **Resource Optimization** - Reduces system overhead by consolidating extensions
- 📈 **Scalability** - Designed to accommodate new extensions as they emerge
- 🖥️ **Cross-Platform** - Works on any Docker-supported system
- 💾 **Persistent Sessions** - Maintains login states across container restarts

---

## 📱 Supported Applications

| Application | Referral Code | Status |
|-------------|---------------|---------|
| [🌱 Grass](https://app.getgrass.io/register/?referralCode=cDmWvtOKIDU-7T-) | `cDmWvtOKIDU-7T-` | ✅ Active |
| [🎨 GradientNode](https://app.gradient.network/signup?code=5VSBV9) | `5VSBV9` | ✅ Active |
| [🌅 DawnInternet](https://www.dawninternet.com/) | `sufx302h` | ✅ Active |
| [💰 NodePay](https://app.nodepay.ai/register?ref=EHEzbYy5vbpP2cj) | `EHEzbYy5vbpP2cj` | ✅ Active |
| [🔥 Teneo]([https://bit.ly/teneo-community-node](https://dashboard.teneo.pro/auth/signup?referralCode=S7erg)) | `S7erg` | ❌ Inactive |

> 💡 **Pro Tip:** Using referral codes helps support the development of this free project!

---

## 🚀 Quick Start

### One-Click Deployment (Recommended)

```bash
docker run -d \
  --name dockweb \
  --env ALL_EMAIL=your_email@example.com \
  --env ALL_PASS=your_password \
  --volume ./chrome_user_data:/app/chrome_user_data \
  --publish 5000:5000 \
  --restart unless-stopped \
  carbon2029/dockweb
```

### 🔧 Individual Extension Configuration

If you prefer to configure extensions individually:

```bash
docker run -d \
  --name dockweb \
  --env GRASS_USER=your_email@example.com \
  --env GRASS_PASS=your_password \
  --env GRADIENT_EMAIL=your_email@example.com \
  --env GRADIENT_PASS=your_password \
  --env DAWN_EMAIL=your_email@example.com \
  --env DAWN_PASS=your_password \
  --volume ./chrome_user_data:/app/chrome_user_data \
  --publish 5000:5000 \
  --restart unless-stopped \
  carbon2029/dockweb
```

> 📝 **Note:** You only need to include variables for the extensions you plan to use.

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ALL_EMAIL` | Universal email for all extensions | `user@example.com` |
| `ALL_PASS` | Universal password for all extensions | `your_password` |
| `GRASS_USER` | Grass extension email | `user@example.com` |
| `GRASS_PASS` | Grass extension password | `grass_password` |
| `GRADIENT_EMAIL` | GradientNode extension email | `user@example.com` |
| `GRADIENT_PASS` | GradientNode extension password | `gradient_password` |
| `DAWN_EMAIL` | Dawn extension email | `user@example.com` |
| `DAWN_PASS` | Dawn extension password | `dawn_password` |
| `TENO_COOKIE` | Teneo cookie ([setup guide](Instructions/teneo.md)) | `cookie_value` |
| `NP_COOKIE` | NodePay cookie ([setup guide](Instructions/nodepay.md)) | `cookie_value` |

### Volume Mounts

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `./chrome_user_data` | `/app/chrome_user_data` | Session persistence |

### Port Mapping

| Host Port | Container Port | Purpose |
|-----------|----------------|---------|
| `5000` | `5000` | Web interface access |

---

## 🔧 Advanced Usage

### Step-by-Step Setup

1. **Pull the Docker Image**
   ```bash
   docker pull carbon2029/dockweb
   ```

2. **Create Data Directory** (Optional but recommended)
   ```bash
   mkdir -p ./chrome_user_data
   ```

3. **Run the Container**
   ```bash
   docker run -d \
     --name dockweb \
     --env ALL_EMAIL=your_email@example.com \
     --env ALL_PASS=your_password \
     --volume ./chrome_user_data:/app/chrome_user_data \
     --publish 5000:5000 \
     --restart unless-stopped \
     carbon2029/dockweb
   ```

4. **Monitor Container Status**
   ```bash
   docker ps
   docker logs dockweb
   ```

5. **To Solve Dawn Captcha**
   Open your browser and navigate to `http://localhost:5000`

### Container Management

```bash
# View running containers
docker ps

# Check container logs
docker logs dockweb

# Stop the container
docker stop dockweb

# Start the container
docker start dockweb

# Remove the container
docker rm dockweb
```

---

## 📊 Performance & Resources

### Current Resource Usage

| Metric | Value | Notes |
|--------|-------|-------|
| **CPU Usage** | ~0.01 - 1% | Minimal impact |
| **RAM Usage** | ~522 MB | With 5 apps running |
| **Storage** | Variable | Depends on session data |

> 🎯 **Optimization Goal:** Future updates will focus on further reducing resource consumption.

---

## 💰 Revenue Information

### Payout Status (as of Feb 9, 2025)

| Platform | Airdrop Status | Notes |
|----------|----------------|-------|
| 🌱 **Grass** | ✅ **Paid** | Successfully distributed |
| 💰 **NodePay** | ✅ **Paid** | Successfully distributed |
| 🎨 **GradientNode** | ⏳ **Pending** | Claims future payouts |
| 🌅 **DawnInternet** | ⏳ **Pending** | Claims future payouts |
| 🔥 **Teneo** | ⏳ **Pending** | Claims future payouts |

> ⚠️ **Disclaimer:** Exercise discretion and only participate if you trust the respective platforms.

---

## 🆕 Recent Updates

### Latest Changelog

- ✅ **Fixed Grass Lite Node** - Yes the recent issues with grass lite node is fixed it should be functional
- 🔔 **Discord Webhooks** - Currently in development
- 🐛 **Bug Reports Welcome** - Found an issue? [Create one here](https://github.com/carbon2029/dockweb/issues)

### Upcoming Features

- 🤖 **Auto-login for Captcha Services** - Working on bypassing Cloudflare challenges
- 📊 **Enhanced Monitoring** - Better logging and status reporting
- 🎨 **Improved Web Interface** - More user-friendly dashboard

---

## 🤔 Frequently Asked Questions

<details>
<summary><strong>Why use DockWeb instead of browser extensions?</strong></summary>

DockWeb provides several advantages:
- **Security**: Isolates unknown extensions from your personal browser
- **Resource Management**: Centralized control over all extensions
- **Automation**: "Set it and forget it" approach
- **Scalability**: Easy to manage multiple accounts or extensions
</details>

<details>
<summary><strong>Is DockWeb resource-intensive?</strong></summary>

No! DockWeb is designed to be lightweight:
- CPU usage: ~0.01-1%
- RAM usage: ~522MB with 5 applications
- Continuous optimization efforts to reduce footprint further
</details>

<details>
<summary><strong>How do I handle Captcha challenges?</strong></summary>

For NodePay and Teneo:
- These services use Cloudflare captcha protection
- Currently requires manual cookie extraction
- Refer to setup guides: [Teneo](Instructions/teneo.md) | [NodePay](Instructions/nodepay.md)
- Auto-login solution is in development
</details>

<details>
<summary><strong>Will you add more applications?</strong></summary>

Yes, but selectively:
- Apps must show genuine potential
- Personal testing and validation required
- Community demand considered
- No "trash apps" that may never pay
- Suggest new apps via [GitHub Issues](https://github.com/carbon2029/dockweb/issues)
</details>

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

- 🐛 **Report Bugs** - [Open an issue](https://github.com/carbon2029/dockweb/issues)
- 💡 **Suggest Features** - Share your ideas
- 🏗️ **Submit PRs** - Code contributions are welcome
- 📖 **Improve Documentation** - Help make guides clearer

---

## 🙏 Acknowledgments

- **Alternative Solution** - Check out [money4band](https://github.com/MRColorR/money4band) for easier setup
- **Community Support** - Thanks to all users providing feedback and suggestions

---

## 📞 Contact & Support

- **Issues & Bugs**: [GitHub Issues](https://github.com/carbon2029/dockweb/issues)
- **General Inquiries**: masterofnoothing@proton.me
- **App Developers**: If you have concerns about your app being listed, please reach out

---

## 📄 License & Legal

### License
This software is distributed under the [GNU General Public License (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html). Users are free to redistribute and modify it in accordance with the license terms.

### Disclaimer
This software is provided "as is," without warranty of any kind. Users assume full responsibility for any risks associated with its usage.

### Important Notice
This project was created solely to enhance the experience of real users. I do not condone or support:
- ❌ Farming or automation abuse
- ❌ Proxy misuse
- ❌ Application terms violation

---

<div align="center">

### 💖 Support the Project

If you find DockWeb helpful, consider:
- ⭐ Starring the repository
- 🔗 Using the provided referral links
- 🤝 Contributing to the codebase
- 📢 Sharing with others

*Your support helps fund the development of more free and open-source projects!*

---

**Made with ❤️ by the DockWeb Team**

</div>

