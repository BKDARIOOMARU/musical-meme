# Deployment Quick Start

## 🚀 What's Ready to Deploy

### ✅ GitHub
- Code pushed to `main` branch
- GitHub Actions CI/CD running on every push
- Automated tests on Python 3.9, 3.10, 3.11
- Docker image auto-built and pushed to GHCR

**GitHub Repo**: https://github.com/BKDARIOOMARU/musical-meme

### ✅ Docker & Cloud Ready
- `Dockerfile` for containerized deployment
- Ready for: Google Cloud Run, Azure Container Instances, AWS ECS, Heroku

### ✅ Mobile Wrapper (Capacitor)
- Android/iOS support configured
- Ready to build APK for Google Play Store
- `mobile/` directory with build config

---

## 📱 Deploy to Google Play Store (Step-by-Step)

### Phase 1: Prepare (30 mins)

**1. Get a Developer Account**
```
💰 Cost: $25 one-time
🌐 Link: https://play.google.com/console
⏱️  Time: 5 mins
```

**2. Generate Signing Key** (on your local machine)
```bash
keytool -genkey -v -keystore release-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias release-key
```
Keep `release-key.jks` **private** (don't commit to GitHub)

---

### Phase 2: Build APK (45 mins)

**1. Clone and setup**
```bash
git clone https://github.com/BKDARIOOMARU/musical-meme
cd musical-meme/mobile
npm install
```

**2. Add Android platform**
```bash
npx cap add android
npx cap sync
```

**3. Configure signing** (`mobile/android/app/build.gradle`)
```gradle
signingConfigs {
    release {
        storeFile file('path/to/release-key.jks')
        storePassword 'your-password'
        keyAlias 'release-key'
        keyPassword 'your-password'
    }
}
```

**4. Build signed APK**
```bash
cd android
./gradlew assembleRelease
```

Output: `android/app/build/outputs/apk/release/app-release.apk` (~15–30 MB)

---

### Phase 3: Submit to Play Store (2 hours)

**1. Create app in Play Console**
- Go to https://play.google.com/console
- Click "Create App"
- Name: "AI Music Generator"
- Accept all declarations

**2. Upload APK**
- Navigate to **Production → Releases**
- Click "Create Release"
- Upload `app-release.apk`
- Add release notes:
  ```
  🎹 Instrumental Synthesis - Create melodies with customizable tempo & genre
  🎤 Lyrics to Vocals - Convert text to sung vocals
  🎲 Random Mode - Discover unexpected musical ideas
  ⚡ Fast Preview - Quick cached generation
  📥 Download - Export as WAV/MP3
  ```

**3. Complete store listing**
- ✏️ App icon (512×512 PNG)
- ✏️ Feature graphic (1024×500 PNG)
- ✏️ 4–8 screenshots from the app
- ✏️ Short description (80 chars): 
  ```
  Create, remix, and download AI-generated music instantly.
  ```
- ✏️ Full description (use [STORE_LISTING.md](STORE_LISTING.md))

**4. Content rating**
- Complete questionnaire
- Select "All Ages"

**5. Submit for review**
- Click "Submit App"
- ⏳ Google reviews in 2–48 hours
- 📊 Monitor in dashboard

---

## ☁️ Alternative Cloud Deployments

### Google Cloud Run (Free tier)
```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT-ID/ai-music-generator

# Deploy
gcloud run deploy ai-music-generator \
  --image gcr.io/PROJECT-ID/ai-music-generator \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Access at: https://ai-music-generator-xxxxx.run.app
```

### Azure Container Instances
```bash
az container create \
  --resource-group myResourceGroup \
  --name ai-music-gen \
  --image ghcr.io/BKDARIOOMARU/musical-meme:latest \
  --ports 8501
```

### Heroku (via Docker)
```bash
heroku container:push web
heroku container:release web
heroku open
```

---

## 📊 Monitoring

### GitHub Actions
Watch tests run automatically:
```
https://github.com/BKDARIOOMARU/musical-meme/actions
```

### Docker Image
Pull the latest built image:
```bash
docker pull ghcr.io/BKDARIOOMARU/musical-meme:latest
```

### Google Play Console
Monitor app metrics:
- Installs & uninstalls
- Crash reports
- User reviews
- Geographic distribution

---

## 🔄 Update Workflow

After making changes:

```bash
# 1. Commit locally
git add -A
git commit -m "feature: description"

# 2. Push to GitHub
git push origin main

# 3. GitHub Actions auto-tests + builds Docker

# 4. For new Play Store version:
#    - Update version in mobile/capacitor.config.ts
#    - Rebuild APK
#    - Upload to Play Console
```

---

## ✅ Checklist

- [ ] GitHub repo pushed
- [ ] GitHub Actions running (check Actions tab)
- [ ] Docker image built (check GHCR)
- [ ] Google Play Developer account created
- [ ] Signing key generated
- [ ] APK built and tested locally
- [ ] App details filled in Play Console
- [ ] Screenshots uploaded
- [ ] Submitted for review
- [ ] App published 🎉

---

## 🆘 Troubleshooting

**APK won't build?**
```bash
cd mobile/android
./gradlew clean
./gradlew assembleRelease
```

**Tests fail on GitHub?**
Check logs: https://github.com/BKDARIOOMARU/musical-meme/actions

**App crashes on Android device?**
```bash
adb logcat | grep "ai-music-generator"
```

**Play Console rejects APK?**
- Ensure target SDK ≥ 31
- Check signing certificate validity
- Review security scan results

---

## 📚 Full Documentation

- **Development**: [README.md](README.md)
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Play Store**: [STORE_LISTING.md](STORE_LISTING.md)
- **Mobile Build**: [mobile/README.md](mobile/README.md)

---

**Next step**: Start building the APK! 🚀
