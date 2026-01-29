# 📱 Download Your APK

## ✅ APK Building Now

Your GitHub Actions workflow is **automatically building the APK** right now!

### 📊 Check Build Status

Open this link to see the build progress:

**→ [GitHub Actions Build](https://github.com/BKDARIOOMARU/musical-meme/actions)**

---

## 📥 Download the APK (when build completes)

Once the build finishes (~5–10 minutes):

1. Go to **GitHub Actions**: https://github.com/BKDARIOOMARU/musical-meme/actions
2. Click the latest **"Build Android APK"** workflow
3. Scroll down to **"Artifacts"** section
4. Download one of:
   - **app-debug.apk** — Ready to test on your phone right now ✅
   - **app-release-unsigned.apk** — For Play Store submission (needs signing)
   - **release-notes** — Build details

---

## 🔧 Install & Test Debug APK

### On Your Android Phone:

**Option 1: USB Install (Fastest)**
```bash
# On your computer:
adb install ~/Downloads/app-debug.apk

# Wait for "Success"
```

**Option 2: Manual Install**
1. Download `app-debug.apk` to your phone
2. Open file manager on phone
3. Tap the APK file
4. Allow installation from unknown sources
5. Install

### ✅ Test the App
- Try **Instrumental** mode (generate a melody)
- Try **Lyrics to Vocals** (convert text to singing)
- Try **Random** mode (explore procedural music)
- Download WAV files

---

## 📦 Sign & Submit Release APK

Once you're happy with testing:

1. **Download** `app-release-unsigned.apk`
2. **Sign** it with your keystore:
```bash
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore release-key.jks \
  app-release-unsigned.apk release-key
```

3. **Align** (optimize):
```bash
zipalign -v 4 app-release-unsigned.apk app-release-signed.apk
```

4. **Upload** to Google Play Console:
   - https://play.google.com/console
   - Production → Releases → Create Release
   - Upload `app-release-signed.apk`

---

## 🔄 Auto-Build on Every Change

From now on:
- Every push to `main` triggers a new APK build
- You can download fresh APKs anytime
- Great for rapid testing & iteration

---

## ✨ What's Included in This Build

✅ **Streamlit Web App** (Python backend)  
✅ **Capacitor Mobile Wrapper** (Android bridge)  
✅ **Synthesis Engines** (all 3 modes working)  
✅ **Audio Export** (WAV format)  
✅ **All dependencies** (bundled)

---

## 🆘 Build Failed?

Check the GitHub Actions logs:
1. Go to https://github.com/BKDARIOOMARU/musical-meme/actions
2. Click the failed workflow
3. Click the job name
4. Scroll down to see error details
5. Common issues:
   - Java not found → Retry (sometimes transient)
   - Android SDK issue → Check Android setup
   - Node version mismatch → Update Node locally

---

## 📞 Need Help?

- **APK won't install?** Check Android version (needs 6.0+)
- **App crashes on startup?** Check device storage
- **Audio not working?** Ensure microphone permission granted
- **Build takes too long?** GitHub Actions queues builds, may wait a few minutes

---

**Next Step**: Download and test the APK on your device! 🎵
