# Deployment Guide

## GitHub Deployment

### 1. Initial Commit & Push

```bash
cd /workspaces/musical-meme
git add -A
git commit -m "feat: initial AI Music Generator with synthesis and TTS

- Instrumental melody generation with harmonics and reverb
- Lyrics-to-vocals using pyttsx3 TTS
- 5 genre presets (Electronic, Pop, Classical, Hip-Hop, Ambient)
- Preview playback with caching
- WAV/MP3 export support
- Comprehensive test suite"
git push origin main
```

### 2. Create GitHub Releases

```bash
git tag -a v1.0.0 -m "Initial release: AI Music Generator"
git push origin v1.0.0
```

### 3. GitHub Actions CI/CD

Once pushed, workflows run automatically:
- ✅ Tests run on Python 3.9, 3.10, 3.11
- ✅ Docker image built and pushed to GHCR
- ✅ Accessible via `ghcr.io/BKDARIOOMARU/musical-meme:latest`

---

## Docker Deployment

### Build Locally

```bash
docker build -t ai-music-generator:latest .
docker run -p 8501:8501 ai-music-generator:latest
```

### Deploy to Cloud

#### Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/ai-music-generator
gcloud run deploy ai-music-generator --image gcr.io/PROJECT-ID/ai-music-generator
```

#### Azure Container Instances
```bash
az container create \
  --resource-group myResourceGroup \
  --name ai-music-gen \
  --image ghcr.io/BKDARIOOMARU/musical-meme:latest \
  --ports 8501 \
  --environment-variables STREAMLIT_SERVER_HEADLESS=true
```

#### AWS ECS / Heroku
Push image to ECR or Heroku Registry; configure environment variables.

---

## Google Play Store Deployment

### Prerequisites
1. **Google Play Developer Account**: $25 one-time fee
2. **Signing Key**: Generate keystore for APK signing
3. **App Assets**: Screenshots, descriptions, icons

### Step-by-Step

#### 1. Generate Signing Key
```bash
keytool -genkey -v -keystore release-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias release-key
```

Store `release-key.jks` securely (add to `.gitignore`).

#### 2. Build Signed APK
```bash
cd mobile
npm install
npx cap add android
npx cap sync
cd android
./gradlew assembleRelease
```

Signed APK: `android/app/build/outputs/apk/release/app-release.apk`

#### 3. Create App in Google Play Console

**Console**: https://play.google.com/console

Steps:
- Click "Create App"
- Fill in app name: "AI Music Generator"
- Accept declarations (content rating, target audience)
- Complete app setup

#### 4. Upload APK

Under **Production → Releases**:
- Click "Create Release"
- Upload `app-release.apk`
- Add release notes (see STORE_LISTING.md)
- Review and confirm

#### 5. Complete Store Listing

**App Details**:
- [ ] App icon (512×512 PNG)
- [ ] Feature graphic (1024×500 PNG)
- [ ] Screenshots (min 2, max 8)
- [ ] Short description (80 chars)
- [ ] Full description (see STORE_LISTING.md)

**Content Rating**:
- [ ] Complete questionnaire
- [ ] Select "All Ages"

**Target Audience & Content**:
- [ ] Unrated
- [ ] No ads, no in-app purchases

**Privacy Policy**:
- [ ] Add link (create privacy.md in repo)

#### 6. Submit for Review

- Click "Submit App"
- Google reviews in 2–48 hours
- Monitor review status in dashboard

#### 7. Monitor & Update

After launch:
- Monitor crash reports and ANRs
- Respond to reviews on Play Store
- Plan next version with user feedback
- Use Play Console analytics to track installs and retention

---

## Version Updates

### For Each Release:

1. **Update version in**:
   - `mobile/capacitor.config.ts` (`version` field)
   - `mobile/android/app/build.gradle` (`versionCode`, `versionName`)

2. **Commit and tag**:
   ```bash
   git commit -am "chore: bump to v1.1.0"
   git tag -a v1.1.0 -m "v1.1.0: [feature description]"
   git push origin main --tags
   ```

3. **Build and upload**:
   ```bash
   cd mobile
   npm run build:android
   # Upload new APK to Play Console
   ```

---

## Troubleshooting

### APK Won't Build
```bash
cd mobile/android
./gradlew clean
./gradlew assembleRelease
```

### Play Console Rejects APK
- Check target SDK (should be ≥31)
- Verify signing certificate
- Review system logs in Play Console

### App Crashes on Device
- Check logcat: `adb logcat | grep "ai-music-generator"`
- Test on emulator first
- Review permissions in `AndroidManifest.xml`

---

## CI/CD Status

Check deployment status:
- GitHub Actions: https://github.com/BKDARIOOMARU/musical-meme/actions
- Docker Registry: https://ghcr.io/BKDARIOOMARU/musical-meme
- Google Play Console: https://play.google.com/console

